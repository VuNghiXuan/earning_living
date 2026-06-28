from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class PlanHeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        self.title_label = QLabel("PHIẾU CÔNG NGHỆ BQDP - KSĐK")
        self.title_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.group_label = QLabel("NHÓM: ---")
        self.group_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.group_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.group_label)
        layout.setContentsMargins(0, 0, 0, 10)

    def update_info(self, filter_data):
        nhom = filter_data.get('nhom_thuc_hien', '---')
        # phieu = filter_data.get('so_phieu', '---')
        
        # Cập nhật văn bản cho các label trong header
        # self.title_label.setText(f"PHIẾU CÔNG NGHỆ BQDP")
        self.group_label.setText(f"NHÓM: {nhom}")