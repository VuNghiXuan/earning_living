from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTableWidget, QHeaderView, QTableWidgetItem
from views.components.plan_filter_widget import FilterWidget
from views.components.plan_table_component import PlanTable
from views.components.header_table import PlanHeaderWidget

import config.app_config as cfg
 

class PlanTabWidget(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.deadlines = {}
        
        # Khởi tạo các thành phần
        self.header = PlanHeaderWidget()
        self.filter_widget = FilterWidget()
        self.table = PlanTable(db=self.model)
        
        self.init_ui()
        self.load_initial_data()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(cfg.TAB_BAR_STYLE)
        
        # --- TAB 1 ---
        self.sub_tab_create = QWidget()
        create_layout = QVBoxLayout(self.sub_tab_create)
        
        create_layout.addWidget(self.filter_widget)
        create_layout.addWidget(self.table)
        
        # --- TAB 2 & 3 ---
        self.setup_history_tab()
        self.setup_stats_tab()
        
        self.tab_widget.addTab(self.sub_tab_create, "⚡ Lập kế hoạch")
        self.tab_widget.addTab(self.sub_tab_history, "📜 Lịch sử")
        self.tab_widget.addTab(self.sub_tab_stats, "📊 Thống kê")
        main_layout.addWidget(self.tab_widget)

        # KẾT NỐI SỰ KIỆN TẠI ĐÂY
        # Khi bộ lọc thay đổi, vừa cập nhật định mức vừa cập nhật bảng
        self.filter_widget.cb_phieu.currentIndexChanged.connect(self.on_phieu_changed)
        self.filter_widget.cb_phieu.currentIndexChanged.connect(self.refresh_plan_table)
        self.filter_widget.cb_group.currentIndexChanged.connect(self.refresh_plan_table)

    def load_initial_data(self):
        """Nạp dữ liệu từ Database vào bộ lọc."""
        # Nạp tên phiếu
        if hasattr(self.model, 'get_all_phieu_names'):
            phieu_items = self.model.get_all_phieu_names() or []
            self.filter_widget.cb_phieu.blockSignals(True)
            self.filter_widget.cb_phieu.clear()
            self.filter_widget.cb_phieu.addItem("-- Chọn phiếu BQDP --")
            self.filter_widget.cb_phieu.addItems([str(i) for i in phieu_items if i])
            self.filter_widget.cb_phieu.blockSignals(False)
            
            # Load deadlines
            for p in phieu_items:
                val = self.model.get_setting(f"deadline_{p}", "0")
                self.deadlines[str(p)] = int(val) if val.isdigit() else 0

        # Nạp danh mục nhóm
        if hasattr(self.model, 'get_all_norms'):
            groups = self.model.get_all_norms() or []
            self.filter_widget.cb_group.blockSignals(True)
            self.filter_widget.cb_group.clear()
            self.filter_widget.cb_group.addItem("Tất cả các nhóm")
            self.filter_widget.cb_group.addItems([str(g) for g in groups if g])
            self.filter_widget.cb_group.blockSignals(False)

    def on_phieu_changed(self, index):
        """Cập nhật số ngày thực hiện khi chọn phiếu."""
        selected_phieu = self.filter_widget.cb_phieu.currentText()
        if selected_phieu in self.deadlines:
            self.filter_widget.spin_duration.blockSignals(True)
            self.filter_widget.spin_duration.setValue(self.deadlines[selected_phieu])
            self.filter_widget.spin_duration.blockSignals(False)
            self.filter_widget.update_logic('duration')

    # def refresh_plan_table(self):
    #     """Lấy dữ liệu từ Model và đổ vào bảng."""
    #     phieu = self.filter_widget.cb_phieu.currentText()
    #     group = self.filter_widget.cb_group.currentText()
        
    #     # Xử lý giá trị mặc định cho Model
    #     phieu_val = phieu if phieu != "-- Chọn phiếu BQDP --" else None
    #     group_val = group if group != "Tất cả các nhóm" else None
        
    #     try:
    #         data = self.model.get_tasks_by_filter(group_val, phieu_val)
    #         self.table.populate_table(data)
    #     except Exception as e:
    #         print(f"[ERROR] Không thể refresh bảng kế hoạch: {e}")

    def refresh_plan_table(self):
        # Lấy dữ liệu filter hiện tại
        filter_data = self.filter_widget.get_filter_results()
        
        # Kiểm tra: Nếu nhóm là mặc định thì không làm gì cả
        nhom = filter_data.get('nhom_thuc_hien')
        if nhom in ["-- Chọn nhóm --", "Tất cả các nhóm", ""]:
            print("Người dùng chưa chọn nhóm hợp lệ, bỏ qua cập nhật.")
            return 

        # Nếu đã chọn nhóm -> Tiến hành cập nhật
        try:
            tasks_data = self.model.get_tasks_by_filter(nhom, filter_data.get('so_phieu'))
            payload = {"tasks": tasks_data, "metadata": filter_data}
            self.table.populate_table(payload)
        except Exception as e:
            print(f"Lỗi: {e}")



    def setup_history_tab(self):
        self.sub_tab_history = QWidget()
        layout = QVBoxLayout(self.sub_tab_history)
        self.table_history = QTableWidget(0, 4)
        self.table_history.setHorizontalHeaderLabels(["Ngày lập", "Thiết bị", "Loại phiếu", "File"])
        layout.addWidget(self.table_history)

    def setup_stats_tab(self):
        self.sub_tab_stats = QWidget()
        layout = QVBoxLayout(self.sub_tab_stats)
        self.table_stats = QTableWidget(0, 4)
        self.table_stats.setHorizontalHeaderLabels(["Năm", "Tổng giờ BD", "Số lượt", "Tỷ lệ (%)"])
        layout.addWidget(self.table_stats)