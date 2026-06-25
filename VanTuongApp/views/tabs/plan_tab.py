from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTableWidget, QHeaderView
from views.components.plan_filter_widget import FilterWidget
from views.components.plan_table_component import PlanTable
import config.app_config as cfg

class PlanTabWidget(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.deadlines = {}  # Khởi tạo dict lưu deadline
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

        # Kết nối tín hiệu
        self.filter_widget.cb_phieu.currentIndexChanged.connect(self.on_phieu_changed)

    def load_initial_data(self):
        """Nạp dữ liệu từ Database vào các bộ lọc và tải cấu hình deadline."""
        
        # 1. Nạp danh sách loại phiếu
        phieu_items = []
        if hasattr(self.model, 'get_all_phieu_names'):
            self.filter_widget.cb_phieu.blockSignals(True)
            self.filter_widget.cb_phieu.clear()
            self.filter_widget.cb_phieu.addItem("-- Chọn phiếu BQDP --")
            
            raw_phieu = self.model.get_all_phieu_names() or []
            phieu_items = [str(item) for item in raw_phieu if item]
            self.filter_widget.cb_phieu.addItems(phieu_items)
            self.filter_widget.cb_phieu.blockSignals(False)
            
        # 2. Nạp danh mục nhóm (Norms)
        if hasattr(self.model, 'get_all_norms'):
            self.filter_widget.cb_group.blockSignals(True)
            self.filter_widget.cb_group.clear()
            self.filter_widget.cb_group.addItem("Tất cả các nhóm")
            
            raw_groups = self.model.get_all_norms() or []
            group_items = [str(item) for item in raw_groups if item]
            self.filter_widget.cb_group.addItems(group_items)
            self.filter_widget.cb_group.blockSignals(False)

        # 3. LẤY SỐ NGÀY THỰC HIỆN TỪ DATABASE (Bảng system_settings)
        if hasattr(self.model, 'get_setting'):
            for p in phieu_items:
                key = f"deadline_{p}"
                val = self.model.get_setting(key, "0") 
                try:
                    self.deadlines[p] = int(val)
                except ValueError:
                    self.deadlines[p] = 0
            # print(f"Đã load deadlines: {self.deadlines}")

    def on_phieu_changed(self, index):
        """Xử lý khi thay đổi loại phiếu để cập nhật định mức vào spin_duration"""
        selected_phieu = self.filter_widget.cb_phieu.currentText()
        
        # Nếu chọn "Tất cả", có thể reset spin_duration về 0 hoặc giữ nguyên tùy ý bạn
        if selected_phieu == "-- Chọn phiếu BQDP----":
            # Ví dụ: reset về 0
            self.filter_widget.spin_duration.setValue(0)
            return

        # Cập nhật giá trị vào spin_duration từ dict đã load từ DB
        if selected_phieu in self.deadlines:
            days = self.deadlines[selected_phieu]
            
            # Cập nhật giá trị mà không kích hoạt sự kiện update_logic nhiều lần
            self.filter_widget.spin_duration.blockSignals(True)
            self.filter_widget.spin_duration.setValue(days)
            self.filter_widget.spin_duration.blockSignals(False)
            
            # Sau khi set giá trị, gọi update_logic để tính lại ngày kết thúc
            self.filter_widget.update_logic('duration')
            
            print(f"Đã cập nhật định mức '{selected_phieu}': {days} ngày")

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