from PySide6.QtWidgets import (QTableWidget, QTableWidgetItem, QHeaderView, 
                               QSpinBox, QComboBox, QLineEdit, QCheckBox, 
                               QWidget, QHBoxLayout, QSizePolicy)
from PySide6.QtCore import Qt

class PlanTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(0, 8) # Khởi tạo 0 dòng, 8 cột
        
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
        
        headers = ["", 'TT', "Nội dung", "Số người", "Thời gian", "Phương tiện", "Vật tư", "TCKT", "Kết quả"]
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
    
    def load_data(self, data_list):
        """
        data_list: List các dictionary chứa thông tin:
        [
            {"noi_dung": "...", "nguoi": 2, "thoi_gian": "30", "phuong_tien": "...", ...},
            ...
        ]
        """
        # Tạm thời disable block signals để không trigger sự kiện không mong muốn
        self.setRowCount(max(len(data_list) + 1, 10)) # Giữ tối thiểu 10 dòng
        
        for i, row_data in enumerate(data_list):
            row = i + 1
            
            # Cột Nội dung
            self.cellWidget(row, 1).setText(row_data.get("noi_dung", ""))
            
            # Cột Số người
            spin = self.cellWidget(row, 2)
            if isinstance(spin, QSpinBox): spin.setValue(int(row_data.get("nguoi", 1)))
            
            # Cột Thời gian
            cb = self.cellWidget(row, 3)
            if isinstance(cb, QComboBox): cb.setCurrentText(str(row_data.get("thoi_gian", "15")))
            
            # Cột Phương tiện, Vật tư, TCKT, Kết quả
            self.cellWidget(row, 4).setText(row_data.get("phuong_tien", ""))
            self.cellWidget(row, 5).setText(row_data.get("vat_tu", ""))
            self.cellWidget(row, 6).setText(row_data.get("tckt", ""))
            self.cellWidget(row, 7).setText(row_data.get("ket_qua", ""))