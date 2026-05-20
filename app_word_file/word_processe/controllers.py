import os
from .models import WordProcessor

class WordApplicationController:
    def __init__(self, model: WordProcessor, view):
        self.model = model
        self.view = view
        
        # Đăng ký hàm xử lý sự kiện khi View kích hoạt chọn file Word
        self.view.register_controller_handler(self.handle_word_import)

    def handle_word_import(self, file_path):
        """Xử lý luồng dữ liệu khi người dùng chọn file Word thành công"""
        try:
            # 1. Ra lệnh cho Model nạp file
            self.model.read_file(file_path)
            
            # 2. Lấy cấu trúc dữ liệu đã được bóc tách từ Model
            structured_data = self.model.get_structured_content()
            file_name = os.path.basename(file_path)
            
            # 3. Đổ dữ liệu về cho View hiển thị lên màn hình Tab 1
            self.view.update_document_view(file_name, structured_data)
            print(f"--- Controller điều phối thành công dữ liệu file: {file_name} ---")
            
        except Exception as error:
            print(f"Lỗi hệ thống trong quá trình điều phối file: {error}")
            self.view.lbl_file_status.configure(text="Lỗi: Không thể đọc cấu trúc file!", text_color="red")