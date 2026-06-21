from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class TabConfigView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        layout.addWidget(QLabel("<h2>CẤU HÌNH KHUNG GIỜ LÀM VIỆC HÀNH CHÍNH</h2>"))
        
        # Buổi sáng
        h1 = QHBoxLayout()
        self.txt_m_start = QLineEdit("07:00")
        self.txt_m_end = QLineEdit("11:30")
        h1.addWidget(QLabel("Ca Sáng - Bắt đầu (hh:mm):"))
        h1.addWidget(self.txt_m_start)
        h1.addWidget(QLabel("Kết thúc (hh:mm):"))
        h1.addWidget(self.txt_m_end)
        layout.addLayout(h1)
        
        # Buổi chiều
        h2 = QHBoxLayout()
        self.txt_a_start = QLineEdit("13:30")
        self.txt_a_end = QLineEdit("17:00")  # Thêm ô nhập giờ kết thúc chiều
        h2.addWidget(QLabel("Ca Chiều - Bắt đầu (hh:mm):"))
        h2.addWidget(self.txt_a_start)
        h2.addWidget(QLabel("Kết thúc (hh:mm):"))
        h2.addWidget(self.txt_a_end)
        layout.addLayout(h2)
        
        # Nút lưu
        self.btn_save = QPushButton("LƯU CẤU HÌNH THỜI GIAN")
        self.btn_save.setStyleSheet("background-color: #0078D4; color: white; font-weight: bold; padding: 10px; max-width: 250px; border-radius: 0px;")
        layout.addWidget(self.btn_save)
        layout.addStretch()