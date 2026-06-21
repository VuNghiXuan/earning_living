import re
from docx import Document

# --- CÁC LỚP DỮ LIỆU ---
class MaintenanceTask:
    def __init__(self, tt, name, workers, minutes, tool, material, tckt, result=""):
        self.tt = tt
        self.name = name
        self.workers = workers
        self.minutes = minutes
        self.tool = tool
        self.material = material
        self.tckt = tckt
        self.result = result

class DeviceMaintenance:
    def __init__(self, device_name, tech_name):
        self.device_name = device_name
        self.tech_name = tech_name
        self.cycles = {} 

    def add_task(self, cycle_code, task_obj):
        cycle_code = cycle_code.strip()
        if cycle_code not in self.cycles:
            self.cycles[cycle_code] = []
        # Tạo bản sao đối tượng để tránh xung đột dữ liệu
        new_task = MaintenanceTask(
            task_obj.tt, task_obj.name, task_obj.workers, task_obj.minutes,
            task_obj.tool, task_obj.material, task_obj.tckt, task_obj.result
        )
        self.cycles[cycle_code].append(new_task)


# --- CÁC HÀM XỬ LÝ DỮ LIỆU ---

def is_placeholder(val):
    clean_val = val.strip().replace('-', '').replace('/', '').replace(':', '')
    return clean_val == ""

def parse_header(text):
    """Phân tích tiêu đề để tìm: Phiếu công nghệ, Tên thiết bị, Các phiếu số."""
    header_data = {}
    
    # 1. Tìm Phiếu công nghệ
    tech_match = re.search(r'(PHIẾU\s+CÔNG\s+NGHỆ.+)', text, re.IGNORECASE)
    if tech_match:
        header_data['tech_name'] = tech_match.group(1).strip()
    
    # 2. Tìm Tên thiết bị
    dev_match = re.search(r'(?:TÊN\s*TRANG\s*BỊ\s*:\s*|\d+\.\s+)(.+)', text, re.IGNORECASE)
    if dev_match and "PHIẾU" not in dev_match.group(1).upper():
        header_data['device_name'] = dev_match.group(1).strip()
        
    # 3. Tìm Phiếu số
    cycle_match = re.search(r'PHIẾU\s*SỐ\s*:\s*([\d\s,–\-]+)', text, re.IGNORECASE)
    if cycle_match:
        raw_nums = re.split(r'[,–\-]', cycle_match.group(1))
        header_data['cycles'] = [f"Phiếu {n.strip().zfill(2)}" for n in raw_nums if n.strip().isdigit()]
        
    return header_data if header_data else None

def parse_table_row(row, prev_state):
    """Đọc và trích xuất dữ liệu từ hàng bảng."""
    cells = row.cells
    # Kiểm tra đủ cột và hàng dữ liệu phải bắt đầu bằng số (STT)
    if len(cells) < 8 or not re.match(r'^\d+', cells[0].text.strip()):
        return None, prev_state

    tt = cells[0].text.strip()
    name = cells[1].text.strip().replace('\n', ' ')
    workers = int(re.search(r'\d+', cells[2].text.strip()).group()) if re.search(r'\d+', cells[2].text.strip()) else 1
    mins = int(re.search(r'\d+', cells[3].text.strip()).group()) if re.search(r'\d+', cells[3].text.strip()) else 0
    
    # Kế thừa dữ liệu
    raw_tool = cells[4].text.strip()
    tool = prev_state['tool'] if is_placeholder(raw_tool) else raw_tool
    
    raw_mat = cells[5].text.strip()
    mat = prev_state['mat'] if is_placeholder(raw_mat) else raw_mat
    
    raw_tckt = cells[6].text.strip()
    tckt = prev_state['tckt'] if is_placeholder(raw_tckt) else raw_tckt
    
    result = cells[7].text.strip()

    # Cập nhật trạng thái
    if not is_placeholder(raw_tool): prev_state['tool'] = tool
    if not is_placeholder(raw_mat): prev_state['mat'] = mat
    if not is_placeholder(raw_tckt): prev_state['tckt'] = tckt
    
    task = MaintenanceTask(tt, name, workers, mins, tool, mat, tckt, result)
    return task, prev_state

# --- HÀM CHÍNH ---
def parse_maintenance_word_file(file_path):
    doc = Document(file_path)
    devices_dict = {}
    
    # 1. Gom nhóm: Chia document thành các block (1 tiêu đề + 1 bảng)
    # Chúng ta dùng chỉ số để duyệt
    all_elements = doc.paragraphs + doc.tables
    # Sắp xếp lại dựa trên vị trí thực tế trong file nếu cần, 
    # nhưng ở đây ta duyệt tuần tự:
    
    current_device = None
    current_tech = "Chưa xác định"
    current_cycles = ["Phiếu 01"]

    # Duyệt qua từng đoạn văn/bảng
    for item in doc.element.body:
        # Nếu là Paragraph (Tiêu đề)
        if item.tag.endswith('p'):
            text = item.text.strip()
            header = parse_header(text)
            if header:
                if 'tech_name' in header: current_tech = header['tech_name']
                if 'cycles' in header: current_cycles = header['cycles']
                if 'device_name' in header:
                    current_device = header['device_name']
                    if current_device not in devices_dict:
                        devices_dict[current_device] = DeviceMaintenance(current_device, current_tech)
                    print(f"\n>>> [TIÊU ĐỀ]: {current_device} | {current_cycles}")

        # Nếu là Table (Bảng)
        elif item.tag.endswith('tbl'):
            # Tìm đối tượng table tương ứng trong doc.tables
            # (Phải dùng cơ chế tìm bảng theo vị trí)
            table = next((t for t in doc.tables if t._element == item), None)
            
            if table and current_device:
                print(f"    [BẢNG]: Đang nạp cho {current_device} - {current_cycles}")
                
                device_obj = devices_dict[current_device]
                prev_state = {'tool': "", 'mat': "", 'tckt': ""}
                
                for row in table.rows[1:]:
                    task, prev_state = parse_table_row(row, prev_state)
                    if task:
                        # NẠP DỮ LIỆU ĐÚNG VÀO PHIẾU CỦA BLOCK HIỆN TẠI
                        for cycle in current_cycles:
                            device_obj.add_task(cycle, task)
                
                print(f"    [XONG]: Nạp xong {len(table.rows)-1} dòng vào {current_cycles}")
                
                # QUAN TRỌNG: RESET PHIẾU SAU MỖI BẢNG ĐỂ TRÁNH BỊ GÁN NHẦM
                current_cycles = [] 
                
    return list(devices_dict.values())