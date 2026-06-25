from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QLabel, 
                               QComboBox, QDateEdit, QPushButton, QSpinBox, QGridLayout)
from PySide6.QtCore import QDate
import config.app_config as cfg

class FilterWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Bộ lọc thông tin lập kế hoạch", parent)
        
        # Khởi tạo đối tượng DB
        from models.plan_model import PlanModel
        self.db = PlanModel()

        self.setStyleSheet("""
            QGroupBox { font-weight: bold; margin-top: 10px; padding-top: 10px; }
            QLabel { font-weight: bold; color: #0078D7; margin-left: 5px; }
        """)

        # 1. Khởi tạo Widget
        self.cb_phieu = QComboBox()
        self.spin_duration = QSpinBox()
        self.spin_duration.setRange(0, 365)
        self.spin_duration.setSuffix(" ngày")
        
        self.date_start = QDateEdit(QDate.currentDate())
        self.date_start.setCalendarPopup(True)
        self.date_start.setDisplayFormat("dd/MM/yyyy")
        
        self.date_end = QDateEdit(QDate.currentDate())
        self.date_end.setCalendarPopup(True)
        self.date_end.setDisplayFormat("dd/MM/yyyy")
        
        self.cb_group = QComboBox()
        self.cb_device = QComboBox()
        self.spin_nhan_vien = QSpinBox()
        self.spin_nhan_vien.setRange(1, 100)
        self.spin_nhan_vien.setValue(1)
        
        self.btn_tao_phieu = QPushButton("➕ Tạo phiếu công nghệ")
        self.btn_tao_phieu.setStyleSheet("""
            QPushButton { background-color: #FFD700; color: black; font-weight: bold; border-radius: 4px; padding: 5px; }
            QPushButton:hover { background-color: #FFC107; }
        """)

        # 2. Xây dựng Layout
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(5, 5, 5, 5)
        # Thiết lập cột (Label không giãn, Widget giãn)
        for i in range(8):
            if i % 2 == 0: 
                grid_layout.setColumnStretch(i, 0) # Label giữ nguyên vị trí
            else:
                grid_layout.setColumnStretch(i, 1) # Widget giãn ra
                
        grid_layout.setSpacing(5) # Giảm spacing xuống 5 thay vì 10
        grid_layout.addWidget(QLabel("Kế hoạch BQDP:"), 0, 0)
        grid_layout.addWidget(self.cb_phieu, 0, 1)
        grid_layout.addWidget(QLabel("Số ngày thực hiện:"), 0, 2)
        grid_layout.addWidget(self.spin_duration, 0, 3)
        grid_layout.addWidget(QLabel("Bắt đầu:"), 0, 4)
        grid_layout.addWidget(self.date_start, 0, 5)
        grid_layout.addWidget(QLabel("Kết thúc:"), 0, 6)
        grid_layout.addWidget(self.date_end, 0, 7)

        grid_layout.addWidget(QLabel("Nhóm thực hiện:"), 1, 0)
        grid_layout.addWidget(self.cb_group, 1, 1)
        grid_layout.addWidget(QLabel("Trang bị:"), 1, 2)
        grid_layout.addWidget(self.cb_device, 1, 3)
        grid_layout.addWidget(QLabel("Nhân viên:"), 1, 4)
        grid_layout.addWidget(self.spin_nhan_vien, 1, 5)
        grid_layout.addWidget(self.btn_tao_phieu, 1, 6, 1, 2)

        main_v_layout = QVBoxLayout(self)
        main_v_layout.addLayout(grid_layout)
        self.setFixedHeight(120)

        # 3. Kết nối sự kiện
        self.cb_phieu.currentIndexChanged.connect(self.load_duration_from_db)
        self.spin_duration.valueChanged.connect(lambda: self.update_logic('duration'))
        self.date_start.dateChanged.connect(lambda: self.update_logic('start'))
        self.date_end.dateChanged.connect(lambda: self.update_logic('end'))
        self.cb_group.currentIndexChanged.connect(self.update_devices_list)
        self.cb_phieu.currentIndexChanged.connect(self.update_devices_list)
        
        self.load_groups_to_cb()

    def load_duration_from_db(self):
        """Lấy số ngày từ DB dựa trên tên phiếu"""
        phieu_name = self.cb_phieu.currentText()
        if phieu_name == "Tất cả loại phiếu": return

        # Gọi hàm get_setting từ model (db) của bạn
        duration = self.db.get_setting(f"deadline_{phieu_name}", "0")
        
        self.spin_duration.blockSignals(True)
        self.spin_duration.setValue(int(duration))
        self.spin_duration.blockSignals(False)
        self.update_logic('duration')

    def update_logic(self, trigger_source):
        self.spin_duration.blockSignals(True)
        self.date_start.blockSignals(True)
        self.date_end.blockSignals(True)
        try:
            if trigger_source in ['duration', 'start']:
                days = self.spin_duration.value()
                self.date_end.setDate(self.date_start.date().addDays(days))
            elif trigger_source == 'end':
                days = self.date_start.date().daysTo(self.date_end.date())
                self.spin_duration.setValue(max(0, days))
        finally:
            self.spin_duration.blockSignals(False)
            self.date_start.blockSignals(False)
            self.date_end.blockSignals(False)
    
    def load_groups_to_cb(self):
        self.cb_group.clear()
        self.cb_group.addItem("Chưa phân loại")
        self.cb_group.addItems(self.db.get_all_group_names() or [])

    def update_devices_list(self):
        group_name = self.cb_group.currentText()
        phieu_name = self.cb_phieu.currentText()
        if not group_name or not phieu_name or phieu_name == "Tất cả loại phiếu":
            self.cb_device.clear()
            return
        self.cb_device.blockSignals(True)
        self.cb_device.clear()
        devices = self.db.get_devices_by_group_and_cycle(group_name, phieu_name)
        self.cb_device.addItems(devices if devices else ["Không có máy phù hợp"])
        self.cb_device.blockSignals(False)