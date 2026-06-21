import customtkinter as ctk
from word_processe.models import WordProcessor
from word_processe.views import MainApplicationView
from word_processe.controllers import WordApplicationController

def main():
    # Thiết lập giao diện hiện đại (Dark/Light mode)
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue") 
    
    # Khởi tạo các thành phần theo đúng mô hình MVC
    model_instance = WordProcessor()
    view_instance = MainApplicationView()
    
    # Khởi tạo bộ điều khiển trung tâm để kết nối Model và View
    controller_instance = WordApplicationController(model=model_instance, view=view_instance)
    
    # Chạy vòng lặp ứng dụng Desktop
    view_instance.mainloop()

if __name__ == "__main__":
    main()
