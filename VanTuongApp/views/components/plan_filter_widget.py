from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QLabel, 
                               QComboBox, QDateEdit, QPushButton, QSpinBox, QGridLayout)
from PySide6.QtCore import QDate, Qt
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
        for i in range(8):
            grid_layout.setColumnStretch(i, 1 if i % 2 != 0 else 0)
                
        grid_layout.setSpacing(5)
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
        grid_layout.addWidget(QLabel("Trang bị/Máy:"), 1, 2)
        grid_layout.addWidget(self.cb_device, 1, 3)
        grid_layout.addWidget(QLabel("Số nhân viên:"), 1, 4)
        grid_layout.addWidget(self.spin_nhan_vien, 1, 5)
        grid_layout.addWidget(self.btn_tao_phieu, 1, 6, 1, 2)

        main_v_layout = QVBoxLayout(self)
        main_v_layout.addLayout(grid_layout)
        self.setFixedHeight(120)

        # 3. Kết nối sự kiện & Khởi tạo dữ liệu ban đầu
        self.spin_duration.valueChanged.connect(lambda: self.update_logic('duration'))
        self.date_start.dateChanged.connect(lambda: self.update_logic('start'))
        self.date_end.dateChanged.connect(lambda: self.update_logic('end'))
        
        self.cb_phieu.currentIndexChanged.connect(lambda: self.update_filters('phieu'))
        self.cb_group.currentIndexChanged.connect(lambda: self.update_filters('group'))
       
        self.init_data()

    def init_data(self):
        """Nạp dữ liệu lần đầu"""
        self.cb_group.blockSignals(True)
        self.cb_phieu.blockSignals(True)
        self.cb_group.addItem("-- Chọn nhóm --")
        self.cb_group.addItems(self.db.get_all_group_names() or [])
        self.cb_phieu.addItem("-- Chọn phiếu --")
        self.cb_phieu.addItems(self.db.get_all_phieu_names() or [])
        self.cb_group.blockSignals(False)
        self.cb_phieu.blockSignals(False)

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

    def refresh_data(self):
        """Làm mới toàn bộ dữ liệu bộ lọc từ DB"""
        self.cb_group.blockSignals(True)
        self.cb_phieu.blockSignals(True)
        self.cb_device.blockSignals(True)
        
        # 1. Lưu giá trị hiện tại (nếu muốn giữ lựa chọn của user)
        current_phieu = self.cb_phieu.currentText()
        current_group = self.cb_group.currentText()
        
        # 2. Làm mới danh sách Nhóm
        self.cb_group.clear()
        self.cb_group.addItem("-- Chọn nhóm --")
        self.cb_group.addItems(self.db.get_all_group_names() or [])
        
        # 3. Làm mới danh sách Phiếu
        self.cb_phieu.clear()
        self.cb_phieu.addItem("-- Chọn phiếu --")
        self.cb_phieu.addItems(self.db.get_all_phieu_names() or [])
        
        # 4. Khôi phục lựa chọn cũ nếu còn tồn tại trong danh sách mới
        if self.cb_group.findText(current_group) != -1:
            self.cb_group.setCurrentText(current_group)
        if self.cb_phieu.findText(current_phieu) != -1:
            self.cb_phieu.setCurrentText(current_phieu)
            
        self.cb_group.blockSignals(False)
        self.cb_phieu.blockSignals(False)
        self.cb_device.blockSignals(False)
        
        # 5. Cập nhật lại máy
        self.update_filters('group')

    def update_filters(self, trigger_source):
        # Lưu giá trị cũ
        val_phieu = self.cb_phieu.currentText()
        val_group = self.cb_group.currentText()
        
        self.cb_group.blockSignals(True)
        self.cb_phieu.blockSignals(True)
        self.cb_device.blockSignals(True)

        try:
            phieu_val = val_phieu if val_phieu != "-- Chọn phiếu --" else None
            group_val = val_group if val_group not in ["-- Chọn nhóm --", "Chưa phân loại"] else None

            if trigger_source == 'phieu':
                # 1. Cập nhật Nhóm
                groups = self.db.get_groups_by_cycle(phieu_val)
                self.cb_group.clear()
                self.cb_group.addItem("-- Chọn nhóm --")
                if groups: self.cb_group.addItems(groups)
                
                # 2. Cập nhật Máy (Lọc theo cả Phiếu và Nhóm hiện tại)
                devices = self.db.get_devices_by_filter(cycle_code=phieu_val, group_name=group_val)
                self.cb_device.clear()
                if devices: self.cb_device.addItems(devices)

            elif trigger_source == 'group':
                # 1. Cập nhật Phiếu
                cycles = self.db.get_cycles_by_group(group_val)
                self.cb_phieu.clear()
                self.cb_phieu.addItem("-- Chọn phiếu --")
                if cycles: self.cb_phieu.addItems(cycles)
                
                # 2. Cập nhật Máy (Lọc theo cả Phiếu và Nhóm hiện tại)
                # Lưu ý: Lúc này phieu_val có thể đã bị "rỗng" do clear, 
                # cần kiểm tra lại nếu muốn giữ filter phiếu cũ
                devices = self.db.get_devices_by_filter(cycle_code=phieu_val, group_name=group_val)
                self.cb_device.clear()
                if devices: self.cb_device.addItems(devices)

        finally:
            # KHÔI PHỤC GIÁ TRỊ: Chỉ khôi phục nếu giá trị vẫn tồn tại trong danh sách mới
            if phieu_val and self.cb_phieu.findText(phieu_val) != -1:
                self.cb_phieu.setCurrentText(phieu_val)
            else:
                self.cb_phieu.setCurrentIndex(0) # Reset về "-- Chọn phiếu --"

            if group_val and self.cb_group.findText(group_val) != -1:
                self.cb_group.setCurrentText(group_val)
            else:
                self.cb_group.setCurrentIndex(0) # Reset về "-- Chọn nhóm --"

            self.cb_device.blockSignals(False)
            self.cb_group.blockSignals(False)
            self.cb_phieu.blockSignals(False)
    
    