import sqlite3
import os
from docx import Document

class PlanModel:
    def __init__(self, db_path="config/database.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            cursor.execute("CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY AUTOINCREMENT, group_name TEXT UNIQUE NOT NULL)")
            cursor.execute("CREATE TABLE IF NOT EXISTS source_files (id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT NOT NULL, file_path TEXT NOT NULL, imported_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, group_id INTEGER NOT NULL, source_file_id INTEGER, device_name TEXT UNIQUE NOT NULL,
                    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE, FOREIGN KEY (source_file_id) REFERENCES source_files(id) ON DELETE SET NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS maintenance_cycles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, device_id INTEGER NOT NULL, cycle_code TEXT NOT NULL, cycle_name TEXT,
                    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
                )
            """)
            # ĐÃ THÊM CỘT result TEXT Ở DƯỚI ĐÂY:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS master_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, cycle_id INTEGER NOT NULL, tt TEXT NOT NULL, task_name TEXT NOT NULL,
                    norm_workers INTEGER DEFAULT 1, norm_minutes INTEGER DEFAULT 0, tool TEXT, material TEXT, tckt TEXT, result TEXT,
                    FOREIGN KEY (cycle_id) REFERENCES maintenance_cycles(id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def add_new_group(self, group_name):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO groups (group_name) VALUES (?)", (group_name.strip(),))
            conn.commit()

    def import_from_word_data(self, parsed_data, target_group_name, file_name, file_path):
        if not parsed_data: return
        
        if not target_group_name or target_group_name.strip() == "":
            target_group_name = "Chưa phân loại"
            
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 1. Đảm bảo nhóm tồn tại
            cursor.execute("INSERT OR IGNORE INTO groups (group_name) VALUES (?)", (target_group_name,))
            cursor.execute("SELECT id FROM groups WHERE group_name = ?", (target_group_name,))
            group_id = cursor.fetchone()["id"]
            
            # 2. Ghi nhận file nguồn
            cursor.execute("INSERT INTO source_files (file_name, file_path) VALUES (?, ?)", (file_name, file_path))
            source_file_id = cursor.lastrowid
            
            # 3. Nạp thiết bị và tác vụ
            for dev_obj in parsed_data: # Sử dụng dev_obj là instance của DeviceMaintenance
                d_name = dev_obj.device_name
                
                # Insert thiết bị
                cursor.execute("INSERT OR IGNORE INTO devices (group_id, source_file_id, device_name) VALUES (?, ?, ?)", 
                               (group_id, source_file_id, d_name))
                cursor.execute("SELECT id FROM devices WHERE device_name = ?", (d_name,))
                device_id = cursor.fetchone()["id"]
                
                # Duyệt qua các chu kỳ (cycles là dict: {"Phiếu 01": [tasks]})
                for c_code, tasks in dev_obj.cycles.items():
                    # Xử lý chu kỳ bảo dưỡng
                    cursor.execute("SELECT id FROM maintenance_cycles WHERE device_id = ? AND cycle_code = ?", (device_id, c_code))
                    cycle_row = cursor.fetchone()
                    if cycle_row:
                        cycle_id = cycle_row["id"]
                        cursor.execute("DELETE FROM master_tasks WHERE cycle_id = ?", (cycle_id,))
                    else:
                        cursor.execute("INSERT INTO maintenance_cycles (device_id, cycle_code, cycle_name) VALUES (?, ?, ?)", 
                                       (device_id, c_code, c_code)) # c_name có thể dùng c_code nếu không có tên riêng
                        cycle_id = cursor.lastrowid
                    
                    # Insert các đầu việc với cột result mới
                    for t in tasks: # t là instance của MaintenanceTask
                        cursor.execute("""
                            INSERT INTO master_tasks (cycle_id, tt, task_name, norm_workers, norm_minutes, tool, material, tckt, result)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (cycle_id, t.tt, t.name, t.workers, t.minutes, t.tool, t.material, t.tckt, t.result))
            conn.commit()

    def move_device_to_group(self, device_name, new_group_name):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Lấy ID của nhóm đích
            cursor.execute("SELECT id FROM groups WHERE group_name = ?", (new_group_name,))
            group_row = cursor.fetchone()
            if group_row:
                new_group_id = group_row["id"]
                # Cập nhật group_id cho máy
                cursor.execute("UPDATE devices SET group_id = ? WHERE device_name = ?", (new_group_id, device_name))
                conn.commit()

    def generate_daily_plan_word(self, save_path, selected_tasks, device_name, cycle_info, plan_date_str):
        doc = Document()
        doc.add_heading('KẾ HOẠCH BẢO DƯỠNG TRANG BỊ TRONG NGÀY', level=1)
        doc.add_paragraph(f"Ngày lập thực hiện: {plan_date_str}")
        doc.add_paragraph(f"Tên trang bị: {device_name}")
        doc.add_paragraph(f"Nội dung thực hiện: {cycle_info}")
        
        # 1. Tăng số cột lên 8
        table = doc.add_table(rows=1, cols=8) 
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        
        # 2. Thêm tiêu đề 'Kết quả' vào headers
        headers = ['STT', 'Nội dung công việc', 'Số người', 'Thời gian (Phút)', 'Dụng cụ', 'Vật tư', 'TCKT', 'Kết quả']
        for idx, text in enumerate(headers):
            hdr_cells[idx].text = text
            
        for task in selected_tasks:
            row_cells = table.add_row().cells
            row_cells[0].text = str(task.get("tt", ""))
            row_cells[1].text = str(task.get("name", ""))
            row_cells[2].text = str(task.get("workers", ""))
            row_cells[3].text = str(task.get("minutes", ""))
            row_cells[4].text = str(task.get("tool", ""))
            row_cells[5].text = str(task.get("material", ""))
            row_cells[6].text = str(task.get("tckt", ""))
            # 3. Nạp dữ liệu vào cột thứ 8 (index 7)
            row_cells[7].text = str(task.get("result", "")) 
            
        doc.save(save_path)

    # Cập nhật dữ liệu cho danh mục định mức
    def get_all_norms(self):
        query = """
            SELECT d.device_name, mc.cycle_code, mt.tt, mt.task_name, mt.norm_workers, 
                mt.norm_minutes, mt.tool, mt.material, mt.tckt, mt.result
            FROM master_tasks mt
            JOIN maintenance_cycles mc ON mt.cycle_id = mc.id
            JOIN devices d ON mc.device_id = d.id
            ORDER BY d.device_name, mc.cycle_code, CAST(mt.tt AS REAL) ASC
        """
        with self.get_connection() as conn:
            return [list(row) for row in conn.execute(query).fetchall()]
        
    def get_tasks(self, group_name, device_name, cycle_code):
        """
        Truy vấn danh sách công việc dựa trên Nhóm, Thiết bị và Mã chu kỳ.
        """
        with self.get_connection() as conn:
            query = """
                SELECT t.* FROM master_tasks t
                JOIN maintenance_cycles c ON t.cycle_id = c.id
                JOIN devices d ON c.device_id = d.id
                JOIN groups g ON d.group_id = g.id
                WHERE g.group_name = ? AND d.device_name = ? AND c.cycle_code = ?
            """
            return conn.execute(query, (group_name, device_name, cycle_code)).fetchall()
        
    def get_devices_by_group(self, group_name):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.device_name FROM devices d
                JOIN groups g ON d.group_id = g.id
                WHERE g.group_name = ?
            """, (group_name,))
            return [row["device_name"] for row in cursor.fetchall()]

    def get_all_group_names(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT group_name FROM groups")
            return [row["group_name"] for row in cursor.fetchall()]