from PySide6.QtWidgets import (QTableWidget, QTableWidgetItem, QHeaderView, 
                               QSpinBox, QComboBox, QLineEdit, QCheckBox, 
                               QWidget, QHBoxLayout, QSizePolicy)
from PySide6.QtCore import Qt

class PlanTable(QTableWidget):
    def __init__(self, row_count=9):
        super().__init__(row_count + 1, 8)
        
        # 1. Cấu hình cho phép co dãn linh hoạt
        # Expanding giúp bảng chiếm không gian còn dư trong layout
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setAlternatingRowColors(True)
        
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        
        # Cấu hình header co dãn tự động theo bảng
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 2. StyleSheet
        self.setStyleSheet("""
            QTableWidget {
                gridline-color: #dcdcdc;
                border: 1px solid #dcdcdc;
                alternate-background-color: #f2f2f2;
                background-color: white;
            }
            QTableWidget::item {
                border: 1px solid #dcdcdc;
            }
        """)
        
        self.setup_header_row()
        self.setup_data_rows()

    def setup_header_row(self):
        self.chk_select_all = QCheckBox("Chọn tất cả")
        self.chk_select_all.setStyleSheet("font-weight: bold; padding: 5px;")
        self.chk_select_all.stateChanged.connect(self.select_all_rows)
        
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(self.chk_select_all)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setCellWidget(0, 0, widget)
        
        headers = ["", "Nội dung", "Số người", "Thời gian", "Phương tiện", "Vật tư", "TCKT", "Kết quả"]
        for col in range(1, 8):
            item = QTableWidgetItem(headers[col])
            item.setTextAlignment(Qt.AlignCenter)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            item.setBackground(Qt.lightGray)
            self.setItem(0, col, item)

    def setup_data_rows(self):
        for row in range(1, self.rowCount()):
            chk = QCheckBox()
            chk.setObjectName("row_checkbox")
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.addWidget(chk)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(5, 0, 5, 0)
            self.setCellWidget(row, 0, widget)
            
            for col in range(1, 8):
                if col == 2:
                    spin = QSpinBox(); spin.setRange(0, 100)
                    self.setCellWidget(row, col, spin)
                elif col == 3:
                    cb = QComboBox(); cb.addItems(["15", "30", "45", "60"])
                    self.setCellWidget(row, col, cb)
                else:
                    self.setCellWidget(row, col, QLineEdit())

    def select_all_rows(self, state):
        is_checked = (state == 2)
        for row in range(1, self.rowCount()):
            container = self.cellWidget(row, 0)
            if container:
                chk = container.findChild(QCheckBox, "row_checkbox")
                if chk:
                    chk.blockSignals(True)
                    chk.setCheckState(Qt.Checked if is_checked else Qt.Unchecked)
                    chk.blockSignals(False)