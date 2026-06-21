from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QListWidget, QMessageBox)

class TabCategoryView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # --- BÊN TRÁI: QUẢN LÝ NHÓM ---
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("<b>DANH SÁCH NHÓM THIẾT BỊ</b>"))
        self.list_groups = QListWidget()
        self.list_groups.setStyleSheet("border: 1px solid #D2D2D2; border-radius: 0px;")
        left_layout.addWidget(self.list_groups)
        
        h_group_input = QHBoxLayout()
        self.txt_group_name = QLineEdit()
        self.txt_group_name.setPlaceholderText("Nhập tên nhóm mới...")
        self.txt_group_name.setStyleSheet("padding: 5px; border-radius: 0px; border: 1px solid #D2D2D2;")
        self.btn_add_group = QPushButton("Thêm Nhóm")
        self.btn_add_group.setStyleSheet("background-color: #0078D4; color: white; padding: 5px 10px; border-radius:0px;")
        h_group_input.addWidget(self.txt_group_name)
        h_group_input.addWidget(self.btn_add_group)
        left_layout.addLayout(h_group_input)
        
        self.btn_delete_group = QPushButton("Xóa Nhóm Đang Chọn (Xóa hết cả máy bên trong)")
        self.btn_delete_group.setStyleSheet("background-color: #A80000; color: white; padding: 6px; font-weight: bold; border-radius:0px;")
        left_layout.addWidget(self.btn_delete_group)
        
        # --- BÊN PHẢI: QUẢN LÝ MÁY THUỘC NHÓM ---
        right_layout = QVBoxLayout()
        self.lbl_device_title = QLabel("<b>DANH SÁCH MÁY THUỘC NHÓM: TRỐNG</b>")
        right_layout.addWidget(self.lbl_device_title)
        self.list_devices = QListWidget()
        self.list_devices.setStyleSheet("border: 1px solid #D2D2D2; border-radius: 0px;")
        right_layout.addWidget(self.list_devices)
        
        h_device_input = QHBoxLayout()
        self.txt_device_name = QLineEdit()
        self.txt_device_name.setPlaceholderText("Nhập tên trang bị máy móc mới...")
        self.txt_device_name.setStyleSheet("padding: 5px; border-radius: 0px; border: 1px solid #D2D2D2;")
        self.btn_add_device = QPushButton("Thêm Máy")
        self.btn_add_device.setStyleSheet("background-color: #107C41; color: white; padding: 5px 10px; border-radius:0px;")
        h_device_input.addWidget(self.txt_device_name)
        h_device_input.addWidget(self.btn_add_device)
        right_layout.addLayout(h_device_input)
        
        self.btn_delete_device = QPushButton("Bỏ Máy Khỏi Danh Mục")
        self.btn_delete_device.setStyleSheet("background-color: #A80000; color: white; padding: 6px; font-weight: bold; border-radius:0px;")
        right_layout.addWidget(self.btn_delete_device)
        
        # Ghép khung layout
        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 1)