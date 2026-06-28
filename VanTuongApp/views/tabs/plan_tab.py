from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTableWidget, QPushButton, QMessageBox)
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
        
        # Gán header_label từ header widget vào bảng để populate_table có thể cập nhật
        # Giả định PlanHeaderWidget có thuộc tính hoặc phương thức cập nhật thông tin
        self.table.header_label = self.header.title_label 
        
        self.init_ui()
        self.load_initial_data()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(cfg.TAB_BAR_STYLE)
        
        # --- TAB 1 ---
        self.sub_tab_create = QWidget()
        create_layout = QVBoxLayout(self.sub_tab_create)
        
        # Thêm header lên trên cùng của layout
        create_layout.addWidget(self.filter_widget)
        create_layout.addWidget(self.header)
        create_layout.addWidget(self.table)
        
        # --- TAB 2 & 3 ---
        self.setup_history_tab()
        self.setup_stats_tab()
        
        self.tab_widget.addTab(self.sub_tab_create, "⚡ Lập kế hoạch")
        self.tab_widget.addTab(self.sub_tab_history, "📜 Lịch sử")
        self.tab_widget.addTab(self.sub_tab_stats, "📊 Thống kê")
        
        main_layout.addWidget(self.tab_widget)

        # KẾT NỐI SỰ KIỆN
        # self.filter_widget.cb_phieu.currentIndexChanged.connect(self.on_phieu_changed)
        # self.filter_widget.cb_phieu.currentIndexChanged.connect(self.refresh_plan_table)
        # self.filter_widget.cb_group.currentIndexChanged.connect(self.refresh_plan_table)
        self.filter_widget.btn_tao_phieu.clicked.connect(self.on_tao_phieu_clicked)
        


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

    # def on_phieu_changed(self, index):
    #     selected_phieu = self.filter_widget.cb_phieu.currentText()
    #     if selected_phieu in self.deadlines:
    #         self.filter_widget.spin_duration.blockSignals(True)
    #         self.filter_widget.spin_duration.setValue(self.deadlines[selected_phieu])
    #         self.filter_widget.spin_duration.blockSignals(False)
    #         self.filter_widget.update_logic('duration')

    def on_tao_phieu_clicked(self):
        """Hàm này là trung gian, chỉ cần gọi hàm refresh là đủ."""
        print("Nút TẠO PHIẾU đã được nhấn, đang gọi hàm cập nhật...")
        self.refresh_plan_table()

    def refresh_plan_table(self):
        """Hàm này chỉ nhận 'self', không nhận đối số nào khác."""
        # 1. Lấy dữ liệu mới nhất từ filter
        filter_data = self.filter_widget.get_filter_results()
        
        # 2. Kiểm tra nhóm
        nhom = filter_data.get('nhom_thuc_hien')
        if nhom in ["-- Chọn nhóm --", "Tất cả các nhóm", ""]:
            QMessageBox.warning(
                self, 
                "Thông báo", 
                "Vui lòng chọn một nhóm thực hiện hợp lệ trước khi xem phiếu!"
            )
            return 

        try:
            # 3. Cập nhật header
            if hasattr(self, 'header'):
                self.header.update_info(filter_data)
            
            # 4. Lấy data từ model và cập nhật bảng
            tasks_data = self.model.get_tasks_by_filter(nhom, filter_data.get('so_phieu'))
            payload = {"tasks": tasks_data, "metadata": filter_data}
            self.table.populate_table(payload)
            print("Cập nhật bảng thành công.")
        except Exception as e:
            print(f"[ERROR] refresh_plan_table: {e}")


    # def refresh_plan_table(self):
    #     print('------------------------- vào được refresh_plan_table' )
    #     filter_data = self.filter_widget.get_filter_results()
        
    #     nhom = filter_data.get('nhom_thuc_hien')
    #     if nhom in ["-- Chọn nhóm --", "Tất cả các nhóm", ""]:
    #         return 

    #     try:
    #         # 1. CẬP NHẬT NHÓM LÊN HEADER
    #         # Giả sử bạn đã có phương thức update_info trong PlanHeaderWidget
    #         self.header.update_info(filter_data)

    #         # 2. Lấy dữ liệu và cập nhật bảng
    #         tasks_data = self.model.get_tasks_by_filter(nhom, filter_data.get('so_phieu'))
    #         payload = {"tasks": tasks_data, "metadata": filter_data}
    #         self.table.populate_table(payload)
    #     except Exception as e:
    #         print(f"[ERROR] refresh_plan_table: {e}")

    

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