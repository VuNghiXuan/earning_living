from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QButtonGroup, QScrollArea
from PySide6.QtCore import Qt, Signal

import config.app_config as cfg

class SidebarWidget(QWidget):
    # Tạo tín hiệu custom để thông báo cho QStackedWidget đổi trang
    current_index_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_collapsed = False
        self.setFixedWidth(260)
        
        # Đảm bảo nền của widget gốc luôn chiếm toàn bộ chiều cao sidebar
        self.setStyleSheet(cfg.SIDEBAR_CONTAINER_STYLE)
        
        # Danh sách dữ liệu Menu mẫu
        self.menu_data = [
            ("📅", " Lập kế hoạch"),
            ("🗂️", " Danh mục & Định mức"),
            ("⚙️", " Cấu hình hệ thống"),
        ]
        self.menu_buttons = []
        self.init_ui()
        
    def init_ui(self):
        # Layout chính của toàn bộ Sidebar
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        
        # --- 1. NÚT THU GỌN / MỞ RỘNG (TOGGLE ZONE) ---
        toggle_layout = QHBoxLayout()
        toggle_layout.setContentsMargins(5, 5, 5, 0)
        self.btn_toggle = QPushButton("☰")
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.setStyleSheet(cfg.TOGGLE_BTN_STYLE)
        self.btn_toggle.setFixedWidth(45)
        self.btn_toggle.clicked.connect(self.toggle_sidebar)
        toggle_layout.addWidget(self.btn_toggle, 0, Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addLayout(toggle_layout)
        
        # --- 2. KHUNG THÔNG TIN CÔNG TY (BRAND ZONE) ---
        self.brand_frame = QFrame()
        self.brand_frame.setStyleSheet(cfg.BRAND_FRAME_STYLE)
        self.brand_layout = QVBoxLayout(self.brand_frame)
        self.brand_layout.setSpacing(6)
        
        self.lbl_company = QLabel(cfg.COMPANY_NAME)
        self.lbl_company.setWordWrap(True)
        self.lbl_company.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # SỬA LỖI: Chuyển COLOR_TEXT_HIGHLIGHT thành màu vàng chỉ huy COLOR_PRIMARY chuẩn hóa
        self.lbl_company.setStyleSheet(f"font-weight: bold; font-size: {cfg.FONT_SIZE_COMPANY}; color: {cfg.COLOR_PRIMARY};")
        
        self.lbl_dept = QLabel(cfg.DEPARTMENT_NAME)
        self.lbl_dept.setWordWrap(True)
        self.lbl_dept.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_dept.setStyleSheet(f"font-size: {cfg.FONT_SIZE_REGULAR}; color: {cfg.COLOR_TEXT_MUTED};")
        
        self.brand_layout.addWidget(self.lbl_company)
        self.brand_layout.addWidget(self.lbl_dept)
        self.main_layout.addWidget(self.brand_frame)
        
        # --- 3. VÙNG CUỘN MENU TỰ ĐỘNG (SCROLL ZONE CHO MENU) ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Định hình style cho thanh cuộn tiệp màu tối với hệ thống (Dark Theme Scrollbar)
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{ border: none; background-color: transparent; }}
            QScrollBar:vertical {{
                background: {cfg.COLOR_BG_DARK}; width: 6px; margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #555555; min-height: 20px; border-radius: 3px;
            }}
            QScrollBar::handle:vertical:hover {{ background: {cfg.COLOR_PRIMARY}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ border: none; background: none; }}
        """)
        
        # Tạo widget chứa danh sách nút bấm bên trong vùng cuộn
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet(f"background-color: {cfg.COLOR_BG_DARK};")
        self.menu_layout = QVBoxLayout(self.scroll_content)
        self.menu_layout.setContentsMargins(0, 10, 0, 0)
        self.menu_layout.setSpacing(2)
        
        self.button_group = QButtonGroup(self)
        
        for idx, (icon, text) in enumerate(self.menu_data):
            btn = QPushButton()
            btn.setText(f" {icon}   {text}")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(cfg.MENU_ITEM_STYLE)
            
            btn.clicked.connect(lambda checked, i=idx: self.on_menu_clicked(i))
            
            self.menu_layout.addWidget(btn)
            self.menu_buttons.append(btn)
            self.button_group.addButton(btn, idx)
            
        # Thêm khoảng giãn ở cuối vùng cuộn để đẩy menu lên đầu
        self.menu_layout.addStretch()
        
        # Nạp content vào ScrollArea và đẩy ScrollArea vào bố cục chính
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)
        
        # Mặc định kích hoạt dòng đầu tiên
        if self.menu_buttons:
            self.menu_buttons[0].setChecked(True)
            self.menu_buttons[0].setStyleSheet(cfg.MENU_ITEM_SELECTED_STYLE)

    def on_menu_clicked(self, index):
        """Đồng bộ hóa giao diện nút bấm khi click chuột dựa trên cấu hình tập trung"""
        for btn in self.menu_buttons:
            if self.is_collapsed:
                btn.setStyleSheet(cfg.MENU_ITEM_COLLAPSED_STYLE)
            else:
                btn.setStyleSheet(cfg.MENU_ITEM_STYLE)
                
        # Áp dụng style được chọn từ cấu hình tương ứng
        active_btn = self.menu_buttons[index]
        if self.is_collapsed:
            active_btn.setStyleSheet(cfg.MENU_ITEM_COLLAPSED_SELECTED_STYLE)
        else:
            active_btn.setStyleSheet(cfg.MENU_ITEM_SELECTED_STYLE)
            
        self.current_index_changed.emit(index)

    def toggle_sidebar(self):
        """Hàm xử lý logic co/giãn thanh điều hướng an toàn và sạch sẽ"""
        if not self.is_collapsed:
            # 1. TIẾN HÀNH THU GỌN (Collapse)
            self.setFixedWidth(65)
            self.brand_frame.hide()
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            
            for idx, btn in enumerate(self.menu_buttons):
                icon = self.menu_data[idx][0]
                btn.setText(icon)
                # Sử dụng cấu hình tập trung chuyên biệt cho giao diện co gọn
                if btn.isChecked():
                    btn.setStyleSheet(cfg.MENU_ITEM_COLLAPSED_SELECTED_STYLE)
                else:
                    btn.setStyleSheet(cfg.MENU_ITEM_COLLAPSED_STYLE)
                
            self.is_collapsed = True
        else:
            # 2. TIẾN HÀNH MỞ RỘNG (Expand)
            self.setFixedWidth(260)
            self.brand_frame.show()
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            
            for idx, btn in enumerate(self.menu_buttons):
                icon, text = self.menu_data[idx]
                btn.setText(f" {icon}   {text}")
                # Hoàn tác sạch sẽ về các Style gốc định nghĩa trong file Config
                if btn.isChecked():
                    btn.setStyleSheet(cfg.MENU_ITEM_SELECTED_STYLE)
                else:
                    btn.setStyleSheet(cfg.MENU_ITEM_STYLE)
                    
            self.is_collapsed = False