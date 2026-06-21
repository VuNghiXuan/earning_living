import sys
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox, QHBoxLayout, QCheckBox, QWidget, QTableWidgetItem
from views.main_window import MainWindow
from models.plan_model import PlanModel
from core.scheduler import calculate_timeline
from core.word_parser import parse_maintenance_word_file

class MainController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.current_raw_tasks = []
        
        # Khởi tạo dữ liệu ban đầu lên UI
        self.refresh_all_dropdowns()
        self.load_time_config_to_ui()
        self.refresh_category_lists()
        
        # KẾT NỐI SỰ KIỆN TAB LẬP KẾ HOẠCH
        self.view.view_plan.cb_group.currentTextChanged.connect(self.on_plan_group_changed)
        self.view.view_plan.btn_load.clicked.connect(self.on_btn_load_clicked)
        self.view.view_plan.btn_import_word.clicked.connect(self.on_admin_import_clicked)
        self.view.view_config.btn_save.clicked.connect(self.on_btn_save_config_clicked)
        
        # KẾT NỐI SỰ KIỆN TAB QUẢN LÝ DANH MỤC
        self.view.view_category.list_groups.currentTextChanged.connect(self.on_category_group_selected)
        self.view.view_category.btn_add_group.clicked.connect(self.on_btn_add_group_clicked)
        self.view.view_category.btn_delete_group.clicked.connect(self.on_btn_delete_group_clicked)
        self.view.view_category.btn_add_device.clicked.connect(self.on_btn_add_device_clicked)
        self.view.view_category.btn_delete_device.clicked.connect(self.on_btn_delete_device_clicked)

    # --- XỬ LÝ ĐỒNG BỘ BỘ LỌC VÀ CẤU HÌNH ---
    def refresh_all_dropdowns(self):
        """Làm mới toàn bộ ComboBox ở Tab Lập kế hoạch"""
        self.view.view_plan.cb_group.clear()
        groups = self.model.get_unique_groups()
        if groups:
            self.view.view_plan.cb_group.addItems(groups)
            self.on_plan_group_changed(groups[0])

    def on_plan_group_changed(self, group_name):
        self.view.view_plan.cb_device.clear()
        if group_name:
            devices = self.model.get_devices_by_group(group_name)
            self.view.view_plan.cb_device.addItems(devices)

    def load_time_config_to_ui(self):
        cfg = self.model.load_time_config()
        self.view.view_config.txt_m_start.setText(cfg.get("morning_start", "07:00"))
        self.view.view_config.txt_m_end.setText(cfg.get("morning_end", "11:30"))
        self.view.view_config.txt_a_start.setText(cfg.get("afternoon_start", "13:30"))
        self.view.view_config.txt_a_end.setText(cfg.get("afternoon_end", "17:00"))

    def on_btn_save_config_clicked(self):
        ms = self.view.view_config.txt_m_start.text()
        me = self.view.view_config.txt_m_end.text()
        as_ = self.view.view_config.txt_a_start.text()
        ae = self.view.view_config.txt_a_end.text()
        self.model.save_time_config(ms, me, as_, ae)
        QMessageBox.information(self.view, "Thành công", "Đã cập nhật khung giờ làm việc!")
        if self.current_raw_tasks:
            self.recalculate_timeline_on_grid()

    # --- XỬ LÝ ĐỘNG TRÊN TAB QUẢN LÝ DANH MỤC ---
    def refresh_category_lists(self):
        """Đổ lại dữ liệu cho ListWidget quản lý danh mục"""
        self.view.view_category.list_groups.clear()
        groups = self.model.get_unique_groups()
        self.view.view_category.list_groups.addItems(groups)
        self.view.view_category.list_devices.clear()

    def on_category_group_selected(self, group_name):
        self.view.view_category.list_devices.clear()
        if group_name:
            self.view.view_category.lbl_device_title.setText(f"<b>DANH SÁCH MÁY THUỘC NHÓM: {group_name.upper()}</b>")
            devices = self.model.get_devices_by_group(group_name)
            self.view.view_category.list_devices.addItems(devices)
        else:
            self.view.view_category.lbl_device_title.setText("<b>DANH SÁCH MÁY THUỘC NHÓM: TRỐNG</b>")

    def on_btn_add_group_clicked(self):
        name = self.view.view_category.txt_group_name.text().strip()
        if name:
            if self.model.add_group(name):
                self.view.view_category.txt_group_name.clear()
                self.refresh_category_lists()
                self.refresh_all_dropdowns() # Đồng bộ sang combo bộ lọc
            else:
                QMessageBox.warning(self.view, "Lỗi", "Tên nhóm này đã tồn tại rồi anh nhé!")

    def on_btn_delete_group_clicked(self):
        current_group = self.view.view_category.list_groups.currentItem()
        if current_group:
            group_name = current_group.text()
            ret = QMessageBox.question(self.view, "Xác nhận", f"Xóa nhóm '{group_name}' sẽ xóa sạch toàn bộ máy móc thuộc nhóm này. Anh chắc chắn chứ?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if ret == QMessageBox.StandardButton.Yes:
                self.model.delete_group(group_name)
                self.refresh_category_lists()
                self.refresh_all_dropdowns()

    def on_btn_add_device_clicked(self):
        current_group = self.view.view_category.list_groups.currentItem()
        device_name = self.view.view_category.txt_device_name.text().strip()
        if not current_group:
            QMessageBox.warning(self.view, "Chú ý", "Vui lòng tích chọn một Nhóm bên trái trước khi thêm máy!")
            return
        if device_name:
            if self.model.add_device(current_group.text(), device_name):
                self.view.view_category.txt_device_name.clear()
                self.on_category_group_selected(current_group.text())
                self.refresh_all_dropdowns()
            else:
                QMessageBox.warning(self.view, "Lỗi", "Máy này đã tồn tại trong hệ thống!")

    def on_btn_delete_device_clicked(self):
        current_group = self.view.view_category.list_groups.currentItem()
        current_device = self.view.view_category.list_devices.currentItem()
        if current_device and current_group:
            self.model.delete_device(current_device.text())
            self.on_category_group_selected(current_group.text())
            self.refresh_all_dropdowns()

    # --- TẢI VÀ TÍNH TOÁN LƯỚI ĐỊNH MỨC ---
    def on_admin_import_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Chọn File Định Mức Word", "", "Word Files (*.docx)")
        if file_path:
            group = self.view.view_plan.cb_group.currentText()
            data = parse_maintenance_word_file(file_path)
            if data:
                self.model.import_from_word_data(data, group)
                QMessageBox.information(self.view, "Thành công", "Đã nạp ma trận định mức vào SQLite vĩnh viễn!")
                self.refresh_all_dropdowns()
                self.refresh_category_lists()
            else:
                QMessageBox.warning(self.view, "Lỗi", "Cấu trúc bảng không đúng hoặc lỗi đọc file.")

    def on_btn_load_clicked(self):
        device = self.view.view_plan.cb_device.currentText()
        cycle = self.view.view_plan.cb_cycle.currentText()
        if not device:
            QMessageBox.warning(self.view, "Chú ý", "Chưa có thiết bị nào được chọn!")
            return
            
        self.current_raw_tasks = self.model.get_tasks(device, cycle)
        table = self.view.view_plan.table
        table.setRowCount(len(self.current_raw_tasks))
        workers = str(self.view.view_plan.sp_workers.value())
        
        for row, task in enumerate(self.current_raw_tasks):
            chk_widget = QWidget()
            chk_layout = QHBoxLayout(chk_widget)
            chk_layout.setContentsMargins(8, 0, 8, 0)
            checkbox = QCheckBox(task["tt"])
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self.recalculate_timeline_on_grid)
            chk_layout.addWidget(checkbox)
            table.setCellWidget(row, 0, chk_widget)
            
            table.setItem(row, 1, QTableWidgetItem(task["name"]))
            table.setItem(row, 2, QTableWidgetItem(workers))
            table.setItem(row, 3, QTableWidgetItem(""))
            table.setItem(row, 4, QTableWidgetItem(task["tool"]))
            table.setItem(row, 5, QTableWidgetItem(task["material"]))
            table.setItem(row, 6, QTableWidgetItem(task["tckt"]))
            
        self.recalculate_timeline_on_grid()

    def recalculate_timeline_on_grid(self):
        table = self.view.view_plan.table
        active_tasks = []
        active_rows = []
        
        for row in range(table.rowCount()):
            chk_widget = table.cellWidget(row, 0)
            checkbox = chk_widget.findChild(QCheckBox) if chk_widget else None
            if checkbox and checkbox.isChecked():
                active_tasks.append(self.current_raw_tasks[row])
                active_rows.append(row)
            else:
                if table.item(row, 3):
                    table.item(row, 3).setText("-")
                    
        cfg = self.model.load_time_config()
        time_ranges = calculate_timeline(
            active_tasks, 
            morning_start=cfg.get("morning_start"), morning_end=cfg.get("morning_end"), 
            afternoon_start=cfg.get("afternoon_start"), afternoon_end=cfg.get("afternoon_end")
        )
        
        for idx, row in enumerate(active_rows):
            if table.item(row, 3):
                table.item(row, 3).setText(time_ranges[idx])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = MainWindow()
    model = PlanModel()
    controller = MainController(view, model)
    view.showMaximized() # Đảm bảo bật phát full screen luôn
    sys.exit(app.exec())