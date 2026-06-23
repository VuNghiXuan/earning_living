from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from .catagory_detail.norm_tab import NormTabWidget
from .catagory_detail.group_machine_tab import GroupMachineTabWidget
from .catagory_detail.ticket_tab import TicketTabWidget
import config.app_config as cfg

class CategoryTabWidget(QWidget):
    def __init__(self, model, parent=None): # Thêm model vào đây
        super().__init__(parent)
        self.model = model
        self.main_layout = QVBoxLayout(self)
        
        # Khởi tạo QTabWidget với tên biến là self.tabs để khớp với các dòng bên dưới
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(cfg.TAB_BAR_STYLE)
        
        # Khởi tạo các tab từ các file riêng biệt
        self.tab_norm = NormTabWidget()
        self.tab_group = GroupMachineTabWidget(self.model)
        # self.tab_ticket = TicketTabWidget()
        
        # Thêm các tab vào widget
        self.tabs.addTab(self.tab_norm, "📁 Quản Lý Định Mức")
        self.tabs.addTab(self.tab_group, "🏢 Quản Lý Nhóm & Máy")
        # self.tabs.addTab(self.tab_ticket, "🎫 Loại Phiếu Bảo Dưỡng")
        
        # Thêm TabWidget vào layout chính
        self.main_layout.addWidget(self.tabs)