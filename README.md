# ThuyAm\_Scheduler/

# │

# ├── config/

# │   ├── config.json          # Lưu cấu hình giờ giấc làm việc (Buổi sáng, Buổi chiều)

# │   └── database.db          # Cơ sở dữ liệu SQLite lưu Định mức gốc và Lịch sử phiếu

# │

# ├── core/

# │   ├── \_\_init\_\_.py

# │   ├── scheduler.py         # Thuật toán tính dải giờ tự động (Timeline Engine)

# │   └── word\_exporter.py     # Module đọc/ghi và xuất biểu mẫu Word (.docx)

# │

# ├── models/

# │   ├── \_\_init\_\_.py

# │   ├── base\_model.py        # Kết nối và tương tác SQLite

# │   ├── plan\_model.py        # Xử lý dữ liệu liên quan đến Định mức phiếu, Máy, Nhóm

# │   └── history\_model.py     # Xử lý lưu vết, sửa đổi phiếu bảo dưỡng cũ

# │

# ├── views/

# │   ├── \_\_init\_\_.py

# │   ├── main\_window.py       # Giao diện chính (Sidebar + Khung chứa Tab)

# │   ├── tab\_plan.py          # View Tab LẬP KẾ HOẠCH (Metadata Form + Excel Grid)

# │   ├── tab\_config.py        # View Tab CẤU HÌNH THỜI GIAN

# │   ├── tab\_history.py       # View Tab LỊCH SỬ BẢO QUẢN

# │   └── components/

# │       ├── \_\_init\_\_.py

# │       ├── excel\_grid.py    # Custom Table Widget kiểu ô vuông phẳng chuẩn Excel

# │       └── date\_picker.py   # Custom Widget chọn ngày tháng

# │

# ├── controllers/

# │   ├── \_\_init\_\_.py

# │   ├── main\_controller.py   # Điều phối trung tâm kết nối các Tab và Models

# │   ├── plan\_controller.py   # Xử lý logic nạp định mức, tính giờ, bắt sự kiện lưới

# │   ├── config\_controller.py # Xử lý đọc/ghi file config.json khi người dùng đổi giờ

# │   └── history\_controller.py# Xử lý tìm kiếm lịch sử, gọi ngược phiếu cũ đổ lại lưới

# │

# ├── assets/

# │   ├── icons/               # Chứa các file icon .png/.svg (chọn file Word, lưu, cài đặt...)

# │   └── templates/           # Chứa các file Word mẫu (.docx) đầu ra để đổ dữ liệu vào

# │

# ├── requirements.txt         # Danh sách thư viện (PySide6, python-docx, v.v.)

# └── main.py                  # File khởi chạy ứng dụng (Application Entry Point)

