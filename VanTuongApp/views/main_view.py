from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QFrame, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from views.sidebar import SidebarWidget
from views.tabs.setting_tab import SettingTabWidget
from views.tabs.plan_tab import PlanTabWidget
from views.tabs.category_tab import CategoryTabWidget

import config.app_config as cfg

class MainView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.init_ui()
        
    # =====================================================================
    # 🔥 ĐÂY CHÍNH LÀ CHÌA KHÓA: ÉP HỆ THỐNG BỎ QUA GỢI Ý KÍCH THƯỚC CỦA CÁC TAB CON
    # =====================================================================
    def minimumSizeHint(self):
        from PySide6.QtCore import QSize
        return QSize(400, 300) # Cho phép ứng dụng co giãn tự do từ mức 400x300 trở lên

    def init_ui(self):
        # Ép MainView phải tự động giãn theo cửa sổ cha
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Bố cục hàng ngang bao phủ toàn bộ phần mềm (Sidebar bên trái | Nội dung bên phải)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Gọi thành thành phần Sidebar bên trái (Đã có tính năng thu gọn)
        self.sidebar = SidebarWidget()
        main_layout.addWidget(self.sidebar)
        
        # 2. Khung chứa khu vực bên phải (Gồm Header + Content Tab + Footer)
        right_container = QWidget()
        # Ép khung chứa bên phải luôn chiếm trọn diện tích trống còn lại
        right_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # -----------------------------------------------------------------
        # 🏛️ TẠO LỚP HEADER CỐ ĐỊNH (Tên phần mềm & Công tác)
        # -----------------------------------------------------------------
        header_frame = QFrame()
        header_frame.setStyleSheet(cfg.HEADER_STYLE)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 10, 15, 10)
        
        # Tên phần mềm nằm bên trái
        lbl_header_app = QLabel(cfg.APP_NAME)
        # lbl_header_app.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {cfg.COLOR_PRIMARY};")
        
        # Công tác nhiệm vụ nằm bên phải
        lbl_header_mission = QLabel(cfg.MISSION_NAME)
        lbl_header_mission.setStyleSheet("font-size: 13px; font-weight: 500; font-style: italic; color: #27AE60;")
        
        header_layout.addWidget(lbl_header_app, 0, Qt.AlignmentFlag.AlignLeft)
        header_layout.addStretch()
        header_layout.addWidget(lbl_header_mission, 0, Qt.AlignmentFlag.AlignRight)
        
        right_layout.addWidget(header_frame)
        
        # -----------------------------------------------------------------
        # 📦 VÙNG HIỂN THỊ NỘI DUNG CHÍNH (QStackedWidget)
        # -----------------------------------------------------------------
        self.container = QStackedWidget()
        # self.container.setStyleSheet("background-color: #F8F9FA; padding: 15px;")
        
        # Đảm bảo vùng lật trang co giãn mượt mà theo độ rộng màn hình
        self.container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Khởi tạo 3 Module Tab lớn
        self.tab_plan = PlanTabWidget()
        self.tab_category = CategoryTabWidget(self.model)
        self.tab_setting = SettingTabWidget()
        
        # Đưa vào bộ Stack quản lý trang
        self.container.addWidget(self.tab_plan)      # Chỉ số 0 -> Lập kế hoạch
        self.container.addWidget(self.tab_category)  # Chỉ số 1 -> Danh mục & Định mức
        self.container.addWidget(self.tab_setting)   # Chỉ số 2 -> Cấu hình hệ thống
        
        right_layout.addWidget(self.container, 1) 
        
        # -----------------------------------------------------------------
        # 👣 TẠO LỚP FOOTER CỐ ĐỊNH (Thông tin về sản phẩm)
        # -----------------------------------------------------------------
        footer_frame = QFrame()
        footer_frame.setStyleSheet(cfg.FOOTER_STYLE)
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(15, 5, 15, 5)
        
        # Bản quyền & Phiên bản bên trái
        lbl_footer_left = QLabel(f"© 2026 {cfg.COMPANY_NAME}. Tất cả quyền được bảo lưu.")
        # Thông tin kỹ thuật / Trạng thái hệ thống bên phải
        lbl_footer_right = QLabel("Phiên bản: v2.1.0 Enterprise | Trạng thái: 🟢 Đang kết nối Cơ sở dữ liệu")
        
        footer_layout.addWidget(lbl_footer_left, 0, Qt.AlignmentFlag.AlignLeft)
        footer_layout.addStretch()
        footer_layout.addWidget(lbl_footer_right, 0, Qt.AlignmentFlag.AlignRight)
        
        right_layout.addWidget(footer_frame)
        
        # -----------------------------------------------------------------
        # Đẩy toàn bộ khối bên phải vào Layout tổng của MainView
        # Tham số '1' ép khối bên phải co giãn tối đa (Khác với sidebar cố định width)
        main_layout.addWidget(right_container, 1)
        
        # Kết nối signal của Sidebar để lật trang nội dung ở giữa
        self.sidebar.current_index_changed.connect(self.container.setCurrentIndex)