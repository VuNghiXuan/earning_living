import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from core.word_parser import parse_maintenance_word_file
from models.plan_model import PlanModel
from views.main_view import MainView
from controllers.category_controller import CategoryController
from controllers.plan_controller import PlanController
import config.app_config as cfg

class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Hệ Thống - {cfg.COMPANY_NAME}")
        self.model = PlanModel()
        self.main_view = MainView(self.model)
        self.setCentralWidget(self.main_view)
        
        # 1. Định nghĩa các shortcut để truy cập Tab nhanh (Sửa lỗi AttributeError)
        self.p_tab = self.main_view.tab_plan
        self.c_tab = self.main_view.tab_category
        self.s_tab = self.main_view.tab_setting
        
        # 2. Khởi tạo các controller con
        self.cat_ctrl = CategoryController(self)
        self.plan_ctrl = PlanController(self.p_tab, self.model)
        
        # 3. Kết nối sự kiện toàn cục
        # self.main_view.tab_setting.btn_save_config.clicked.connect(self.on_btn_save_config_clicked)
        self.main_view.tab_setting.btn_save.clicked.connect(self.on_btn_save_config_clicked)
        
        # Gọi khởi tạo ban đầu
        self.refresh_group_dropdown()

    def on_btn_save_config_clicked(self):
        s = self.main_view.tab_setting
        # Lấy dữ liệu từ dictionary time_fields đã được tối ưu trong bản trước
        am_s = s.time_fields['am_start'].time().toString("HH:mm")
        am_e = s.time_fields['am_end'].time().toString("HH:mm")
        
        # Bạn có thể gọi trực tiếp hàm lưu của SettingTabWidget để đồng bộ
        s.save_all_settings()
        
        # msg = f"Đã cập nhật cấu hình:\nSáng: {am_s} - {am_e}\n(Dữ liệu đã lưu vào config.json)"
        # QMessageBox.information(self, "Hệ thống", msg)

    def refresh_group_dropdown(self):
        """Đổ dữ liệu nhóm vào ComboBox"""
        if not hasattr(self, 'p_tab'): return
        
        self.p_tab.filter_widget.cb_group.blockSignals(True)
        self.p_tab.filter_widget.cb_group.clear()
        
        try:
            with self.model.get_connection() as conn:
                rows = conn.execute("SELECT group_name FROM groups").fetchall()
                for r in rows:
                    self.p_tab.filter_widget.cb_group.addItem(r["group_name"])
        except Exception as e:
            print(f"Lỗi refresh group: {e}")
        finally:
            self.p_tab.filter_widget.cb_group.blockSignals(False)
            # Tự động cập nhật danh sách thiết bị
            if self.p_tab.filter_widget.cb_group.count() > 0:
                self.on_group_changed(self.p_tab.filter_widget.cb_group.currentText())

    def on_group_changed(self, group_name):
        """Hàm xử lý thay đổi nhóm - nên nằm ở PlanController nếu muốn chuyên biệt"""
        # Logic cập nhật combobox thiết bị ở đây...
        pass

    def on_admin_import_clicked(self):
        # KHÔNG GỌI self.p_tab.filter_widget.cb_group.currentText() ĐỂ CHẶN NỮA
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn File", "", "Word Files (*.docx)")
        if not file_path: return

        try:
            parsed_data = parse_maintenance_word_file(file_path)
            # Truyền None hoặc chuỗi rỗng để Model tự hiểu là "Chưa phân loại"
            self.model.import_from_word_data(parsed_data, "", os.path.basename(file_path), file_path)
            
            QMessageBox.information(self, "Thành công", "Đã nạp file vào nhóm 'Chưa phân loại'!")
            self.refresh_group_dropdown()
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = MainController()
    controller.showMaximized()
    sys.exit(app.exec())