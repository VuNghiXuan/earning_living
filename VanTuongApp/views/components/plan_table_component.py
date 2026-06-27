from PySide6.QtWidgets import (QTableWidget, QTableWidgetItem, QHeaderView, 
                               QSpinBox, QComboBox, QCheckBox, QWidget, 
                               QHBoxLayout, QTextEdit, QAbstractItemView)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QTextOption

class AutoResizeTextEdit(QTextEdit):
    """Widget tùy chỉnh tự động rớt dòng và báo chiều cao cho bảng"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("""
            QTextEdit {
                border: none;
                background: transparent;
                padding: 5px;
                font-size: 13px;
            }
        """)

    def sizeHint(self):
        doc = self.document()
        # Tính toán chiều cao dựa trên độ rộng thực tế của cột
        width = self.viewport().width()
        doc.setTextWidth(width)
        height = doc.size().height() + 10
        return QSize(width, int(height))

class PlanTable(QTableWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        
        self.setup_header()
        self.apply_style()

    def setup_header(self):
        headers = ["Chọn", "STT", "Nội dung", "Số người", "Thời gian", "Phương tiện", "Vật tư", "TCKT", "Kết quả"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        # Giãn cột nội dung (cột 2) để chiếm không gian
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        # Cố định độ rộng tối thiểu cho các cột quan trọng
        for i in range(len(headers)):
            if i != 2: self.setColumnWidth(i, 150)

    def apply_style(self):
        style = """
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
        """
        self.setStyleSheet(style)

    def populate_table(self, devices_data):
        self.setRowCount(len(devices_data))
        for row, device in enumerate(devices_data):
            # 0. Checkbox
            chk = QCheckBox(); chk.setChecked(True)
            self.setCellWidget(row, 0, chk)
            
            # 1. TT
            self.setItem(row, 1, QTableWidgetItem(str(device.get('tt', row + 1))))
            
            # 2. Nội dung (Dùng AutoResizeTextEdit để rớt dòng)
            text_edit = AutoResizeTextEdit(str(device.get('task_name', '')))
            self.setCellWidget(row, 2, text_edit)
            
            # 3. Số người
            spin = QSpinBox(); spin.setValue(int(device.get('norm_workers', 1)))
            self.setCellWidget(row, 3, spin)
            
            # 4. Thời gian
            cb = QComboBox(); cb.addItems(["15", "30", "45", "60"])
            cb.setCurrentText(str(device.get('norm_minutes', '30')))
            self.setCellWidget(row, 4, cb)
            
            # 5-8. Các cột text khác (Dùng AutoResizeTextEdit cho tất cả để tránh bị che)
            for col, key in enumerate(['tool', 'material', 'tckt', 'result'], 5):
                text_edit_col = AutoResizeTextEdit(str(device.get(key, '')))
                self.setCellWidget(row, col, text_edit_col)

        # Ép bảng cập nhật lại toàn bộ chiều cao các dòng
        self.resizeRowsToContents()

    def resizeRowsToContents(self):
        super().resizeRowsToContents()
        for row in range(self.rowCount()):
            max_height = 80 # Chiều cao tối thiểu
            for col in range(self.columnCount()):
                widget = self.cellWidget(row, col)
                if isinstance(widget, AutoResizeTextEdit):
                    max_height = max(max_height, widget.sizeHint().height())
            self.setRowHeight(row, max_height)