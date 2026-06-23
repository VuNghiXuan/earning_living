from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QComboBox, QDateEdit, QPushButton, QTableWidget, QHeaderView
from PySide6.QtCore import Qt, QDate

import config.app_config as cfg  # Nạp file cấu hình tập trung để đồng bộ bộ nhận diện

class PlanTabWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10) # Tạo khoảng cách viền cho thoáng
        
        # --- 1. KHỞI TẠO TAB WIDGET LỚN ---
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(cfg.TAB_BAR_STYLE)
        
        # --- SUB-TAB 1: LẬP KẾ HOẠCH TRONG NGÀY ---
        sub_tab_create = QWidget()
        create_layout = QVBoxLayout(sub_tab_create)
        create_layout.setContentsMargins(15, 15, 15, 15)
        
        filter_layout = QHBoxLayout()
        self.cb_group = QComboBox()
        self.cb_device = QComboBox()
        self.cb_cycle = QComboBox()
        
        # Nút Tải Biểu Mẫu Gốc (Nạp style nút bấm vàng chỉ huy từ config)
        self.btn_load = QPushButton("⚡ Tải Biểu Mẫu Gốc")
        self.btn_load.setStyleSheet(cfg.BTN_PLAN_STYLE)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        
        filter_layout.addWidget(QLabel("Ngày thực hiện:"))
        filter_layout.addWidget(self.date_edit)
        filter_layout.addWidget(QLabel("Nhóm:"))
        filter_layout.addWidget(self.cb_group, 1)
        filter_layout.addWidget(QLabel("Máy:"))
        filter_layout.addWidget(self.cb_device, 2)
        filter_layout.addWidget(QLabel("Phiếu:"))
        filter_layout.addWidget(self.cb_cycle, 1)
        filter_layout.addWidget(self.btn_load, 0)
        create_layout.addLayout(filter_layout)
        
        # Khởi tạo bảng dữ liệu kế hoạch chính
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Chọn làm", "STT", "Nội dung công việc bảo dưỡng", "Số người (ĐM)", 
            "Thời gian (Phút)", "Phương tiện dụng cụ", "Vật tư kỹ thuật", "Tiêu chuẩn kỹ thuật (TCKT)"
        ])
        
        # Nạp bộ style bảng biểu chuẩn hóa tập trung từ config
        self.table.setStyleSheet(cfg.TABLE_WIDGET_STYLE)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        create_layout.addWidget(self.table)
        
        export_layout = QHBoxLayout()
        self.btn_export = QPushButton("📥 XUẤT BÁO CÁO WORD KẾ HOẠCH NGÀY")
        self.btn_export.setStyleSheet(cfg.BTN_PLAN_STYLE)
        export_layout.addStretch()
        export_layout.addWidget(self.btn_export)
        create_layout.addLayout(export_layout)
        
        # --- SUB-TAB 2: LỊCH SỬ KẾ HOẠCH ---
        sub_tab_history = QWidget()
        history_layout = QVBoxLayout(sub_tab_history)
        history_layout.setContentsMargins(15, 15, 15, 15)
        
        lbl_hist_info = QLabel("📜 Danh sách các file kế hoạch, nhật ký bảo dưỡng đã xuất bản ghi nhận trong hệ thống:")
        lbl_hist_info.setStyleSheet(f"font-weight: bold; color: {cfg.COLOR_BG_BRAND}; font-size: {cfg.FONT_SIZE_REGULAR};")
        
        self.table_history = QTableWidget()
        self.table_history.setColumnCount(4)
        self.table_history.setHorizontalHeaderLabels(["Ngày lập", "Tên thiết bị máy móc", "Loại phiếu bảo dưỡng", "Đường dẫn file lưu trữ"])
        
        # Tái sử dụng cấu hình bảng tập trung
        self.table_history.setStyleSheet(cfg.TABLE_WIDGET_STYLE)
        self.table_history.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        history_layout.addWidget(lbl_hist_info)
        history_layout.addWidget(self.table_history)
        
        # --- SUB-TAB 3: THỐNG KÊ THEO NĂM ---
        sub_tab_stats = QWidget()
        stats_layout = QVBoxLayout(sub_tab_stats)
        stats_layout.setContentsMargins(15, 15, 15, 15)
        
        lbl_stats_info = QLabel("📊 Thống kê chất lượng công tác bảo quản, bảo dưỡng kỹ thuật theo từng năm:")
        lbl_stats_info.setStyleSheet(f"font-weight: bold; color: {cfg.COLOR_BG_BRAND}; font-size: {cfg.FONT_SIZE_REGULAR};")
        
        self.table_stats = QTableWidget()
        self.table_stats.setColumnCount(4)
        self.table_stats.setHorizontalHeaderLabels(["Năm", "Tổng số giờ bảo dưỡng", "Số lượt trang bị hoàn thành", "Tỷ lệ đạt chuẩn TCKT (%)"])
        
        # Tái sử dụng cấu hình bảng tập trung
        self.table_stats.setStyleSheet(cfg.TABLE_WIDGET_STYLE)
        self.table_stats.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        stats_layout.addWidget(lbl_stats_info)
        stats_layout.addWidget(self.table_stats)

        # =====================================================================
        # 🔩 LẮP RÁP CÁC SUB-TAB VÀO KHUNG CHÍNH ĐỂ GIỮ BỘ NHỚ C++ AN TOÀN
        # =====================================================================
        self.tab_widget.addTab(sub_tab_create, "⚡ Lập kế hoạch")
        self.tab_widget.addTab(sub_tab_history, "📜 Lịch sử kế hoạch")
        self.tab_widget.addTab(sub_tab_stats, "📊 Thống kê năm")
        
        layout.addWidget(self.tab_widget)