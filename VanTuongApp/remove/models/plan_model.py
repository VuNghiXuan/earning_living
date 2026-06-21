import sqlite3
import os
import json
import re

class PlanModel:
    def __init__(self, db_path="config/database.db", config_path="config/config.json"):
        self.db_path = db_path
        self.config_path = config_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()
        self.init_config()
        
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
        
    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Bảng nhóm thiết bị
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_name TEXT UNIQUE
                )
            """)
            # Bảng máy móc (Trang bị) liên kết với nhóm qua group_id
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER,
                    device_name TEXT UNIQUE,
                    FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
                )
            """)
           
            # Hàm init_db cho bảng master_tasks
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS master_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cycle_id INTEGER,
                    tt TEXT,
                    task_name TEXT,
                    norm_workers INTEGER,
                    norm_minutes INTEGER,
                    tool TEXT,
                    material TEXT,
                    tckt TEXT,
                    FOREIGN KEY(cycle_id) REFERENCES maintenance_cycles(id) ON DELETE CASCADE
                )
            """)

            # CẦN THÊM BẢNG NÀY ĐỂ HÀM IMPORT HOẠT ĐỘNG
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS maintenance_cycles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id INTEGER,
                    cycle_code TEXT,
                    cycle_name TEXT,
                    FOREIGN KEY(device_id) REFERENCES devices(id) ON DELETE CASCADE
                )
            """)
            
            # Khởi tạo một số dữ liệu mẫu nếu DB trống
            cursor.execute("SELECT COUNT(*) as count FROM groups")
            if cursor.fetchone()["count"] == 0:
                cursor.execute("INSERT INTO groups (group_name) VALUES ('Nhóm Sonar')")
                cursor.execute("INSERT INTO groups (group_name) VALUES ('Nhóm Thông Tin')")
                cursor.execute("INSERT INTO devices (group_id, device_name) VALUES (1, 'TỔ HỢP THỦY ÂM МГК-400ЭМ')")
                cursor.execute("INSERT INTO devices (group_id, device_name) VALUES (2, 'TRẠM ĐO VẬN TỐC ÂM МГ-553')")
            conn.commit()

    def init_config(self):
        if not os.path.exists(self.config_path):
            default_config = {
                "morning_start": "07:00", "morning_end": "11:30",
                "afternoon_start": "13:30", "afternoon_end": "17:00"
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4)

    def save_time_config(self, m_start, m_end, a_start, a_end):
        config = {"morning_start": m_start, "morning_end": m_end, "afternoon_start": a_start, "afternoon_end": a_end}
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)

    def load_time_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # Các hàm tương tác danh mục động
    def add_group(self, group_name):
        try:
            with self.get_connection() as conn:
                conn.execute("INSERT INTO groups (group_name) VALUES (?)", (group_name,))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_group(self, group_name):
        with self.get_connection() as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("DELETE FROM groups WHERE group_name = ?", (group_name,))
            conn.commit()

    def add_device(self, group_name, device_name):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM groups WHERE group_name = ?", (group_name,))
                row = cursor.fetchone()
                if row:
                    cursor.execute("INSERT INTO devices (group_id, device_name) VALUES (?, ?)", (row["id"], device_name))
                    conn.commit()
                    return True
            return False
        except sqlite3.IntegrityError:
            return False

    def delete_device(self, device_name):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM devices WHERE device_name = ?", (device_name,))
            conn.commit()

    def get_unique_groups(self):
        with self.get_connection() as conn:
            return [row["group_name"] for row in conn.execute("SELECT group_name FROM groups").fetchall()]

    def get_devices_by_group(self, group_name):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.device_name FROM devices d 
                JOIN groups g ON d.group_id = g.id 
                WHERE g.group_name = ?
            """, (group_name,))
            return [row["device_name"] for row in cursor.fetchall()]

    # Các hàm tương tác dữ liệu định mức việc
    def import_from_word_data(self, parsed_data, group_name):
        if not parsed_data: return
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Lấy group_id
            cursor.execute("SELECT id FROM groups WHERE group_name = ?", (group_name,))
            row = cursor.fetchone()
            g_id = row["id"] if row else 1 

            for block in parsed_data:
                # 2. Thêm thiết bị
                cursor.execute("INSERT OR IGNORE INTO devices (group_id, device_name) VALUES (?, ?)", 
                            (g_id, block["device_name"]))
                
                # 3. Lấy device_id
                cursor.execute("SELECT id FROM devices WHERE device_name = ?", (block["device_name"],))
                d_id = cursor.fetchone()["id"]
                
                # 4. Xử lý cycle và lấy cycle_id
                cursor.execute("SELECT id FROM maintenance_cycles WHERE device_id = ? AND cycle_code = ?", 
                            (d_id, block["cycle_code"]))
                c_row = cursor.fetchone()
                
                if c_row:
                    cycle_id = c_row["id"]
                    cursor.execute("DELETE FROM master_tasks WHERE cycle_id = ?", (cycle_id,))
                else:
                    cursor.execute("INSERT INTO maintenance_cycles (device_id, cycle_code, cycle_name) VALUES (?, ?, ?)", 
                                (d_id, block["cycle_code"], block["cycle_name"]))
                    cycle_id = cursor.lastrowid
                
                # 5. Insert vào master_tasks với cycle_id chính xác
                for task in block["tasks"]:
                    cursor.execute("""
                        INSERT INTO master_tasks (cycle_id, tt, task_name, norm_workers, norm_minutes, tool, material, tckt)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (cycle_id, task["tt"], task["name"], task["norm_workers"], 
                        task["norm_minutes"], task["tool"], task["material"], task["tckt"]))
            conn.commit()

    def get_tasks(self, device, cycle_text):
        match = re.search(r'\d+', cycle_text)
        if not match: return []
        cycle_code = f"Phiếu {match.group()}"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tt, task_name AS name, norm_minutes, tool, material, tckt 
                FROM master_tasks 
                WHERE device_name = ? AND cycle_code = ?
                ORDER BY id ASC
            """, (device, cycle_code))
            return [dict(row) for row in cursor.fetchall()]
    
    # Trong PlanModel.py - Hàm get_all_norms
    def get_all_norms(self):
        query = """
            SELECT 
                d.device_name, 
                mc.cycle_code, 
                mt.tt, 
                mt.task_name, 
                mt.norm_workers, 
                mt.norm_minutes, 
                mt.tool, 
                mt.tckt,
                mt.result
            FROM master_tasks mt
            JOIN maintenance_cycles mc ON mt.cycle_id = mc.id
            JOIN devices d ON mc.device_id = d.id
            ORDER BY d.device_name, mc.cycle_code, CAST(mt.tt AS REAL) ASC
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Dữ liệu trả về bây giờ có 9 phần tử (index 8 là result)
            return [list(row) for row in cursor.execute(query).fetchall()]