from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTableWidget, QHeaderView
from views.components.plan_filter_widget import FilterWidget
from views.components.plan_table_component import PlanTable
import config.app_config as cfg

class PlanTabWidget(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.filter_widget = FilterWidget() # Sử dụng widget bộ lọc
        self.init_ui()
        self.load_initial_data()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(cfg.TAB_BAR_STYLE)
        
        # --- TAB 1 ---
        self.sub_tab_create = QWidget()
        create_layout = QVBoxLayout(self.sub_tab_create)
        
        create_layout.addWidget(self.filter_widget) # Đưa bộ lọc vào
        self.table = PlanTable()
        create_layout.addWidget(self.table)
        
        # --- TAB 2 & 3 ---
        self.setup_history_tab()
        self.setup_stats_tab()
        
        self.tab_widget.addTab(self.sub_tab_create, "⚡ Lập kế hoạch")
        self.tab_widget.addTab(self.sub_tab_history, "📜 Lịch sử")
        self.tab_widget.addTab(self.sub_tab_stats, "📊 Thống kê")
        main_layout.addWidget(self.tab_widget)

    def load_initial_data(self):
        # Nạp tên phiếu
        if hasattr(self.model, 'get_all_phieu_names'):
            raw_phieu = self.model.get_all_phieu_names() or []
            # Ép kiểu mỗi phần tử thành chuỗi để tránh lỗi Shiboken
            phieu_items = [str(item) for item in raw_phieu]
            self.filter_widget.cb_phieu.addItems(phieu_items)
            
        # Nạp danh mục nhóm
        if hasattr(self.model, 'get_all_norms'):
            raw_groups = self.model.get_all_norms() or []
            # Ép kiểu mỗi phần tử thành chuỗi
            group_items = [str(item) for item in raw_groups]
            self.filter_widget.cb_group.addItems(group_items)

    # ... các hàm setup_history_tab và setup_stats_tab giữ nguyên ...

    def setup_history_tab(self):
        self.sub_tab_history = QWidget()
        layout = QVBoxLayout(self.sub_tab_history)
        self.table_history = QTableWidget(0, 4)
        self.table_history.setHorizontalHeaderLabels(["Ngày lập", "Thiết bị", "Loại phiếu", "File"])
        self.table_history.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_history)

    def setup_stats_tab(self):
        self.sub_tab_stats = QWidget()
        layout = QVBoxLayout(self.sub_tab_stats)
        self.table_stats = QTableWidget(0, 4)
        self.table_stats.setHorizontalHeaderLabels(["Năm", "Tổng giờ BD", "Số lượt", "Tỷ lệ (%)"])
        self.table_stats.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_stats)

    # def load_initial_data(self):
    #     # Đảm bảo dùng đúng phương thức của model (ví dụ: get_all_norms thay vì get_all_groups)
    #     if hasattr(self.model, 'get_all_phieu_names'):
    #         self.cb_phieu.addItems(self.model.get_all_phieu_names())
    #     if hasattr(self.model, 'get_all_norms'):
    #         self.cb_group.addItems(self.model.get_all_norms())