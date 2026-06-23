import json
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                               QGroupBox, QFormLayout, QLabel, QTimeEdit, 
                               QPushButton, QSpinBox, QScrollArea, QMessageBox, QGridLayout)
from PySide6.QtCore import QTime, Qt
import config.app_config as cfg

class SettingTabWidget(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.config_path = os.path.join("config", "config.json")
        self.time_fields = {}
        self.init_ui()
        self.load_config_to_ui()

    def create_time_edit(self):
        te = QTimeEdit()
        te.setDisplayFormat("HH:mm")
        te.setCalendarPopup(True)
        te.setKeyboardTracking(True)
        # Khi click vào, tự động bôi đen để nhập đè nhanh
        te.mousePressEvent = lambda event: (te.selectAll(), QTimeEdit.mousePressEvent(te, event))
        te.setStyleSheet("""
            QTimeEdit { padding: 8px; border: 1px solid #3498db; border-radius: 4px; font-size: 14px; }
            QTimeEdit::up-button, QTimeEdit::down-button { width: 20px; }
        """)
        return te

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(cfg.TAB_BAR_STYLE)
        
        # --- TAB 1: THỜI GIAN LÀM VIỆC ---
        tab_time = QWidget()
        time_layout = QVBoxLayout(tab_time)
        
        # Nhóm hành chính
        box_work = QGroupBox("🕒 Giờ hành chính")
        form_work = QFormLayout(box_work)
        for label, key, default in [("Sáng bắt đầu", "am_start", QTime(8, 0)), 
                                    ("Sáng kết thúc", "am_end", QTime(11, 30)),
                                    ("Chiều bắt đầu", "pm_start", QTime(13, 30)), 
                                    ("Chiều kết thúc", "pm_end", QTime(17, 0))]:
            field = self.create_time_edit()
            field.setTime(default)
            self.time_fields[key] = field
            form_work.addRow(f"{label}:", field)
            
        # Nhóm tăng ca
        box_ot = QGroupBox("🌙 Giờ tăng ca")
        form_ot = QFormLayout(box_ot)
        for label, key, default in [("OT bắt đầu", "ot_start", QTime(17, 30)),
                                    ("OT kết thúc", "ot_end", QTime(19, 30))]:
            field = self.create_time_edit()
            field.setTime(default)
            self.time_fields[key] = field
            form_ot.addRow(f"{label}:", field)
            
        time_layout.addWidget(box_work)
        time_layout.addWidget(box_ot)
        time_layout.addStretch()
        self.tab_widget.addTab(tab_time, "⏰ Thời gian làm việc")

        # --- TAB 2: THỜI HẠN PHIẾU (ĐÃ TỐI ƯU GIAO DIỆN) ---
        tab_deadline = QWidget()
        d_layout = QVBoxLayout(tab_deadline)
        
        # Tạo box bao quanh với nội dung có khoảng cách (padding)
        box_deadline = QGroupBox("Định mức số ngày thực hiện cho từng loại phiếu")
        box_deadline.setStyleSheet("QGroupBox { font-weight: bold; margin-top: 10px; }")
        
        grid = QGridLayout(box_deadline)
        grid.setSpacing(20) # Khoảng cách giữa các ô
        grid.setContentsMargins(20, 20, 20, 20) # Lề trong của box
        
        self.deadline_inputs = {}
        phieu_list = self.model.get_all_phieu_names()

        for i, p in enumerate(phieu_list):
            lbl = QLabel(f"📄 {p}")
            # Cấu hình Label để chữ không bị dính vào cạnh
            lbl.setStyleSheet("color: #2c3e50; font-size: 13px;")
            
            spin = QSpinBox()
            spin.setRange(0, 365)
            spin.setSuffix(" ngày")
            spin.setFixedHeight(35) # Tăng chiều cao để dễ nhìn
            # Style ô nhập số chuyên nghiệp
            spin.setStyleSheet("""
                QSpinBox { 
                    border: 1px solid #bdc3c7; 
                    border-radius: 5px; 
                    padding: 5px; 
                    background: #f8f9fa;
                }
                QSpinBox:focus { border: 1px solid #3498db; }
            """)
            
            # Cột 0: Label, Cột 1: SpinBox
            # i // 2 là hàng, (i % 2) * 2 là cột
            row = i // 2
            col = (i % 2) * 2
            
            grid.addWidget(lbl, row, col, Qt.AlignVCenter)
            grid.addWidget(spin, row, col + 1, Qt.AlignVCenter)
            
            # Thiết lập tỉ lệ co dãn cột: cột 1 (spinbox) co dãn, cột 0 (label) cố định
            grid.setColumnStretch(col + 1, 1)
            
            self.deadline_inputs[p] = spin
            
        # Thêm một Spacer ở dưới cùng để các hàng không bị dãn ra khi tab trống
        grid.setRowStretch(len(phieu_list) // 2 + 1, 1)
            
        scroll = QScrollArea()
        scroll.setWidget(box_deadline)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        d_layout.addWidget(scroll)
        self.tab_widget.addTab(tab_deadline, "📅 Thời hạn phiếu")

        main_layout.addWidget(self.tab_widget)
        
        # Footer chứa nút lưu
        footer = QHBoxLayout()
        footer.addStretch()
        self.btn_save = QPushButton("💾 Lưu cấu hình hệ thống")
        self.btn_save.setStyleSheet(cfg.BTN_PLAN_STYLE + "padding: 10px 20px;")
        self.btn_save.clicked.connect(self.save_all_settings)
        footer.addWidget(self.btn_save)
        main_layout.addLayout(footer)

    def save_all_settings(self):
        data = {
            "worktime": {k: v.time().toString("HH:mm") for k, v in self.time_fields.items()},
            "deadlines": {name: spin.value() for name, spin in self.deadline_inputs.items()}
        }
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        QMessageBox.information(self, "Thành công", "Đã cập nhật cấu hình hệ thống!")

    def load_config_to_ui(self):
        if not os.path.exists(self.config_path): return
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for k, v in data.get("worktime", {}).items():
                if k in self.time_fields:
                    self.time_fields[k].setTime(QTime.fromString(v, "HH:mm"))
            for name, value in data.get("deadlines", {}).items():
                if name in self.deadline_inputs:
                    self.deadline_inputs[name].setValue(value)