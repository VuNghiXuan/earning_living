from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
import config.app_config as cfg
from views.components.custom_table import CustomTableWidget
from views.styles.table_styles import TABLE_WIDGET_STYLE

class NormTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Khối thao tác
        box = QGroupBox("Nạp định mức từ file Word")
        box.setStyleSheet(cfg.SETTING_GROUP_BOX_STYLE)
        inner = QVBoxLayout(box)
        
        self.btn_import_word = QPushButton("📁 Chọn file Word (.docx) và Nạp dữ liệu")
        self.btn_import_word.setStyleSheet(cfg.BTN_PLAN_STYLE)
        inner.addWidget(self.btn_import_word)
        
        # Cấu hình Bảng (Table)
        self.table_norms = CustomTableWidget()
        
        # Thiết lập 8 cột theo yêu cầu:
        # [0: Thiết bị, 1: Phiếu, 2: TT, 3: Nội dung, 4: Nhân công, 5: Thời gian, 6: Dụng cụ, 7: Ghi chú]
        self.table_norms.setColumnCount(8) 
        headers = ["TT", "Nội dung", "Nhân công", "Thời gian", "Dụng cụ", "Vật tư", "TCKT",  "Ghi chú", "Máy/Thiết bị", "Phiếu"]
        self.table_norms.setHorizontalHeaderLabels(headers)
        
        self.table_norms.apply_style(TABLE_WIDGET_STYLE)
        
        # Thiết lập header để người dùng có thể kéo dãn cột nếu cần
        header = self.table_norms.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        layout.addWidget(box)
        layout.addWidget(self.table_norms)

    def load_norms_to_table(self, data_list):
        self.table_norms.setRowCount(0)
        self.table_norms.setColumnCount(10)
        
        for row_idx, row_data in enumerate(data_list):
            # Đảm bảo row_data luôn có đủ 10 phần tử, nếu thiếu thì điền chuỗi rỗng
            while len(row_data) < 10:
                row_data.append("")
                
            self.table_norms.insertRow(row_idx)
            
            # Ánh xạ theo headers đã định nghĩa
            mapped_data = [
                row_data[2], row_data[3], row_data[4], row_data[5], 
                row_data[6], row_data[7], row_data[8], row_data[9], # TCKT, Vật tư, Kết quả
                row_data[0], row_data[1]
            ]
            
            for col_idx, value in enumerate(mapped_data):
                item = QTableWidgetItem(str(value) if value is not None else "")
                if col_idx == 0: item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table_norms.setItem(row_idx, col_idx, item)
                        
        # Tự động co giãn cột cho vừa khít nội dung
        self.table_norms.resizeColumnsToContents()
        print("[DEBUG] Nạp dữ liệu vào bảng hoàn tất.")