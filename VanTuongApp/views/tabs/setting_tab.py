from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QGroupBox, QFormLayout, QLabel, QDateEdit, QTimeEdit, QPushButton
from PySide6.QtCore import Qt, QDate, QTime

# from components.custom_table import CustomTableWidget
# from views.styles.table_styles import TABLE_WIDGET_STYLE

import config.app_config as cfg  # Nạp cấu hình tập trung để đồng bộ bộ nhận diện

class SettingTabWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # --- 1. KHỞI TẠO THANH TAB LỚN MÀU HẢI QUÂN ---
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(cfg.TAB_BAR_STYLE)
        
        # --- 🎨 NẠP CẤU HÌNH STYLE TẬP TRUNG TỪ CONFIG (Sạch bóng code CSS thủ công) ---
        group_style = cfg.SETTING_GROUP_BOX_STYLE
        input_style = cfg.SETTING_INPUT_STYLE
        label_style = cfg.SETTING_LABEL_STYLE

        # --- SUB-TAB 1: QUỐC GIA / VÙNG MIỀN MẶC ĐỊNH ---
        sub_tab_locale = QWidget()
        locale_layout = QVBoxLayout(sub_tab_locale)
        locale_layout.setContentsMargins(10, 10, 10, 10)
        
        self.box_locale = QGroupBox("Định dạng vùng miền hệ thống")
        self.box_locale.setStyleSheet(group_style)
        fl_locale = QFormLayout(self.box_locale)
        
        lbl_format_title = QLabel("Định dạng ngày mặc định:")
        lbl_format_title.setStyleSheet(label_style)
        lbl_format = QLabel("dd/MM/yyyy (Việt Nam)")
        lbl_format.setStyleSheet(f"font-weight: bold; color: {cfg.COLOR_SUCCESS}; font-size: {cfg.FONT_SIZE_REGULAR};")
        fl_locale.addRow(lbl_format_title, lbl_format)
        
        lbl_preview_title = QLabel("Xem trước ngày hiện tại:")
        lbl_preview_title.setStyleSheet(label_style)
        self.date_preview = QDateEdit()
        self.date_preview.setDate(QDate.currentDate())
        self.date_preview.setDisplayFormat("dd/MM/yyyy")
        self.date_preview.setReadOnly(True)
        self.date_preview.setStyleSheet(input_style)
        fl_locale.addRow(lbl_preview_title, self.date_preview)
        
        locale_layout.addWidget(self.box_locale)
        locale_layout.addStretch()
        
        # --- SUB-TAB 2: THỜI GIAN LÀM VIỆC HÀNH CHÍNH ---
        sub_tab_worktime = QWidget()
        worktime_layout = QVBoxLayout(sub_tab_worktime)
        worktime_layout.setContentsMargins(10, 10, 10, 10)
        
        self.box_worktime = QGroupBox("Thời gian làm việc hành chính")
        self.box_worktime.setStyleSheet(group_style)
        fl_worktime = QFormLayout(self.box_worktime)
        
        self.time_am_start = QTimeEdit(QTime(8, 0))
        self.time_am_end = QTimeEdit(QTime(11, 30))
        self.time_pm_start = QTimeEdit(QTime(13, 30))
        self.time_pm_end = QTimeEdit(QTime(17, 0))
        
        # Áp dụng bộ stylesheet tập trung cho từng ô nhập liệu thời gian
        for widget in [self.time_am_start, self.time_am_end, self.time_pm_start, self.time_pm_end]:
            widget.setStyleSheet(input_style)
            
        lbl_am_start = QLabel("Ca Sáng - Bắt đầu:")
        lbl_am_start.setStyleSheet(label_style)
        lbl_am_end = QLabel("Ca Sáng - Kết thúc:")
        lbl_am_end.setStyleSheet(label_style)
        lbl_pm_start = QLabel("Ca Chiều - Bắt đầu:")
        lbl_pm_start.setStyleSheet(label_style)
        lbl_pm_end = QLabel("Ca Chiều - Kết thúc:")
        lbl_pm_end.setStyleSheet(label_style)
        
        fl_worktime.addRow(lbl_am_start, self.time_am_start)
        fl_worktime.addRow(lbl_am_end, self.time_am_end)
        fl_worktime.addRow(lbl_pm_start, self.time_pm_start)
        fl_worktime.addRow(lbl_pm_end, self.time_pm_end)
        
        worktime_layout.addWidget(self.box_worktime)
        worktime_layout.addStretch()
        
        # --- SUB-TAB 3: THỜI GIAN TĂNG CA NGOÀI GIỜ ---
        sub_tab_ot = QWidget()
        ot_layout = QVBoxLayout(sub_tab_ot)
        ot_layout.setContentsMargins(10, 10, 10, 10)
        
        self.box_ot = QGroupBox("Thời gian tăng ca ngoài giờ (OT)")
        self.box_ot.setStyleSheet(group_style)
        fl_ot = QFormLayout(self.box_ot)
        
        self.time_ot_start = QTimeEdit(QTime(17, 30))
        self.time_ot_end = QTimeEdit(QTime(19, 30))
        
        self.time_ot_start.setStyleSheet(input_style)
        self.time_ot_end.setStyleSheet(input_style)
        
        lbl_ot_start = QLabel("Tăng ca - Thời gian Bắt đầu:")
        lbl_ot_start.setStyleSheet(label_style)
        lbl_ot_end = QLabel("Tăng ca - Thời gian Kết thúc:")
        lbl_ot_end.setStyleSheet(label_style)
        
        fl_ot.addRow(lbl_ot_start, self.time_ot_start)
        fl_ot.addRow(lbl_ot_end, self.time_ot_end)
        
        ot_layout.addWidget(self.box_ot)
        ot_layout.addStretch()
        
        # --- ĐƯA CÁC SUB-TAB VÀO BỘ KHUNG CHÍNH ---
        self.tab_widget.addTab(sub_tab_locale, "📍 Cấu hình mặc định")
        self.tab_widget.addTab(sub_tab_worktime, "☀️ Thời gian làm việc")
        self.tab_widget.addTab(sub_tab_ot, "🌙 Thời gian tăng ca")
        layout.addWidget(self.tab_widget)
        
        # --- 💾 NÚT LƯU CẤU HÌNH TOÀN CỤC ---
        # Áp dụng bộ style nút bấm Cam Radar từ config tập trung
        self.btn_save_config = QPushButton("💾 Lưu cấu hình toàn bộ hệ thống")
        self.btn_save_config.setStyleSheet(cfg.BTN_SETTING_STYLE)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.btn_save_config)
        layout.addLayout(button_layout)