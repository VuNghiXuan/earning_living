import re
from docx import Document

# 1. Định nghĩa từ điển ánh xạ
PHIEU_MAP = {
    "01": "Bảo quản tuần",
    "02": "Bảo quản tháng",
    "03": "Bảo quản quý",
    "04": "Bảo quản trên biển"
}

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
    def __init__(self, device_name): 
        self.device_name = device_name        
        self.cycles = {}           # Dict lưu danh sách task theo từng mã phiếu

    def add_task(self, cycle_code, task_obj):
        cycle_code = cycle_code.strip()
        if cycle_code not in self.cycles:
            self.cycles[cycle_code] = []
        # Sao chép đối tượng để tránh tham chiếu chồng chéo
        new_task = MaintenanceTask(
            task_obj.tt, task_obj.name, task_obj.workers, task_obj.minutes,
            task_obj.tool, task_obj.material, task_obj.tckt, task_obj.result
        )
        self.cycles[cycle_code].append(new_task)

# --- HÀM XỬ LÝ DỮ LIỆU ---

def is_placeholder(val):
    """
    Chỉ trả về True nếu ô trống hoàn toàn hoặc 
    chỉ chứa các ký tự quy ước như '-', '/', hoặc khoảng trắng.
    """
    # Xóa khoảng trắng 2 đầu
    val = val.strip()
    
    # Sử dụng Regex để khớp nếu chuỗi chỉ gồm: - / hoặc khoảng trắng
    if re.fullmatch(r'[\-\/\s]+', val):
        return True
        
    return False

def parse_header(text):
    """Phân tích đoạn văn để trích xuất  Thiết bị và Danh sách Phiếu số."""
    header_data = {}
    
    
    
    # 1. Trích xuất Tên thiết bị (Bỏ qua các đoạn chứa từ khóa "PHIẾU")
    dev_match = re.search(r'(?:TÊN\s*TRANG\s*BỊ\s*:\s*|\d+\.\s+)(.+)', text, re.IGNORECASE)
    if dev_match and "PHIẾU" not in dev_match.group(1).upper():
        header_data['device_name'] = dev_match.group(1).strip()
        
    # 2. Trích xuất Danh sách Phiếu số (Xử lý các dạng: 02, 03 hoặc 02-03)   

    cycle_match = re.search(r'PHIẾU\s*SỐ\s*:\s*([\d\s,–\-]+)', text, re.IGNORECASE)
    if cycle_match:
        raw_nums = re.split(r'[,–\-]', cycle_match.group(1))
        cycles = []
        for n in raw_nums:
            n_clean = n.strip()
            if n_clean.isdigit():
                # Đảm bảo số phiếu có dạng 2 chữ số (VD: 1 -> 01)
                formatted_num = n_clean.zfill(2)
                
                # Lấy mô tả từ map, nếu không có thì để trống
                description = PHIEU_MAP.get(formatted_num, "")
                
                # Tạo chuỗi hiển thị
                display_str = f"Phiếu {formatted_num}"
                if description:
                    display_str += f" ({description})"
                
                cycles.append(display_str)
        
        header_data['cycles'] = cycles
    return header_data if header_data else None

def parse_table_row(row, prev_state):
    """Trích xuất dữ liệu từ hàng bảng và thực hiện cơ chế kế thừa nội dung."""
    cells = row.cells
    # Chỉ xử lý các hàng bắt đầu bằng số STT
    if len(cells) < 8 or not re.match(r'^\d+', cells[0].text.strip()):
        return None, prev_state

    tt = cells[0].text.strip()
    name = cells[1].text.strip().replace('\n', ' ')
    workers = int(re.search(r'\d+', cells[2].text.strip()).group()) if re.search(r'\d+', cells[2].text.strip()) else 1
    mins = int(re.search(r'\d+', cells[3].text.strip()).group()) if re.search(r'\d+', cells[3].text.strip()) else 0
    
    # Kế thừa dữ liệu từ dòng trước nếu ô hiện tại trống
    raw_tool, raw_mat, raw_tckt = cells[4].text.strip(), cells[5].text.strip(), cells[6].text.strip()
    
    tool = prev_state['tool'] if is_placeholder(raw_tool) else raw_tool
    mat = prev_state['mat'] if is_placeholder(raw_mat) else raw_mat
    tckt = prev_state['tckt'] if is_placeholder(raw_tckt) else raw_tckt
    result = cells[7].text.strip()

    # Cập nhật trạng thái kế thừa cho dòng tiếp theo
    if not is_placeholder(raw_tool): prev_state['tool'] = tool
    if not is_placeholder(raw_mat): prev_state['mat'] = mat
    if not is_placeholder(raw_tckt): prev_state['tckt'] = tckt
    
    task = MaintenanceTask(tt, name, workers, mins, tool, mat, tckt, result)
    return task, prev_state

# --- HÀM CHÍNH ---
def parse_maintenance_word_file(file_path):
    doc = Document(file_path)
    devices_dict = {}
    
    current_device = None
    current_cycles = [] # Chỉ reset khi chắc chắn tìm thấy tiêu đề mới

    for element in doc.element.body:
        # Xử lý đoạn văn (Tiêu đề thiết bị và mã phiếu)
        if element.tag.endswith('p'):
            # Convert element XML thành đối tượng Paragraph của docx
            from docx.text.paragraph import Paragraph
            p = Paragraph(element, doc)
            header = parse_header(p.text.strip())
            
            if header:
                if 'cycles' in header: 
                    current_cycles = header['cycles']
                if 'device_name' in header:
                    current_device = header['device_name']
                    if current_device not in devices_dict:
                        devices_dict[current_device] = DeviceMaintenance(current_device)

        # Xử lý bảng
        elif element.tag.endswith('tbl'):
            from docx.table import Table
            table = Table(element, doc)
            
            # Chỉ nạp nếu đã có thiết bị và phiếu xác định
            if current_device and current_cycles:
                device_obj = devices_dict[current_device]
                prev_state = {'tool': "", 'mat': "", 'tckt': ""}
                
                for row in table.rows[1:]:
                    task, prev_state = parse_table_row(row, prev_state)
                    if task:
                        # Gán task vào tất cả các phiếu đã tìm thấy ở trên
                        for cycle in current_cycles:
                            device_obj.add_task(cycle, task)
    
    return list(devices_dict.values())