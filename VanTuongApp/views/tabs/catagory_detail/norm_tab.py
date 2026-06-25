from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidgetItem, QLineEdit, QHBoxLayout, QMessageBox, QMenu, QHeaderView
from PySide6.QtCore import Qt
import config.app_config as cfg
from config.mapping_config import NORMS_TABLE_CONFIG
from views.components.custom_table import CustomTableWidget
from views.styles.table_styles import TABLE_WIDGET_STYLE

class NormTabWidget(QWidget):
    def __init__(self, save_callback=None):
        super().__init__()
        self.original_data = []
        self.save_callback = save_callback # Lưu hàm callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 1. Toolbar
        toolbar_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Tìm kiếm dữ liệu...")
        self.search_bar.textChanged.connect(self.filter_table)
        self.search_bar.setMinimumHeight(35)
        toolbar_layout.addWidget(self.search_bar)

        self.btn_add = QPushButton("➕ Thêm")
        self.btn_add.clicked.connect(self.add_empty_row)
        
        self.btn_delete = QPushButton("🗑️ Xóa")
        self.btn_delete.clicked.connect(self.delete_selected_row)
        
        self.btn_import_word = QPushButton("📁 Nạp từ Word")
        self.btn_import_word.setStyleSheet(cfg.BTN_PLAN_STYLE)
        
        for btn in [self.btn_add, self.btn_delete, self.btn_import_word]:
            btn.setMinimumHeight(35)
            toolbar_layout.addWidget(btn)
        layout.addLayout(toolbar_layout)
        
        # 2. Cấu hình Bảng
        self.table_norms = CustomTableWidget()
        # self.table_norms.setColumnCount(11) 
        self.set_headers() # Hàm thiết lập tên cột
        self.table_norms.apply_style(TABLE_WIDGET_STYLE)
        
        self.table_norms.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_norms.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.table_norms)

        # 3. Footer
        footer_layout = QHBoxLayout()
        # self.btn_cancel = QPushButton("↩️ Hủy thay đổi")
        # self.btn_cancel.clicked.connect(self.reload_data)
        self.btn_save = QPushButton("💾 LƯU DỮ LIỆU")
        self.btn_save.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; height: 40px;")
        self.btn_save.clicked.connect(self.save_to_database)
        
        footer_layout.addStretch()
        # footer_layout.addWidget(self.btn_cancel)
        footer_layout.addWidget(self.btn_save)
        layout.addLayout(footer_layout)

    def set_headers(self):
        """
        Thiết lập tên cột tự động dựa trên cấu hình trong NORMS_TABLE_CONFIG.
        Đảm bảo tính đồng bộ giữa UI và cấu trúc dữ liệu.
        """
        try:
            # 1. Trích xuất thông tin cấu hình cột
            cols = NORMS_TABLE_CONFIG.get("columns", {})
            
            # 2. Tạo danh sách header theo đúng thứ tự index
            # Số lượng cột = tổng số phần tử trong cấu hình
            num_cols = len(cols)
            headers = [None] * num_cols
            
            for key, info in cols.items():
                idx = info.get("idx")
                label = info.get("label")
                if idx is not None and idx < num_cols:
                    headers[idx] = label
            
            # 3. Cập nhật bảng
            self.table_norms.setColumnCount(num_cols)
            self.table_norms.setHorizontalHeaderLabels(headers)
            
        except Exception as e:
            print(f"[ERROR] Không thể thiết lập header từ config: {e}")
            # Dự phòng: Thiết lập mặc định nếu config bị lỗi
            default_headers = ["Máy/Thiết bị", "Phiếu bảo dưỡng", "TT", "Nội dung", "Nhân công", "Thời gian", "Dụng cụ", 
                               "Vật tư", "TCKT", "Kết quả" ] #, "Phiếu công nghệ"
            self.table_norms.setColumnCount(len(default_headers))
            self.table_norms.setHorizontalHeaderLabels(default_headers)

    def load_norms_to_table(self, data_list):
        self.table_norms.setRowCount(0)
        self.set_headers()
        
        cols_config = NORMS_TABLE_CONFIG["columns"]
        
        for row_idx, row_data in enumerate(data_list):
            self.table_norms.insertRow(row_idx)
            
            # Duyệt qua từng cột trong cấu hình để điền dữ liệu
            for field_key, info in cols_config.items():
                ui_idx = info.get("idx")
                
                # Giả sử row_data là list, và thứ tự trong list khớp với thứ tự khai báo trong config
                # Nếu row_data là list theo thứ tự 0,1,2,3... thì bạn cần biết db_index
                # Ở đây mình giả định bạn lấy theo thứ tự của config:
                val = row_data[ui_idx] if ui_idx < len(row_data) else ""
                
                item = QTableWidgetItem(str(val))
                if ui_idx == 0: item.setTextAlignment(Qt.AlignCenter)
                self.table_norms.setItem(row_idx, ui_idx, item)
        
        self.table_norms.resizeColumnsToContents()

    # --- CÁC HÀM KHÁC GIỮ NGUYÊN ---
    def show_context_menu(self, position):
        menu = QMenu()
        actions = {"add": menu.addAction("➕ Thêm dòng mới"), "del": menu.addAction("🗑️ Xóa dòng chọn"), "edit": menu.addAction("✏️ Chỉnh sửa")}
        action = menu.exec(self.table_norms.viewport().mapToGlobal(position))
        if action == actions["add"]: self.add_empty_row()
        elif action == actions["del"]: self.delete_selected_row()
        elif action == actions["edit"]: self.table_norms.editItem(self.table_norms.currentItem())

    def add_empty_row(self):
        row = self.table_norms.rowCount()
        self.table_norms.insertRow(row)
        for col in range(self.table_norms.columnCount()):
            item = QTableWidgetItem("")
            item.setFlags(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.table_norms.setItem(row, col, item)
           
    def delete_selected_row(self):
        for row in sorted(set(idx.row() for idx in self.table_norms.selectedIndexes()), reverse=True):
            self.table_norms.removeRow(row)

    def save_to_database(self):
        # 1. Thu thập dữ liệu từ bảng
        current_data = []
        col_count = self.table_norms.columnCount()
        for r in range(self.table_norms.rowCount()):
            row_data = [self.table_norms.item(r, c).text() if self.table_norms.item(r, c) else "" for c in range(col_count)]
            current_data.append(row_data)

        # 2. Gọi hàm callback đã truyền vào để xử lý lưu DB
        if self.save_callback:
            success = self.save_callback(current_data)
            if success:
                self.original_data = current_data
                QMessageBox.information(self, "Thành công", "Đã lưu thay đổi vào cơ sở dữ liệu!")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể lưu vào cơ sở dữ liệu.")
        else:
            QMessageBox.warning(self, "Thông báo", "Chưa cấu hình hàm lưu DB!")

    def reload_data(self):
        self.load_norms_to_table(self.original_data)

    def filter_table(self, text):
        filter_text = text.lower()
        col_count = self.table_norms.columnCount()
        for row in range(self.table_norms.rowCount()):
            match = any(filter_text in (self.table_norms.item(row, col).text().lower() if self.table_norms.item(row, col) else "") for col in range(col_count))
            self.table_norms.setRowHidden(row, not match)