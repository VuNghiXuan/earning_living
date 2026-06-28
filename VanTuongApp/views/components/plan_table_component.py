from PySide6.QtWidgets import (QTableWidget, QTableWidgetItem, QHeaderView, 
                               QSpinBox, QComboBox, QCheckBox, QWidget, 
                               QHBoxLayout, QTextEdit, QAbstractItemView, QLabel)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QTextOption, QFont, QColor
from itertools import groupby

class AutoResizeTextEdit(QTextEdit):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("border: none; background: transparent; padding: 2px; font-size: 13px;")

    def sizeHint(self):
        # Tính toán chiều cao cần thiết dựa trên nội dung
        doc = self.document()
        height = doc.size().height()
        return QSize(self.width(), int(height) + 5)

class PlanTable(QTableWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setup_header()
        self.apply_style()

    def setup_header(self):
        headers = ["Chọn", "STT", "Nội dung công việc", "Số người", "Thời gian(phút)", "Phương tiện", "Vật tư", "TCKT", "Kết quả"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        header = self.horizontalHeader()
        widths = [60, 50, 0, 80, 150, 150, 150, 150, 150]
        for i, w in enumerate(widths):
            if w > 0:
                self.setColumnWidth(i, w)
                header.setSectionResizeMode(i, QHeaderView.Fixed)
            else:
                header.setSectionResizeMode(i, QHeaderView.Stretch)

    def apply_style(self):
        self.setStyleSheet("""
            QTableWidget { 
                gridline-color: #e0e0e0; 
                background-color: #ffffff; 
                alternate-background-color: #f2f7f9; 
                border: 1px solid #d1d1d1;
            }
            QHeaderView::section { 
                background-color: #417690; 
                color: #ffffff; 
                padding: 8px; 
                border: 1px solid #355d71; 
                font-weight: bold;
                font-size: 13px;
            }
            QTableWidget::item { padding: 5px; }
            QTableWidget::item:hover { background-color: #d1e5ef; color: #000000; }
            QTableWidget::item:selected { background-color: #79aec8; color: #ffffff; }
        """)

    def populate_table(self, payload):
        tasks_data = payload.get("tasks", [])
        self.metadata = payload.get("metadata", {})
        
        # Cập nhật nhãn tiêu đề phiếu (nếu UI có chứa header_label)
        if hasattr(self, 'header_label'):
            nhom = self.metadata.get('nhom_thuc_hien', '---')
            so_phieu_chung = self.metadata.get('so_phieu', '---')
            # self.header_label.setText(f"PHIẾU CÔNG NGHỆ: {so_phieu_chung} | NHÓM: {nhom}")

        self.setUpdatesEnabled(False)
        self.clearContents()
        
        tasks_data.sort(key=lambda x: x.get('device_name', ''))
        self.setRowCount(len(tasks_data) + 20) 
        
        current_row = 0
        grouped_tasks = groupby(tasks_data, key=lambda x: x.get('device_name', ''))
        
        for device_name, tasks in grouped_tasks:
            self._draw_device_header(current_row, device_name)
            current_row += 1
            for task in tasks:
                self._draw_task_row(current_row, task)
                current_row += 1
                
        self.setRowCount(current_row)
        self.resizeRowsToContents()
        self.setUpdatesEnabled(True)

    def _draw_device_header(self, row, device_name):
        """Vẽ tiêu đề máy và số phiếu tương ứng"""
        trang_bi_list = self.metadata.get('trang_bi', [])
        so_phieu = next((item.get('so_phieu') for item in trang_bi_list if item.get('ten_may') == device_name), "---")
        
        header_text = f" MÁY: {device_name} | SỐ PHIẾU: {so_phieu}"
        item = QTableWidgetItem(header_text)
        item.setBackground(QColor("#d1e7dd"))
        item.setFont(QFont("Arial", 9, QFont.Bold))
        self.setSpan(row, 0, 1, 9)
        self.setItem(row, 0, item)

    def _draw_task_row(self, row, task):
        # Checkbox
        chk = QCheckBox()
        chk.setChecked(True)
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.addWidget(chk)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setCellWidget(row, 0, w)
        
        # STT
        self.setItem(row, 1, QTableWidgetItem(str(task.get('tt', ''))))
        
        # Các cột nội dung
        cols = [2, 5, 6, 7, 8]
        keys = ['task_name', 'tool', 'material', 'tckt', 'result']
        for i, col in enumerate(cols):
            te = AutoResizeTextEdit(str(task.get(keys[i], '')))
            self.setCellWidget(row, col, te)
            
        self._setup_inputs(row, task)

    def _setup_inputs(self, row, task):
        # Cột 3: Số người
        w_people = QWidget()
        l_people = QHBoxLayout(w_people)
        spin = QSpinBox()
        spin.setValue(int(task.get('norm_workers', 1)))
        l_people.addWidget(spin)
        l_people.setContentsMargins(0,0,0,0)
        self.setCellWidget(row, 3, w_people)
        
        # Cột 4: Thời gian
        w_time = QWidget()
        l_time = QHBoxLayout(w_time)
        cb = QComboBox()
        cb.addItems(["15", "30", "45", "60", "90"])
        cb.setCurrentText(str(task.get('norm_minutes', '30')))
        l_time.addWidget(cb)
        l_time.setContentsMargins(0,0,0,0)
        self.setCellWidget(row, 4, w_time)
        
    def resizeRowsToContents(self):
        # Thiết lập cơ bản
        super().resizeRowsToContents()
        
        # Duyệt qua từng hàng để điều chỉnh chiều cao
        for row in range(self.rowCount()):
            max_h = 40  # Chiều cao tối thiểu cho hàng
            
            for col in range(self.columnCount()):
                w = self.cellWidget(row, col)
                # Nếu ô này chứa AutoResizeTextEdit, lấy sizeHint của nó
                if isinstance(w, AutoResizeTextEdit):
                    # Cập nhật lại document width trước khi lấy sizeHint
                    w.document().setTextWidth(self.columnWidth(col))
                    h = w.sizeHint().height()
                    if h > max_h:
                        max_h = h
            
            # Cập nhật chiều cao hàng
            self.setRowHeight(row, max_h + 10) # +10 để có khoảng đệm (padding)