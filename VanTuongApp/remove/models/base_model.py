import sqlite3
import os

class BaseModel:
    def __init__(self, db_path="config/database.db"):
        self.db_path = db_path
        # Tự động tạo thư mục config nếu chưa có
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()
        
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row # Cho phép gọi trích xuất dữ liệu theo tên cột
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 1. Bảng lưu trữ Trang bị (Máy)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_name TEXT,
                    device_name TEXT UNIQUE
                )
            """)
            # 2. Bảng lưu trữ Định mức công tác gốc bóc từ file Word ra
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS master_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_name TEXT,
                    cycle_code TEXT,
                    tt TEXT,
                    task_name TEXT,
                    norm_workers INTEGER,
                    norm_minutes INTEGER,
                    tool TEXT,
                    material TEXT,
                    tckt TEXT
                )
            """)
            conn.commit()