from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QPushButton, 
                               QLineEdit, QComboBox, QLabel, QHBoxLayout, 
                               QListWidget, QAbstractItemView, QMessageBox, QInputDialog)
from PySide6.QtCore import Qt

class GroupMachineTabWidget(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        # Cờ tĩnh nằm ngoài các hàm, dùng chung cho tất cả instance
        is_locked = False
        self.init_ui()
        self.refresh_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Style dùng chung cho các nút
        btn_base_style = "font-weight: bold; padding: 6px 12px; border-radius: 4px;"
        
        # 1. Cấu hình Nhóm
        box_g = QGroupBox("Quản lý Nhóm")
        inner_g = QHBoxLayout(box_g)
        self.txt_new_group = QLineEdit()
        self.txt_new_group.setPlaceholderText("Nhập tên nhóm mới...")
        
        self.btn_add_group = QPushButton("➕ Thêm")
        self.btn_add_group.setStyleSheet(f"background-color: #4CAF50; color: white; {btn_base_style}")
        
        inner_g.addWidget(self.txt_new_group)
        inner_g.addWidget(self.btn_add_group)
        layout.addWidget(box_g)

        # 2. Khu vực phân loại máy
        box_m = QGroupBox("Phân loại máy vào nhóm")
        layout_m = QVBoxLayout(box_m)
        
        # Hàng chứa Combobox và nút chức năng (Đồng bộ chiều cao)
        row_action = QHBoxLayout()
        self.cb_group_select = QComboBox()
        self.cb_group_select.setStyleSheet("padding: 5px; font-weight: bold;")
        
        self.btn_edit_group = QPushButton("✏️ Sửa")
        self.btn_edit_group.setStyleSheet(f"background-color: #FF9800; color: white; {btn_base_style}")
        
        self.btn_del_group = QPushButton("🗑️ Xóa")
        self.btn_del_group.setStyleSheet(f"background-color: #F44336; color: white; {btn_base_style}")
        
        # Thiết lập độ rộng nút để không bị quá to
        for btn in [self.btn_edit_group, self.btn_del_group]:
            btn.setFixedWidth(70)
        
        row_action.addWidget(self.cb_group_select)
        row_action.addWidget(self.btn_edit_group)
        row_action.addWidget(self.btn_del_group)
        layout_m.addLayout(row_action)
        
        # Container cho 2 danh sách
        transfer_layout = QHBoxLayout()
        
        # Danh sách trái
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
        
        nav_style = "background-color: #2196F3; color: white; font-weight: bold; padding: 10px; border-radius: 4px;"
        for btn in [self.btn_to_assigned, self.btn_to_unassigned]:
            btn.setStyleSheet(nav_style)
            btn.setFixedWidth(50)
            
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_to_assigned)
        btn_layout.addWidget(self.btn_to_unassigned)
        btn_layout.addStretch()

        # Danh sách phải
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

        # Kết nối tín hiệu
        self.cb_group_select.currentIndexChanged.connect(self.refresh_ui)
        self.btn_add_group.clicked.connect(self.add_group)
        self.btn_edit_group.clicked.connect(self.edit_group)
        self.btn_del_group.clicked.connect(self.delete_group)
        self.btn_to_assigned.clicked.connect(self.move_to_assigned)
        self.btn_to_unassigned.clicked.connect(self.move_to_unassigned)
        

    def refresh_ui(self):
        # 1. Block signals để ngăn việc currentIndexChanged kích hoạt các hàm khác
        self.cb_group_select.blockSignals(True)
        
        target_group = self.cb_group_select.currentText()
        current_idx = self.cb_group_select.currentIndex()
        
        # 2. Cập nhật dữ liệu ComboBox
        self.cb_group_select.clear()
        self.cb_group_select.addItems(self.model.get_all_group_names())
        
        # Khôi phục index
        if current_idx >= 0 and current_idx < self.cb_group_select.count():
            self.cb_group_select.setCurrentIndex(current_idx)
        else:
            self.cb_group_select.setCurrentIndex(0)
            
        # 3. Mở lại signals sau khi đã xong việc thay đổi UI
        self.cb_group_select.blockSignals(False)

        # 4. Cập nhật danh sách (phần này không gây lỗi nhưng cần blocksignals ở trên)
        self.list_unassigned.clear()
        self.list_assigned.clear()
        self.list_unassigned.addItems(self.model.get_devices_by_group("Chưa phân loại"))
        
        # Chỉ lấy danh sách nếu nhóm hiện tại hợp lệ
        group_to_show = self.cb_group_select.currentText()
        if group_to_show and group_to_show != "Chưa phân loại":
            self.list_assigned.addItems(self.model.get_devices_by_group(group_to_show))

    def move_to_assigned(self):
        # THÊM ĐOẠN NÀY ĐỂ DEBUG
        # import inspect
        # caller = inspect.stack()[1].function
        # print(f"[DEBUG] move_to_assigned được gọi bởi: {caller}")
        # print(f"--- TRẠNG THÁI GỌI: {self.model} ---")

        # 1. Kiểm tra máy chọn
        selected_items = self.list_unassigned.selectedItems()
        if not selected_items:
            return 
        
        # 2. Kiểm tra nhóm
        if not self.validate_group_selection(silent=False):
            print("[DEBUG] validate_group_selection trả về False")
            return
        
        # 3. Thực hiện gán
        group = self.cb_group_select.currentText()
        print(f"[DEBUG] Thực hiện gán máy vào nhóm: {group}")
        for item in selected_items:
            self.model.move_device_to_group(item.text(), group)
        
        self.refresh_ui()

    def move_to_unassigned(self):
        selected_items = self.list_assigned.selectedItems()
        if not selected_items: return
        
        for item in selected_items:
            device_name = item.text()
            self.model.move_device_to_group(device_name, "Chưa phân loại")
        
        self.refresh_ui()
    
    def validate_group_selection(self, silent=False):
        """
        Nếu silent=True: Chỉ kiểm tra logic, không hiện MessageBox.
        Nếu silent=False: Hiện MessageBox khi có lỗi.
        """
        
        
        current_text = self.cb_group_select.currentText()
        
        if self.cb_group_select.count() == 0:
            if not silent:
                QMessageBox.warning(self, "Thông báo", "Bạn chưa tạo nhóm nào! Hãy tạo nhóm trước khi bố trí máy.")
            return False
            
        if current_text == "Chưa phân loại":
            if not silent:
                QMessageBox.critical(self, "Lỗi phân loại", 
                                     "Vui lòng chọn một nhóm đích hợp lệ để gán máy.")
            return False
            
        return True

    def add_group(self):
        name = self.txt_new_group.text().strip()
        if not name:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập tên nhóm!")
            return
            
        # Gọi đúng hàm đã thống nhất
        self.model.add_new_group(name) 
        
        self.txt_new_group.clear()
        self.refresh_ui()

    def edit_group(self):
        old_name = self.cb_group_select.currentText()
        if old_name == "Chưa phân loại": return
        
        new_name, ok = QInputDialog.getText(self, "Sửa tên nhóm", "Nhập tên mới:", text=old_name)
        if ok and new_name and new_name != old_name:
            self.model.rename_group(old_name, new_name) # Giả định model có hàm này
            self.refresh_ui()

    def delete_group(self):
        group_name = self.cb_group_select.currentText()
        if group_name == "Chưa phân loại": return
        
        reply = QMessageBox.question(self, "Xóa nhóm", f"Bạn có chắc muốn xóa nhóm '{group_name}'?\nCác máy trong nhóm sẽ trở về 'Chưa phân loại'.",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.model.delete_group(group_name) # Giả định model có hàm này
            self.refresh_ui()