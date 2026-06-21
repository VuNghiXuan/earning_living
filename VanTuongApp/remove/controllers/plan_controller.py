from PySide6.QtWidgets import QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from core.scheduler import calculate_timeline

class PlanController:
    """
    4. FILE: controllers/plan_controller.py (Bộ não điều phối kết nối MVC)
Xử lý bắt các sự kiện (Signals), tính toán lại dòng thời gian ngay khi người dùng bấm nạp hoặc tích/bỏ tích Checkbox trên lưới.
"""
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.current_tasks_data = [] # Lưu trữ data thô hiện tại
        
        # Kết nối sự kiện nút bấm nạp mẫu
        self.view.btn_load.clicked.connect(self.load_data_to_grid)
        
    def load_data_to_grid(self):
        group = self.view.cb_group.currentText()
        device = self.view.cb_device.currentText()
        cycle = self.view.cb_cycle.currentText()
        
        # 1. Gọi Model lấy danh sách đầu việc định mức gốc
        self.current_tasks_data = self.model.get_tasks(group, device, cycle)
        
        self.view.table.setRowCount(len(self.current_tasks_data))
        workers = str(self.view.sp_workers.value())
        
        # 2. Đổ dữ liệu lên lưới và gán Checkbox
        for row, task in enumerate(self.current_tasks_data):
            # Tạo widget Checkbox nằm chính giữa ô STT
            chk_widget = QWidget()
            chk_layout = QHBoxLayout(chk_widget)
            chk_layout.setContentsMargins(5, 0, 5, 0)
            checkbox = QCheckBox(task["tt"])
            checkbox.setChecked(True)
            # Phát tín hiệu tính lại giờ khi tích hoặc bỏ tích đầu việc
            checkbox.stateChanged.connect(self.recalculate_grid_timeline)
            chk_layout.addWidget(checkbox)
            self.view.table.setCellWidget(row, 0, chk_widget)
            
            # Đổ nội dung text
            self.view.table.setItem(row, 1, QTableWidgetItem(task["name"]))
            self.view.table.setItem(row, 2, QTableWidgetItem(workers))
            
            # Ô thời gian tạm thời để trống, tí nữa hàm recalculate sẽ điền dải giờ
            self.view.table.setItem(row, 3, QTableWidgetItem(""))
            
            self.view.table.setItem(row, 4, QTableWidgetItem(task["tool"]))
            self.view.table.setItem(row, 5, QTableWidgetItem(task["material"]))
            self.view.table.setItem(row, 6, QTableWidgetItem(task["tckt"]))
            
        # 3. Chạy thuật toán tính dải giờ cho toàn bộ lưới lần đầu
        self.recalculate_grid_timeline()

    def recalculate_grid_timeline(self):
        # Lọc danh sách các hàng đang được người dùng tích chọn thực hiện
        active_tasks = []
        active_rows = []
        
        for row in range(self.view.table.rowCount()):
            chk_widget = self.view.table.cellWidget(row, 0)
            checkbox = chk_widget.findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                active_tasks.append(self.current_tasks_data[row])
                active_rows.append(row)
            else:
                # Nếu bỏ tích thì xóa hiển thị dải giờ của dòng đó đi
                if self.view.table.item(row, 3):
                    self.view.table.item(row, 3).setText("-")
        
        # Gọi tầng core tính dải giờ nối tiếp
        time_ranges = calculate_timeline(active_tasks)
        
        # Đổ ngược dải giờ hh:mm mới tính lại lên giao diện các hàng active
        for idx, row in enumerate(active_rows):
            self.view.table.item(row, 3).setText(time_ranges[idx])