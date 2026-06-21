class MaintenanceController:
    def __init__(self, parent_controller):
        self.parent = parent_controller
        self.view = parent_controller.main_view.tab_plan
        self.model = parent_controller.model
        
        # Kết nối sự kiện cho tab kế hoạch
        self.view.btn_load.clicked.connect(self.on_btn_load_clicked)
        # ... các kết nối khác ...

    def on_btn_load_clicked(self):
        # Logic đổ dữ liệu lên bảng kế hoạch
        pass