from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QLineEdit, QComboBox, QLabel, QHBoxLayout, QListWidget, QMessageBox
import config.app_config as cfg

class GroupMachineTabWidget(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        layout = QVBoxLayout(self)
        
        # 1. Khu vực thêm nhóm mới
        box_g = QGroupBox("Cấu hình Nhóm")
        inner_g = QHBoxLayout(box_g)
        self.txt_new_group = QLineEdit()
        self.btn_add_group = QPushButton("➕ Thêm Nhóm")
        inner_g.addWidget(self.txt_new_group); inner_g.addWidget(self.btn_add_group)
        
        # 2. Khu vực phân loại máy
        box_m = QGroupBox("Phân loại Máy (Chưa phân loại -> Nhóm chính)")
        inner_m = QVBoxLayout(box_m)
        
        inner_m.addWidget(QLabel("Danh sách máy chưa phân loại:"))
        self.list_unassigned = QListWidget() # Hiển thị máy nhóm "Chưa phân loại"
        inner_m.addWidget(self.list_unassigned)
        
        inner_m.addWidget(QLabel("Chọn nhóm đích:"))
        self.cb_group_select = QComboBox() # Load các nhóm thực tế từ DB
        inner_m.addWidget(self.cb_group_select)
        
        self.btn_assign = QPushButton("✅ Gán máy đã chọn vào nhóm")
        inner_m.addWidget(self.btn_assign)
        
        layout.addWidget(box_g); layout.addWidget(box_m)

        # Kết nối sự kiện
        self.btn_assign.clicked.connect(self.on_assign_clicked)
        self.refresh_ui()

    def refresh_ui(self):
        """Load lại danh sách máy chưa phân loại và danh sách nhóm"""
        # Load máy chưa phân loại (giả định dùng hàm query của model)
        # self.list_unassigned.addItems(self.model.get_devices_by_group("Chưa phân loại"))
        # Load nhóm
        # self.cb_group_select.addItems(self.model.get_all_group_names())
        pass

    def on_assign_clicked(self):
        current_item = self.list_unassigned.currentItem()
        if not current_item: return
        
        device_name = current_item.text()
        target_group = self.cb_group_select.currentText()
        
        # GỌI HÀM MOVE ĐÃ TẠO TRONG MODEL
        self.model.move_device_to_group(device_name, target_group)
        QMessageBox.information(self, "Thành công", f"Đã chuyển {device_name} sang {target_group}")
        self.refresh_ui()