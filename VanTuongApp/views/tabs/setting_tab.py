import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, 
                               QGroupBox, QFormLayout, QLabel, QTimeEdit, 
                               QPushButton, QSpinBox, QScrollArea, QMessageBox, QHBoxLayout)
from PySide6.QtCore import QTime, Qt
import config.app_config as cfg


class SettingTabWidget(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.time_fields = {}
        self.deadline_inputs = {}
        
        # Chỉ giữ lại CSS cho các nút bấm (an toàn)
        self.setStyleSheet("""
            QPushButton { 
                background-color: #3498db; color: white; 
                border-radius: 5px; font-weight: bold; padding: 10px;
            }
            QPushButton:hover { background-color: #2980b9; }
            QGroupBox { font-weight: bold; margin-top: 10px; border: 1px solid #dcdcdc; border-radius: 5px; padding: 10px; }
        """)
        
        self.init_ui()
        self.load_config_to_ui()

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
            te = QTimeEdit()
            te.setDisplayFormat("HH:mm")
            te.setTime(default)
            te.setFixedSize(100, 30)
            form_work.addRow(f"{label}:", te)
            self.time_fields[key] = te
        
        box_ot = QGroupBox("🌙 Giờ tăng ca")
        form_ot = QFormLayout(box_ot)
        for label, key, default in [("OT bắt đầu", "ot_start", QTime(17, 30)),
                                    ("OT kết thúc", "ot_end", QTime(19, 30))]:
            te = QTimeEdit()
            te.setDisplayFormat("HH:mm")
            te.setTime(default)
            te.setFixedSize(100, 30)
            form_ot.addRow(f"{label}:", te)
            self.time_fields[key] = te

        time_layout.addWidget(box_work)
        time_layout.addWidget(box_ot)
        time_layout.addStretch()
        self.tab_widget.addTab(tab_time, "⏰ Thời gian làm việc")

        # --- TAB 2: THỜI HẠN PHIẾU ---
        tab_deadline = QWidget()
        d_layout = QVBoxLayout(tab_deadline)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        form_deadline = QFormLayout(container)
        
        phieu_list = self.model.get_all_phieu_names()
        for p in phieu_list:
            spin = QSpinBox()
            spin.setRange(0, 365)
            spin.setSuffix(" ngày")
            spin.setFixedSize(150, 35)
            
            form_deadline.addRow(f"📄 {p}:", spin)
            self.deadline_inputs[p] = spin
            
        scroll.setWidget(container)
        d_layout.addWidget(scroll)
        self.tab_widget.addTab(tab_deadline, "📅 Số ngày theo phiếu")

        main_layout.addWidget(self.tab_widget)
        
        # Nút lưu
        # Footer cho nút lưu
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()  # Đẩy mọi thứ sang bên trái, dồn nút sang phải
        
        self.btn_save = QPushButton("💾 Lưu cấu hình hệ thống")
        self.btn_save.setFixedWidth(200) # Cố định chiều rộng để nút không quá dài
        self.btn_save.setMinimumHeight(40)
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #FFD700; 
                color: black;
                font-weight: bold;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover { background-color: #FFC107; }
        """)
        self.btn_save.clicked.connect(self.save_all_settings)
        
        footer_layout.addWidget(self.btn_save)
        
        # Thêm footer vào main_layout
        main_layout.addLayout(footer_layout)

    # ĐÃ KHÔI PHỤC CÁC HÀM XỬ LÝ DỮ LIỆU:
    def save_all_settings(self):
        """Lưu toàn bộ cấu hình vào model."""
        # Lưu giờ làm việc
        for key, field in self.time_fields.items():
            self.model.save_setting(f"time_{key}", field.time().toString("HH:mm"))
        
        # Lưu deadlines
        for name, spin in self.deadline_inputs.items():
            self.model.save_setting(f"deadline_{name}", spin.value())
            
        QMessageBox.information(self, "Thành công", "Đã lưu cấu hình vào hệ thống!")

    def load_config_to_ui(self):
        """Load dữ liệu từ model vào các ô nhập liệu."""
        # Load giờ
        for key in self.time_fields:
            val = self.model.get_setting(f"time_{key}")
            if val:
                self.time_fields[key].setTime(QTime.fromString(val, "HH:mm"))
                
        # Load deadlines
        for name, spin in self.deadline_inputs.items():
            val = self.model.get_setting(f"deadline_{name}", "0")
            spin.setValue(int(val))