from PySide6.QtWidgets import QMessageBox

class CategoryController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.view = main_controller.main_view.tab_category
        self.model = main_controller.model

        # Gọi nạp dữ liệu ngay khi khởi tạo để bảng không bị trống
        self.refresh_norms_table()
        
        # 1. Kết nối tín hiệu cho Nhóm
        self.view.tab_group.btn_add_group.clicked.connect(self.add_group)
        
        # 2. Kết nối tín hiệu cho Gán máy (sửa lỗi btn_add_machine -> btn_assign)
        self.view.tab_group.btn_assign.clicked.connect(self.assign_machine)
        
        # 3. Kết nối tín hiệu khác
        self.view.tab_norm.btn_import_word.clicked.connect(self.handle_import_and_refresh)

    def handle_import_and_refresh(self):
        print("[DEBUG] Bắt đầu quá trình nạp và làm mới...")
        # 1. Gọi hàm nạp của main (nó sẽ ghi vào DB)
        self.main.on_admin_import_clicked()
        
        # 2. Sau khi nạp xong, bắt buộc load lại bảng định mức
        self.refresh_norms_table()
        print("[DEBUG] Đã nạp và làm mới bảng xong.")
        
    def add_group(self):
        name = self.view.tab_group.txt_new_group.text().strip()
        if not name:
            QMessageBox.warning(self.main, "Thông báo", "Vui lòng nhập tên nhóm!")
            return
        try:
            # Lưu ý: Đảm bảo model có hàm add_new_group
            self.model.add_new_group(name)
            QMessageBox.information(self.main, "Thành công", f"Đã thêm nhóm '{name}'!")
            self.view.tab_group.txt_new_group.clear()
            self.main.refresh_group_dropdown()
            # Cập nhật lại cả combobox ở tab quản lý nhóm
            self.view.tab_group.refresh_ui() 
        except Exception as e:
            QMessageBox.critical(self.main, "Lỗi", f"Không thể thêm nhóm: {str(e)}")

    def refresh_norms_table(self):
        """Hàm này làm mới bảng định mức và cập nhật giao diện"""
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt # Cần import Qt để sử dụng WaitCursor
        
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor) 
        try:
            data = self.model.get_all_norms()
            self.view.tab_norm.load_norms_to_table(data)
        except Exception as e:
            print(f"[ERROR] refresh_norms_table: {e}")
        finally:
            QApplication.restoreOverrideCursor()


    def assign_machine(self):
        """Logic gán máy từ danh sách 'Chưa phân loại' vào nhóm đích"""
        current_item = self.view.tab_group.list_unassigned.currentItem()
        if not current_item:
            QMessageBox.warning(self.main, "Thông báo", "Vui lòng chọn máy trong danh sách!")
            return
            
        m_name = current_item.text()
        g_name = self.view.tab_group.cb_group_select.currentText()
        
        if not g_name:
            QMessageBox.warning(self.main, "Thông báo", "Vui lòng chọn nhóm đích!")
            return
            
        try:
            # Gọi hàm move_device_to_group đã tạo trong Model
            self.model.move_device_to_group(m_name, g_name)
            QMessageBox.information(self.main, "Thành công", f"Đã gán máy '{m_name}' vào nhóm '{g_name}'!")
            
            # Cập nhật lại giao diện sau khi gán
            self.view.tab_group.refresh_ui()
            self.main.refresh_group_dropdown()
            
        except Exception as e:
            QMessageBox.critical(self.main, "Lỗi", f"Không thể gán máy: {str(e)}")