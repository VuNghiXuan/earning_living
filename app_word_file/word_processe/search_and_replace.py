import tkinter as tk
import customtkinter as ctk
from docx import Document

class WordProcessorTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        
        # 1. Khu vực tìm kiếm và thay thế
        find_replace_frame = ctk.CTkFrame(self)
        find_replace_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.find_entry = ctk.CTkEntry(find_replace_frame, placeholder_text="Tìm kiếm...")
        self.find_entry.pack(fill="x", padx=5, pady=5)
        
        self.replace_entry = ctk.CTkEntry(find_replace_frame, placeholder_text="Thay thế bằng...")
        self.replace_entry.pack(fill="x", padx=5, pady=5)
        
        self.btn_replace = ctk.CTkButton(find_replace_frame, text="Thực hiện Thay thế", command=self.perform_replace)
        self.btn_replace.pack(fill="x", padx=5, pady=5)
        
        # 2. Khu vực xuất file
        export_frame = ctk.CTkFrame(self)
        export_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.btn_export = ctk.CTkButton(export_frame, text="Xuất ra File Word (.docx)", command=self.export_to_word, fg_color="green")
        self.btn_export.pack(fill="x", padx=5, pady=5)
        
        # Giả lập dữ liệu văn bản đang xử lý
        self.current_text = "Chào mừng bạn đến với ứng dụng quản lý tri thức."

    def perform_replace(self):
        find_str = self.find_entry.get()
        replace_str = self.replace_entry.get()
        
        if find_str:
            self.current_text = self.current_text.replace(find_str, replace_str)
            print(f"Đã thay thế '{find_str}' thành '{replace_str}'")
            # Ở đây bạn nên cập nhật lại Textbox hiển thị nếu có
        
    def export_to_word(self):
        """Hàm xuất dữ liệu hiện tại ra file Word"""
        doc = Document()
        doc.add_paragraph(self.current_text)
        
        file_path = "output_tri_thuc.docx"
        doc.save(file_path)
        print(f"Đã xuất file thành công tại: {file_path}")
        # Thêm thông báo UI tại đây nếu muốn