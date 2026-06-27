from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QGroupBox, 
                               QFormLayout, QTimeEdit, QPushButton, 
                               QSpinBox, QScrollArea, QMessageBox, QHBoxLayout)
from PySide6.QtCore import QTime, Qt
import config.app_config as cfg

class SettingTabWidget(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.time_fields = {}
        self.deadline_inputs = {}
        
        self.setStyleSheet("""
            QPushButton { 
                background-color: #3498db; color: white; border-radius: 5px; 
                font-weight: bold; padding: 10px;
            }
            QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }
            QPushButton:hover:!disabled { background-color: #2980b9; }
            QGroupBox { font-weight: bold; margin-top: 10px; border: 1px solid #dcdcdc; border-radius: 5px; padding: 10px; }
        """)
        
        self.init_ui()
        self.load_config_to_ui()
        self.btn_save.setEnabled(False) # Mặc định disable khi vừa load

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(cfg.TAB_BAR_STYLE)

        # --- TAB 1: THỜI GIAN ---
        tab_time = QWidget()
        time_layout = QVBoxLayout(tab_time)
        box_work = QGroupBox("🕒 Giờ hành chính")
        form_work = QFormLayout(box_work)
        
        for label, key, default in [("Sáng bắt đầu", "am_start", QTime(7, 0)), 
                                    ("Sáng kết thúc", "am_end", QTime(11, 0)),
                                    ("Chiều bắt đầu", "pm_start", QTime(14, 0)), 
                                    ("Chiều kết thúc", "pm_end", QTime(16, 30))]:
            te = QTimeEdit(); te.setDisplayFormat("HH:mm"); te.setTime(default); te.setFixedSize(100, 30)
            te.timeChanged.connect(self.check_changes) # Theo dõi thay đổi
            form_work.addRow(f"{label}:", te)
            self.time_fields[key] = te
        
        box_ot = QGroupBox("🌙 Giờ tăng ca")
        form_ot = QFormLayout(box_ot)
        for label, key, default in [("OT bắt đầu", "ot_start", QTime(17, 30)),
                                    ("OT kết thúc", "ot_end", QTime(19, 30))]:
            te = QTimeEdit(); te.setDisplayFormat("HH:mm"); te.setTime(default); te.setFixedSize(100, 30)
            te.timeChanged.connect(self.check_changes) # Theo dõi thay đổi
            form_ot.addRow(f"{label}:", te)
            self.time_fields[key] = te

        time_layout.addWidget(box_work); time_layout.addWidget(box_ot); time_layout.addStretch()
        self.tab_widget.addTab(tab_time, "⏰ Thời gian làm việc")

        # --- TAB 2: THỜI HẠN PHIẾU ---
        self.tab_deadline = QWidget()
        self.d_layout = QVBoxLayout(self.tab_deadline)
        
        # Nút cập nhật bên phải
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        btn_refresh = QPushButton("🔄 Cập nhật từ file")
        btn_refresh.clicked.connect(self.refresh_deadline_ui)
        header_layout.addWidget(btn_refresh)
        self.d_layout.addLayout(header_layout)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.form_deadline = QFormLayout(self.container)
        self.scroll.setWidget(self.container)
        self.d_layout.addWidget(self.scroll)
        
        self.tab_widget.addTab(self.tab_deadline, "📅 Số ngày theo phiếu")
        main_layout.addWidget(self.tab_widget)
        
        # --- NÚT LƯU CỐ ĐỊNH GÓC PHẢI ---
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        self.btn_save = QPushButton("💾 Lưu cấu hình hệ thống")
        self.btn_save.setFixedWidth(200); self.btn_save.setMinimumHeight(40)
        self.btn_save.setStyleSheet("background-color: #FFD700; color: black; font-weight: bold; border-radius: 4px;")
        self.btn_save.clicked.connect(self.save_all_settings)
        footer_layout.addWidget(self.btn_save)
        main_layout.addLayout(footer_layout)

    def check_changes(self):
        """Kiểm tra xem dữ liệu UI có khác trong Model không để enable nút Lưu."""
        is_changed = False
        # So sánh thời gian
        for key, field in self.time_fields.items():
            if field.time().toString("HH:mm") != self.model.get_setting(f"time_{key}"):
                is_changed = True
        # So sánh deadlines
        for name, spin in self.deadline_inputs.items():
            if spin.value() != int(self.model.get_setting(f"deadline_{name}", "0")):
                is_changed = True
        
        self.btn_save.setEnabled(is_changed)

    def refresh_deadline_ui(self):
        """Xóa cũ, load lại danh sách phiếu và gắn signal theo dõi thay đổi."""
        for i in reversed(range(self.form_deadline.count())): 
            self.form_deadline.itemAt(i).widget().deleteLater()
            
        self.deadline_inputs = {}
        phieu_list = self.model.get_all_phieu_names()
        
        for p in phieu_list:
            spin = QSpinBox(); spin.setRange(0, 365); spin.setSuffix(" ngày"); spin.setFixedSize(150, 35)
            spin.setValue(int(self.model.get_setting(f"deadline_{p}", "0")))
            spin.valueChanged.connect(self.check_changes) # Theo dõi thay đổi số ngày
            self.form_deadline.addRow(f"📄 {p}:", spin)
            self.deadline_inputs[p] = spin
        
        self.check_changes() # Kiểm tra lại trạng thái sau khi refresh

    # def save_all_settings(self):
    #     for key, field in self.time_fields.items():
    #         self.model.save_setting(f"time_{key}", field.time().toString("HH:mm"))
    #     for name, spin in self.deadline_inputs.items():
    #         self.model.save_setting(f"deadline_{name}", spin.value())
            
    #     # QMessageBox.information(self, "Thành công", "Đã lưu cấu hình!")
    #     self.btn_save.setEnabled(False) # Tắt nút sau khi lưu

    def save_all_settings(self):
        try:
            for key, field in self.time_fields.items():
                self.model.save_setting(f"time_{key}", field.time().toString("HH:mm"))
            for name, spin in self.deadline_inputs.items():
                self.model.save_setting(f"deadline_{name}", spin.value())
            
            self.btn_save.setEnabled(False)
            return True # Trả về True nếu lưu thành công
        except Exception as e:
            print(f"Lỗi lưu cấu hình: {e}")
            return False

    def load_config_to_ui(self):
        for key in self.time_fields:
            val = self.model.get_setting(f"time_{key}")
            if val: self.time_fields[key].setTime(QTime.fromString(val, "HH:mm"))
        self.refresh_deadline_ui()