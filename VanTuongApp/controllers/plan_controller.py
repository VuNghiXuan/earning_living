from PySide6.QtWidgets import QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from core.scheduler import calculate_timeline

class PlanController:
    """
    Bộ não điều phối: Kết nối tín hiệu View -> Model và cập nhật lại Timeline.
    """
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.current_tasks_data = [] 
        
        # Kết nối tín hiệu UI
        # self.view.btn_load.clicked.connect(self.load_data_to_grid)
        
    def load_data_to_grid(self):
        """
        Nạp dữ liệu từ Model và hiển thị lên bảng. 
        Xử lý linh hoạt trường hợp nhóm trống hoặc dữ liệu rỗng.
        """
        # 1. Thu thập tham số từ UI
        # Nếu combobox nhóm trống, mặc định là "Chưa phân loại" để không làm crash hệ thống
        group = self.view.cb_group.currentText()
        if not group or group.strip() == "":
            group = "Chưa phân loại"
            
        device = self.view.cb_device.currentText()
        cycle = self.view.cb_cycle.currentText()
        
        print(f"[DEBUG] Đang nạp dữ liệu: Group='{group}', Device='{device}', Cycle='{cycle}'")

        # 2. Lấy dữ liệu từ Model
        # Đảm bảo trả về list rỗng nếu không tìm thấy thay vì None
        self.current_tasks_data = self.model.get_tasks(group, device, cycle) or []
        
        print(f"[DEBUG] Số lượng bản ghi lấy được: {len(self.current_tasks_data)}")
        
        # 3. Reset bảng an toàn
        self.view.table.setRowCount(0)
        workers = str(self.view.sp_workers.value())
        
        # 4. Đổ dữ liệu lên lưới
        for row, task in enumerate(self.current_tasks_data):
            self.view.table.insertRow(row)
            
            # Tạo widget Checkbox nằm chính giữa cột 0
            chk_widget = QWidget()
            chk_layout = QHBoxLayout(chk_widget)
            chk_layout.setContentsMargins(5, 2, 5, 2)
            chk_layout.setAlignment(Qt.AlignCenter)
            
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            # Kết nối tín hiệu tính lại timeline khi thay đổi trạng thái
            checkbox.stateChanged.connect(self.recalculate_grid_timeline)
            
            chk_layout.addWidget(checkbox)
            self.view.table.setCellWidget(row, 0, chk_widget)
            
            # Gán giá trị vào các ô (sử dụng .get() để tránh lỗi KeyError)
            self.view.table.setItem(row, 1, QTableWidgetItem(str(task.get("tt", ""))))
            self.view.table.setItem(row, 2, QTableWidgetItem(str(task.get("name", ""))))
            self.view.table.setItem(row, 3, QTableWidgetItem(workers))
            self.view.table.setItem(row, 4, QTableWidgetItem("")) # Cột trống để recalculate điền
            self.view.table.setItem(row, 5, QTableWidgetItem(str(task.get("tool", ""))))
            self.view.table.setItem(row, 6, QTableWidgetItem(str(task.get("material", ""))))
            self.view.table.setItem(row, 7, QTableWidgetItem(str(task.get("tckt", ""))))
            
        # 5. Tính toán timeline ban đầu
        if self.current_tasks_data:
            print("[DEBUG] Đang tính toán timeline...")
            self.recalculate_grid_timeline()
        else:
            print("[DEBUG] Không có dữ liệu để tính timeline.")
            
        print("[DEBUG] Hoàn tất nạp dữ liệu vào bảng.")

    def recalculate_grid_timeline(self):
        active_tasks = []
        active_rows = []
        
        # Lọc các dòng đang được check
        for row in range(self.view.table.rowCount()):
            chk_widget = self.view.table.cellWidget(row, 0)
            if not chk_widget: continue
            
            checkbox = chk_widget.findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                active_tasks.append(self.current_tasks_data[row])
                active_rows.append(row)
            else:
                # Xóa dải giờ của dòng bị bỏ chọn
                if self.view.table.item(row, 4):
                    self.view.table.item(row, 4).setText("-")
        
        # Nếu có công việc được chọn, tính toán qua Core
        if active_tasks:
            time_ranges = calculate_timeline(active_tasks)
            
            # Cập nhật kết quả vào cột 4 (Cột dải giờ)
            for idx, row in enumerate(active_rows):
                if idx < len(time_ranges):
                    self.view.table.item(row, 4).setText(time_ranges[idx])