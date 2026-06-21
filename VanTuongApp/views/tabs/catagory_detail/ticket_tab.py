from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTableWidget, QPushButton, QHeaderView
import config.app_config as cfg

class TicketTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        box = QGroupBox("Danh mục các loại phiếu")
        box.setStyleSheet(cfg.SETTING_GROUP_BOX_STYLE)
        inner = QVBoxLayout(box)
        
        self.table_tickets = QTableWidget()
        self.table_tickets.setColumnCount(3)
        self.table_tickets.setHorizontalHeaderLabels(["Mã", "Tên Phiếu", "Mô tả"])
        self.table_tickets.setStyleSheet(cfg.TABLE_WIDGET_STYLE)
        self.table_tickets.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        inner.addWidget(self.table_tickets)
        
        self.btn_add_ticket = QPushButton("➕ Thêm loại phiếu mới")
        inner.addWidget(self.btn_add_ticket)
        layout.addWidget(box)