from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import Qt
from config.mapping_config import NORMS_TABLE_CONFIG
from controllers.utils_mapper import map_row_to_dict

class CategoryController:
    def __init__(self, main_controller):
        self.main = main_controller
        # Truy cập đúng tab category trong giao diện
        self.view = main_controller.main_view.tab_category
        self.model = main_controller.model

        # Khởi tạo dữ liệu
        self.refresh_norms_table()
        
        # Kết nối sự kiện
        self.view.tab_group.btn_add_group.clicked.connect(self.add_group)
        # Nếu dùng logic 2 list, dùng connect tới các hàm move của view
        self.view.tab_group.btn_to_assigned.clicked.connect(self.view.tab_group.move_to_assigned)
        self.view.tab_group.btn_to_unassigned.clicked.connect(self.view.tab_group.move_to_unassigned)
        
        # Callback cho bảng định mức
        self.view.tab_norm.save_callback = self.handle_save_to_db
        self.view.tab_norm.btn_import_word.clicked.connect(self.handle_import_and_refresh)

    def handle_import_and_refresh(self):
        self.main.on_admin_import_clicked()
        self.refresh_norms_table()
        
    def refresh_norms_table(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor) 
        try:
            data = self.model.get_all_norms()
            # Đẩy dữ liệu đã load được sang View
            self.view.tab_norm.load_norms_to_table(data)
        except Exception as e:
            print(f"[ERROR] refresh_norms_table: {e}")
        finally:
            QApplication.restoreOverrideCursor()

    def handle_save_to_db(self, data_from_table):
        """
        Dữ liệu từ bảng đã được View gom lại theo thứ tự hiển thị hiện tại.
        Hàm này dùng mapper để map lại về đúng trường DB.
        """
        try:
            mapped_list = []
            for row in data_from_table:
                # map_row_to_dict giờ đã dùng cấu hình đúng của DB
                item = map_row_to_dict(row, NORMS_TABLE_CONFIG)
                
                # Ép kiểu dữ liệu an toàn
                item['workers'] = int(item.get('workers', 0)) if str(item.get('workers', '')).isdigit() else 0
                item['minutes'] = int(item.get('minutes', 0)) if str(item.get('minutes', '')).isdigit() else 0
                
                mapped_list.append(item)
            
            if mapped_list:
                if self.model.update_all_norms(mapped_list):
                    # QMessageBox.information(self.main, "Thành công", "Đã lưu dữ liệu định mức!")
                    self.refresh_norms_table()
                    return True
            return False
        except Exception as e:
            print(f"[ERROR] handle_save_to_db: {e}")
            QMessageBox.critical(self.main, "Lỗi", f"Không thể lưu: {str(e)}")
            return False
        
    def add_group(self):
        name = self.view.tab_group.txt_new_group.text().strip()
        if not name: return
        try:
            self.model.add_new_group(name)
            self.view.tab_group.txt_new_group.clear()
            self.main.refresh_group_dropdown()
            self.view.tab_group.refresh_ui() 
        except Exception as e:
            QMessageBox.critical(self.main, "Lỗi", f"Lỗi thêm nhóm: {str(e)}")