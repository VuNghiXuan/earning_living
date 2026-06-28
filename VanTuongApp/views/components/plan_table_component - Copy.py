from PySide6.QtWidgets import (QTableWidget, QTableWidgetItem, QHeaderView, 
                               QSpinBox, QComboBox, QCheckBox, QWidget, 
                               QHBoxLayout, QTextEdit, QAbstractItemView)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QTextOption, QFont, QColor

# Giả định màu chủ đạo - Thay bằng mã màu của bạn
# COLOR_PRIMARY = "#f39c12"
from itertools import groupby

class AutoResizeTextEdit(QTextEdit):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("border: none; background: transparent; padding: 5px; font-size: 13px;")

    def sizeHint(self):
        doc = self.document()
        width = self.viewport().width()
        doc.setTextWidth(width)
        return QSize(width, int(doc.size().height()) + 10)

class PlanTable(QTableWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setup_header()
        self.apply_style()

    def setup_header(self):
        headers = ["Chọn", "STT", "Nội dung", "Số người", "Thời gian(phút)", "Phương tiện", "Vật tư", "TCKT", "Kết quả"]
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
                selection-background-color: transparent; /* Tắt mặc định để kiểm soát bằng item:selected */
            }
            QHeaderView::section { 
                background-color: #417690; 
                color: #ffffff; 
                padding: 8px; 
                border: 1px solid #355d71; 
                font-weight: bold;
                font-size: 13px;
            }
            QTableWidget::item { 
                padding: 5px; 
            }
            /* Hiệu ứng di chuột vào (Hover) - Cốt lõi của giao diện Django */
            QTableWidget::item:hover {
                background-color: #d1e5ef; 
                color: #000000;
            }
            /* Khi hàng được chọn */
            QTableWidget::item:selected {
                background-color: #79aec8; 
                color: #ffffff;
            }
        """)

    def populate_table(self, tasks_data):
        """
        tasks_data: List các dict (kết quả từ DB)
        filter_results: Nên được lưu lại trong class để lấy thông tin header (nhóm, số phiếu)
        """
        print(f"[DEBUG] populate_table nhận vào {len(tasks_data)} dòng.")
        
        # CHỐT CHẶN: Dữ liệu công việc PHẢI là một list
        if not isinstance(tasks_data, list):
            print(f"[ERROR] tasks_data phải là list, nhận được: {type(tasks_data)}")
            return

        self.setUpdatesEnabled(False)
        self.clearContents()
        self.setRowCount(len(tasks_data) + 2)

        # --- PHẦN HEADER (Sử dụng dữ liệu từ dòng đầu tiên hoặc biến lưu trữ) ---
        # Giả sử bạn lấy thông tin nhóm từ item đầu tiên
        group_name = tasks_data[0].get('group_name', '---') if tasks_data else "Chưa xác định"
        
        item_group = QTableWidgetItem(f"PHIẾU CÔNG NGHỆ - Nhóm: {group_name}")
        self.setSpan(0, 0, 1, 9)
        self.setItem(0, 0, item_group)

        # 4. Data Rows
        for row, device in enumerate(tasks_data):
            # Đảm bảo device là dictionary trước khi dùng .get()
            if not isinstance(device, dict): 
                continue
            
            r = row + 2
            
            # CHECKBOX: Dùng widget mặc định (an toàn tuyệt đối)
            chk = QCheckBox()
            chk.setChecked(True)
            w = QWidget()
            layout = QHBoxLayout(w)
            layout.addWidget(chk)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            self.setCellWidget(r, 0, w)
            
            # STT
            self.setItem(r, 1, QTableWidgetItem(str(device.get('tt', row + 1))))
            
            # Nội dung & Text Columns
            cols = [2, 5, 6, 7, 8]
            keys = ['task_name', 'tool', 'material', 'tckt', 'result']
            for i, col in enumerate(cols):
                te = AutoResizeTextEdit(str(device.get(keys[i], '')))
                self.setCellWidget(r, col, te)
                
            # Số người & Thời gian
            for col, key in [(3, 'norm_workers'), (4, 'norm_minutes')]:
                w_inner = QWidget()
                layout = QHBoxLayout(w_inner)
                
                if col == 3:
                    spin = QSpinBox()
                    # Ép kiểu an toàn
                    val = device.get(key, 1)
                    spin.setValue(int(val) if str(val).isdigit() else 1)
                    layout.addWidget(spin)
                else:
                    cb = QComboBox()
                    cb.addItems(["15", "30", "45", "60", "90"])
                    cb.setCurrentText(str(device.get(key, '30')))
                    layout.addWidget(cb)
                
                layout.setAlignment(Qt.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                self.setCellWidget(r, col, w_inner)

        self.resizeRowsToContents()
        self.setUpdatesEnabled(True)
        print("[DEBUG] Populate thành công.")
        
    def resizeRowsToContents(self):
        super().resizeRowsToContents()
        for row in range(self.rowCount()):
            h = 60
            for col in range(self.columnCount()):
                w = self.cellWidget(row, col)
                if isinstance(w, AutoResizeTextEdit): h = max(h, w.sizeHint().height())
            self.setRowHeight(row, h)