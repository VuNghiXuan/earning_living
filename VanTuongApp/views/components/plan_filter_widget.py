import json
import os
from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QLabel, 
                               QComboBox, QDateEdit, QPushButton, QSpinBox, QHBoxLayout, QGridLayout)
from PySide6.QtCore import QDate
import config.app_config as cfg

class FilterWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Bộ lọc thông tin lập kế hoạch", parent)
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
        
        # Tạo nút thay thế ComboBox
        self.btn_tao_phieu = QPushButton("➕ Tạo phiếu công nghệ")
        self.btn_tao_phieu.setStyleSheet("""
            QPushButton {
                background-color: #FFD700; 
                color: black;
                font-weight: bold;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover { background-color: #FFC107; }
        """)

        # 2. Xây dựng Layout bằng QGridLayout (8 cột)
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(5, 5, 5, 5)
        grid_layout.setSpacing(10)

        # Hàng 1
        grid_layout.addWidget(QLabel("Kế hoạch BQDP:"), 0, 0)
        grid_layout.addWidget(self.cb_phieu, 0, 1)
        grid_layout.addWidget(QLabel("Số ngày:"), 0, 2)
        grid_layout.addWidget(self.spin_duration, 0, 3)
        grid_layout.addWidget(QLabel("Bắt đầu:"), 0, 4)
        grid_layout.addWidget(self.date_start, 0, 5)
        grid_layout.addWidget(QLabel("Kết thúc:"), 0, 6)
        grid_layout.addWidget(self.date_end, 0, 7)

        # Hàng 2
        grid_layout.addWidget(QLabel("Nhóm:"), 1, 0)
        grid_layout.addWidget(self.cb_group, 1, 1)
        
        grid_layout.addWidget(QLabel("Trang bị:"), 1, 2)
        grid_layout.addWidget(self.cb_device, 1, 3)
        grid_layout.addWidget(QLabel("Nhân viên:"), 1, 4)
        grid_layout.addWidget(self.spin_nhan_vien, 1, 5)
        
        # Nút Tạo phiếu chiếm 2 cột (6 và 7)
        grid_layout.addWidget(self.btn_tao_phieu, 1, 6, 1, 2)

        # Cấu hình độ co giãn
        for i in range(8):
            if i % 2 != 0: 
                grid_layout.setColumnStretch(i, 1)
            else:
                grid_layout.setColumnMinimumWidth(i, 80)
        
        # Lưu ý: Cột 6 và 7 đã chiếm 2 cột, nên cột 7 không cần setStretch riêng nữa
        grid_layout.setColumnStretch(7, 0) 

        main_v_layout = QVBoxLayout(self)
        main_v_layout.addLayout(grid_layout)
        self.setFixedHeight(120)

        # 3. Kết nối sự kiện
        self.cb_phieu.currentIndexChanged.connect(self.load_duration_from_config)
        self.spin_duration.valueChanged.connect(lambda: self.update_logic('duration'))
        self.date_start.dateChanged.connect(lambda: self.update_logic('start'))
        self.date_end.dateChanged.connect(lambda: self.update_logic('end'))
        
        self.load_duration_from_config()

    def load_duration_from_config(self):
        """Load thời hạn từ file dựa trên tên phiếu đang chọn"""
        phieu_name = self.cb_phieu.currentText()
        config_path = os.path.join('config', 'config.json') 
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    duration = data.get('deadlines', {}).get(phieu_name, 0)
                    
                    # Cập nhật giá trị mà không kích hoạt update_logic nhiều lần
                    self.spin_duration.blockSignals(True)
                    self.spin_duration.setValue(int(duration))
                    self.spin_duration.blockSignals(False)
                    
                    # Sau khi có số ngày, thực hiện tính toán ngày kết thúc
                    self.update_logic('duration')
        except Exception as e:
            print(f"Lỗi đọc config: {e}")

    def update_logic(self, trigger_source):
        """Xử lý tính toán ngày tháng 2 chiều"""
        self.spin_duration.blockSignals(True)
        self.date_start.blockSignals(True)
        self.date_end.blockSignals(True)

        try:
            if trigger_source in ['duration', 'start']:
                days = self.spin_duration.value()
                new_end = self.date_start.date().addDays(days)
                self.date_end.setDate(new_end)
            
            elif trigger_source == 'end':
                days = self.date_start.date().daysTo(self.date_end.date())
                self.spin_duration.setValue(max(0, days))
        finally:
            # Luôn unblock kể cả khi có lỗi xảy ra
            self.spin_duration.blockSignals(False)
            self.date_start.blockSignals(False)
            self.date_end.blockSignals(False)