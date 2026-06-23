from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QSpinBox, QHeaderView
from PySide6.QtCore import Qt

class PlanTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(8)
        self.setHorizontalHeaderLabels([
            "Chọn làm", "STT", "Nội dung", "Số người", 
            "Phút", "Dụng cụ", "Vật tư", "Tiêu chuẩn"
        ])
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

    def add_row(self, data):
        row = self.rowCount()
        self.insertRow(row)
        # Checkbox
        chk = QTableWidgetItem()
        chk.setCheckState(Qt.CheckState.Unchecked)
        self.setItem(row, 0, chk)
        
        # SpinBox cho số người
        spin = QSpinBox()
        spin.setRange(1, 100)
        spin.setValue(int(data.get("people", 1)))
        self.setCellWidget(row, 3, spin)
        
        # Các cột khác...
        self.setItem(row, 2, QTableWidgetItem(data.get("task", "")))