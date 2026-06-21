from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QDateEdit,
                             QSpinBox, QPushButton, QTableWidget, QTableWidgetItem, QCheckBox, QHeaderView)
from PySide6.QtCore import Qt, QDate

class TabPlanView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # 1. Cụm bộ lọc phía trên nâng cấp trường Từ ngày -> Đến ngày
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        self.cb_group = QComboBox()
        self.cb_device = QComboBox()
        self.cb_cycle = QComboBox()
        self.cb_cycle.addItems(["Tuần (Phiếu 01)", "Tháng (Phiếu 02)", "Quý (Phiếu 03)", "Trước/Sau đi biển (Phiếu 04)"])
        
        # Cấu hình trường Ngày tháng
        self.date_from = QDateEdit(QDate.currentDate())
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat("dd/MM/yyyy")
        
        self.date_to = QDateEdit(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("dd/MM/yyyy")
        
        self.sp_workers = QSpinBox()
        self.sp_workers.setRange(1, 10)
        self.sp_workers.setValue(2)
        
        self.btn_load = QPushButton("Tải Biểu Mẫu")
        self.btn_load.setStyleSheet("background-color: #0078D4; color: white; font-weight: bold; padding: 5px 10px; border-radius:0px;")
        
        filter_layout.addWidget(QLabel("Nhóm:"))
        filter_layout.addWidget(self.cb_group, 1)
        filter_layout.addWidget(QLabel("Trang bị:"))
        filter_layout.addWidget(self.cb_device, 1)
        filter_layout.addWidget(QLabel("Chu kỳ:"))
        filter_layout.addWidget(self.cb_cycle, 1)
        filter_layout.addWidget(QLabel("Từ ngày:"))
        filter_layout.addWidget(self.date_from, 0)
        filter_layout.addWidget(QLabel("Đến ngày:"))
        filter_layout.addWidget(self.date_to, 0)
        filter_layout.addWidget(QLabel("Số người:"))
        filter_layout.addWidget(self.sp_workers, 0)
        filter_layout.addWidget(self.btn_load, 0)
        
        layout.addLayout(filter_layout)
        
        # 2. Khung lưới phẳng vuông vức chuẩn Excel
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["STT", "Nội dung công việc", "Số người", "Dự kiến thời gian (hh:mm)", "Phương tiện dụng cụ", "Vật tư", "Kết quả"])
        self.table.setStyleSheet("""
            QTableWidget { gridline-color: #D2D2D2; border: 1px solid #D2D2D2; border-radius: 0px; background-color: white; }
            QTableWidget::item { border-bottom: 1px solid #E0E0E0; padding: 5px; }
            QHeaderView::section { background-color: #F3F3F3; border: 1px solid #D2D2D2; border-radius: 0px; font-weight: bold; padding: 4px; }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
        
        # 3. Thanh hành động
        action_layout = QHBoxLayout()
        self.btn_import_word = QPushButton("Nạp File Word Định Mức (Admin)")
        self.btn_import_word.setStyleSheet("background-color: #7B2CBF; color: white; padding: 8px;")
        
        self.btn_export = QPushButton("XUẤT BÁO CÁO WORD")
        self.btn_export.setStyleSheet("background-color: #107C41; color: white; font-weight: bold; padding: 8px 20px; border-radius:0px;")
        
        action_layout.addWidget(self.btn_import_word)
        action_layout.addStretch()
        action_layout.addWidget(self.btn_export)
        layout.addLayout(action_layout)