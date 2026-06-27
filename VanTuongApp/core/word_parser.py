import re
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table

# Từ điển ánh xạ mã phiếu sang mô tả
PHIEU_MAP = {
    "01": "Bảo quản tuần", "02": "Bảo quản tháng",
    "03": "Bảo quản quý", "04": "Bảo quản trên biển"
}

# --- CÁC LỚP DỮ LIỆU ---
class MaintenanceTask:
    def __init__(self, tt, name, workers, minutes, tool, material, tckt, result="", order_index=0):
        self.tt = tt
        self.name = name
        self.workers = workers
        self.minutes = minutes
        self.tool = tool
        self.material = material
        self.tckt = tckt
        self.result = result
        self.order_index = order_index # Thứ tự dòng dùng để sắp xếp khi lấy từ DB

class DeviceMaintenance:
    def __init__(self, device_name): 
        self.device_name = device_name        
        self.cycles = {} 

    def add_task(self, cycle_code, task_obj):
        cycle_code = cycle_code.strip()
        if cycle_code not in self.cycles:
            self.cycles[cycle_code] = []
        # Tạo bản sao đối tượng để tránh xung đột dữ liệu giữa các phiếu
        new_task = MaintenanceTask(
            task_obj.tt, task_obj.name, task_obj.workers, task_obj.minutes,
            task_obj.tool, task_obj.material, task_obj.tckt, task_obj.result,
            task_obj.order_index
        )
        self.cycles[cycle_code].append(new_task)

# --- CÁC HÀM XỬ LÝ ---

def is_placeholder(val):
    """Kiểm tra nếu ô trống hoặc chứa ký tự quy ước thì sử dụng dữ liệu kế thừa."""
    return bool(re.fullmatch(r'[\-\/\s]+', val.strip()))

def parse_header(text):
    """Phân tích đoạn văn để trích xuất tên Thiết bị và Danh sách Phiếu."""
    header_data = {}
    # Trích xuất tên thiết bị
    dev_match = re.search(r'(?:TÊN\s*TRANG\s*BỊ\s*:\s*|\d+\.\s+)(.+)', text, re.IGNORECASE)
    if dev_match and "PHIẾU" not in dev_match.group(1).upper():
        header_data['device_name'] = dev_match.group(1).strip()
        
    # Trích xuất mã phiếu
    cycle_match = re.search(r'PHIẾU\s*SỐ\s*:\s*([\d\s,–\-]+)', text, re.IGNORECASE)
    if cycle_match:
        raw_nums = re.split(r'[,–\-]', cycle_match.group(1))
        cycles = [f"Phiếu {n.strip().zfill(2)}" for n in raw_nums if n.strip().isdigit()]
        header_data['cycles'] = cycles
    return header_data if header_data else None

def parse_table_row(row, prev_state, current_index):
    """Trích xuất dữ liệu dòng, bỏ qua dòng tổng, kế thừa giá trị ô trống."""
    cells = row.cells
    if len(cells) < 8: return None, prev_state

    task_name = cells[1].text.strip()
    
    # Logic bỏ qua dòng Tổng
    if "TỔNG" in task_name.upper():
        return None, prev_state

    # Chỉ xử lý dòng bắt đầu bằng số thứ tự (STT)
    if not re.match(r'^\d+', cells[0].text.strip()):
        return None, prev_state

    tt = cells[0].text.strip()
    workers = int(re.search(r'\d+', cells[2].text.strip()).group()) if re.search(r'\d+', cells[2].text.strip()) else 1
    mins = int(re.search(r'\d+', cells[3].text.strip()).group()) if re.search(r'\d+', cells[3].text.strip()) else 0
    
    # Xử lý kế thừa dữ liệu từ dòng trước (ô trống dùng lại giá trị cũ)
    raw_tool, raw_mat, raw_tckt = cells[4].text.strip(), cells[5].text.strip(), cells[6].text.strip()
    
    tool = prev_state['tool'] if is_placeholder(raw_tool) else raw_tool
    mat = prev_state['mat'] if is_placeholder(raw_mat) else raw_mat
    tckt = prev_state['tckt'] if is_placeholder(raw_tckt) else raw_tckt
    result = cells[7].text.strip()

    # Cập nhật trạng thái kế thừa cho dòng tiếp theo
    if not is_placeholder(raw_tool): prev_state['tool'] = tool
    if not is_placeholder(raw_mat): prev_state['mat'] = mat
    if not is_placeholder(raw_tckt): prev_state['tckt'] = tckt
    
    task = MaintenanceTask(tt, task_name, workers, mins, tool, mat, tckt, result, current_index)
    return task, prev_state

def parse_maintenance_word_file(file_path):
    """Hàm chính để đọc file Word và trả về danh sách đối tượng thiết bị."""
    doc = Document(file_path)
    devices_dict = {}
    current_device = None
    current_cycles = []

    for element in doc.element.body:
        # Xử lý đoạn văn (Header)
        if element.tag.endswith('p'):
            p = Paragraph(element, doc)
            header = parse_header(p.text.strip())
            if header:
                if 'cycles' in header: current_cycles = header['cycles']
                if 'device_name' in header:
                    current_device = header['device_name']
                    if current_device not in devices_dict:
                        devices_dict[current_device] = DeviceMaintenance(current_device)

        # Xử lý bảng dữ liệu
        elif element.tag.endswith('tbl'):
            table = Table(element, doc)
            if current_device and current_cycles:
                device_obj = devices_dict[current_device]
                prev_state = {'tool': "", 'mat': "", 'tckt': ""}
                row_idx = 0 
                
                # Bỏ qua hàng header của bảng (table.rows[0])
                for row in table.rows[1:]:
                    task, prev_state = parse_table_row(row, prev_state, row_idx)
                    if task:
                        row_idx += 1 # Chỉ tăng khi tìm thấy task hợp lệ
                        for cycle in current_cycles:
                            device_obj.add_task(cycle, task)
    
    return list(devices_dict.values())