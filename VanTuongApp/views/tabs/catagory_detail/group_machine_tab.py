from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QPushButton, 
                               QLineEdit, QComboBox, QLabel, QHBoxLayout, 
                               QListWidget, QAbstractItemView)
from PySide6.QtCore import Qt

class GroupMachineTabWidget(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.init_ui()
        self.refresh_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # 1. Cấu hình Nhóm
        box_g = QGroupBox("Cấu hình Nhóm")
        inner_g = QHBoxLayout(box_g)
        self.txt_new_group = QLineEdit()
        self.txt_new_group.setPlaceholderText("Nhập tên nhóm mới...")
        self.btn_add_group = QPushButton("➕ Thêm Nhóm")
        self.btn_add_group.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 5px;")
        inner_g.addWidget(self.txt_new_group)
        inner_g.addWidget(self.btn_add_group)
        layout.addWidget(box_g)

        # 2. Khu vực phân loại máy
        box_m = QGroupBox("Phân loại Máy")
        layout_m = QVBoxLayout(box_m)
        
        self.cb_group_select = QComboBox()
        self.cb_group_select.setStyleSheet("padding: 5px; font-weight: bold;")
        self.cb_group_select.currentIndexChanged.connect(self.refresh_ui)
        layout_m.addWidget(QLabel("Chọn nhóm đích để phân loại:"))
        layout_m.addWidget(self.cb_group_select)

        # Container cho 2 danh sách
        transfer_layout = QHBoxLayout()
        
        # Danh sách chưa chọn
        left_layout = QVBoxLayout()
        lbl_unassigned = QLabel("⚠️ CHƯA PHÂN LOẠI")
        lbl_unassigned.setStyleSheet("color: #D32F2F; font-weight: bold;")
        self.list_unassigned = QListWidget()
        self.list_unassigned.setSelectionMode(QAbstractItemView.ExtendedSelection)
        left_layout.addWidget(lbl_unassigned)
        left_layout.addWidget(self.list_unassigned)

        # Khu vực nút ở giữa
        btn_layout = QVBoxLayout()
        self.btn_to_assigned = QPushButton(">>")
        self.btn_to_unassigned = QPushButton("<<")
        self.btn_assign = self.btn_to_assigned # Alias giữ tương thích
        
        for btn in [self.btn_to_assigned, self.btn_to_unassigned]:
            btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; font-size: 16px; padding: 10px;")
            btn.setFixedWidth(50)
            
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_to_assigned)
        btn_layout.addWidget(self.btn_to_unassigned)
        btn_layout.addStretch()

        # Danh sách đã chọn
        right_layout = QVBoxLayout()
        lbl_assigned = QLabel("✅ ĐÃ GÁN VÀO NHÓM")
        lbl_assigned.setStyleSheet("color: #388E3C; font-weight: bold;")
        self.list_assigned = QListWidget()
        self.list_assigned.setSelectionMode(QAbstractItemView.ExtendedSelection)
        right_layout.addWidget(lbl_assigned)
        right_layout.addWidget(self.list_assigned)
        
        transfer_layout.addLayout(left_layout)
        transfer_layout.addLayout(btn_layout)
        transfer_layout.addLayout(right_layout)
        
        layout_m.addLayout(transfer_layout)
        layout.addWidget(box_m)

        # Kết nối nút
        self.btn_to_assigned.clicked.connect(self.move_to_assigned)
        self.btn_to_unassigned.clicked.connect(self.move_to_unassigned)

    def refresh_ui(self):
        target_group = self.cb_group_select.currentText()
        
        # Lưu index cũ để giữ trạng thái chọn sau khi refresh
        self.cb_group_select.blockSignals(True)
        current_idx = self.cb_group_select.currentIndex()
        self.cb_group_select.clear()
        self.cb_group_select.addItems(self.model.get_all_group_names())
        self.cb_group_select.setCurrentIndex(current_idx if current_idx != -1 else 0)
        self.cb_group_select.blockSignals(False)

        self.list_unassigned.clear()
        self.list_assigned.clear()
        self.list_unassigned.addItems(self.model.get_devices_by_group("Chưa phân loại"))
        if target_group:
            self.list_assigned.addItems(self.model.get_devices_by_group(target_group))

    def move_to_assigned(self):
        # Lấy danh sách các QListWidgetItem đã chọn
        selected_items = self.list_unassigned.selectedItems()
        if not selected_items: return
        
        group = self.cb_group_select.currentText()
        if not group or group == "Chưa phân loại": return

        # Thực hiện cập nhật Model
        for item in selected_items:
            device_name = item.text()
            self.model.move_device_to_group(device_name, group)
        
        # Làm mới UI
        self.refresh_ui()

    def move_to_unassigned(self):
        selected_items = self.list_assigned.selectedItems()
        if not selected_items: return
        
        for item in selected_items:
            device_name = item.text()
            self.model.move_device_to_group(device_name, "Chưa phân loại")
        
        self.refresh_ui()