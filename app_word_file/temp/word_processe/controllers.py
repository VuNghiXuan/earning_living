import os
import traceback
from .models import WordProcessor

class WordApplicationController:
    def __init__(self, model: WordProcessor, view):
        self.model = model
        self.view = view
        
        # Đăng ký hàm xử lý sự kiện khi View kích hoạt chọn file Word
        if hasattr(self.view, 'register_controller_handler'):
            self.view.register_controller_handler(self.handle_word_import)
        else:
            print("[CẢNH BÁO] View chưa cài đặt hàm register_controller_handler")

    def handle_word_import(self, file_path):
        """Xử lý luồng dữ liệu tuần tự khi người dùng chọn file Word từ giao diện"""
        if not file_path or not os.path.exists(file_path):
            self._show_error_on_view("Đường dẫn file không hợp lệ hoặc không tồn tại!")
            return

        try:
            # Cập nhật trạng thái chờ trên GUI nếu có
            if hasattr(self.view, 'lbl_file_status'):
                self.view.lbl_file_status.configure(text="Đang xử lý cấu trúc file...", text_color="orange")
            
            # 1. Ra lệnh cho Model nạp và bóc tách dữ liệu file Word
            self.model.read_file(file_path)
            structured_data = self.model.get_structured_content()
            
            # 2. Kiểm tra tính toàn vẹn của dữ liệu nhận được từ Model
            if not structured_data:
                self._show_error_on_view("File Word rỗng hoặc không có cấu trúc hợp lệ!")
                return
                
            # Kiểm tra xem cấu trúc dữ liệu trả về có đúng dạng List (danh sách) không
            if not isinstance(structured_data, list):
                raise TypeError(f"Dữ liệu từ Model phải trả về list, nhưng nhận được: {type(structured_data)}")
                
            file_name = os.path.basename(file_path)
            
            # 3. Đổ dữ liệu an toàn về cho View để hiển thị lên UI (Tab Văn bản & Bảng)
            if hasattr(self.view, 'update_document_view'):
                self.view.update_document_view(file_name, structured_data)
                print(f"--- [Controller] Điều phối thành công dữ liệu file: {file_name} ---")
            else:
                raise AttributeError("Giao diện (View) chưa cài đặt hàm hiển thị dữ liệu 'update_document_view'")
            
        except Exception as error:
            # In chi tiết dòng bị lỗi để lập trình viên dễ debug (Tránh nuốt lỗi gốc)
            print("\n" + "="*50)
            print(f"[LỖI HỆ THỐNG PHÂN PHỐI FILE]: {error}")
            print("-" * 50)
            traceback.print_exc()
            print("="*50 + "\n")
            
            # Đẩy thông báo lỗi thân thiện lên UI cho khách hàng/người dùng
            self._show_error_on_view(f"Lỗi: {str(error)}")

    def _show_error_on_view(self, message):
        """Hỗ trợ cập nhật thông báo lỗi đồng bộ lên nhãn trạng thái của giao diện"""
        if hasattr(self.view, 'lbl_file_status') and self.view.lbl_file_status:
            try:
                self.view.lbl_file_status.configure(text=message, text_color="red")
            except Exception:
                pass