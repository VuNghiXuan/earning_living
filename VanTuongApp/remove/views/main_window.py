from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget
from PySide6.QtCore import Qt
from views.tab_plan import TabPlanView
from views.tab_config import TabConfigView
from views.tab_category import TabCategoryView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý bảo trì trang thiết bị - Tường Vân Apps")
        
        self.setWindowFlags(Qt.WindowType.Window | 
                            Qt.WindowType.WindowMinimizeButtonHint | 
                            Qt.WindowType.WindowMaximizeButtonHint | 
                            Qt.WindowType.WindowCloseButtonHint)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar điều hướng phẳng
        sidebar = QWidget()
        sidebar.setStyleSheet("background-color: #201F1E; max-width: 220px; min-width: 200px;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)
        
        self.btn_nav_plan = QPushButton(" Lập Kế Hoạch")
        self.btn_nav_category = QPushButton(" Quản Lý Danh Mục") # Thêm nút danh mục
        self.btn_nav_config = QPushButton(" Cấu Hình Giờ")
        
        nav_style = """
            QPushButton { text-align: left; padding: 10px; color: #F3F3F3; background-color: transparent; border: none; font-size: 14px; font-weight: bold;}
            QPushButton:hover { background-color: #323130; }
            QPushButton:checked { background-color: #0078D4; color: white; }
        """
        for btn in [self.btn_nav_plan, self.btn_nav_category, self.btn_nav_config]:
            btn.setStyleSheet(nav_style)
            btn.setCheckable(True)
            sidebar_layout.addWidget(btn)
            
        self.btn_nav_plan.setChecked(True)
        sidebar_layout.addStretch()
        
        # Vùng nội dung Stack các Tab
        self.stacked_widget = QStackedWidget()
        self.view_plan = TabPlanView()
        self.view_category = TabCategoryView() # Khởi tạo View quản lý danh mục
        self.view_config = TabConfigView()
        
        self.stacked_widget.addWidget(self.view_plan)
        self.stacked_widget.addWidget(self.view_category)
        self.stacked_widget.addWidget(self.view_config)
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget, 1)
        
        self.btn_nav_plan.clicked.connect(lambda: self.switch_tab(0))
        self.btn_nav_category.clicked.connect(lambda: self.switch_tab(1))
        self.btn_nav_config.clicked.connect(lambda: self.switch_tab(2))
        
    def switch_tab(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.btn_nav_plan.setChecked(index == 0)
        self.btn_nav_category.setChecked(index == 1)
        self.btn_nav_config.setChecked(index == 2)