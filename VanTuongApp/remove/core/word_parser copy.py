import docx
import re
import unicodedata

def normalize_text(text):
    if not text: return ""
    text = unicodedata.normalize('NFC', text)
    return " ".join(text.strip().split())

def parse_maintenance_word_file(file_path):
    try:
        doc = docx.Document(file_path)
    except Exception as e:
        print(f"Lỗi mở file Word: {e}")
        return []
        
    parsed_data = []
    current_device = "Chưa xác định"
    current_cycles = []
    
    for element in doc.element.body:
        # 1. Bẫy Tên máy và Số phiếu từ Paragraph
        if element.tag.endswith('p'):
            p = docx.text.paragraph.Paragraph(element, doc)
            text = normalize_text(p.text)
            if not text: continue
            
            # Khớp tên máy lớn (Ví dụ: "1. TỔ HỢP THỦY ÂM МГК-400ЭМ")
            if re.match(r'^\d+\.\s+[A-ZĐ]', text):
                current_device = re.sub(r'^\d+\.\s+', '', text)
                continue
                
            # Khớp số phiếu chu kỳ
            if "PHIẾU SỐ:" in text:
                current_cycles = re.findall(r'\d+', text)
                continue
                
        # 2. Bẫy và bóc tách bảng biểu
        elif element.tag.endswith('tbl'):
            table = docx.table.Table(element, doc)
            if len(table.rows) < 3: continue
            
            tasks_list = []
            for row_idx in range(2, len(table.rows)):
                row = table.rows[row_idx]
                
                # Đọc thô toàn bộ các ô trong hàng (Thư viện docx sẽ tự rã các ô trộn thành các ô độc lập)
                raw_cells = [normalize_text(cell.text) for cell in row.cells]
                
                # Loại bỏ dòng tiêu đề lặp lại hoặc dòng trống
                if not raw_cells or raw_cells[0] == "" or "TT" in raw_cells[0]: 
                    continue
                    
                # Bỏ qua dòng Tổng cộng ở cuối bảng
                if "Tổng" in raw_cells[0] or "Tổng" in raw_cells[1]: 
                    continue
                
                # BẪY CẤU TRÚC: Với bảng của anh, một hàng đầy đủ sau khi rã ô trộn sẽ có đúng 8 ô:
                # [0]: STT, [1]: Nội dung, [2]: Số người, [3]: Thời gian, [4]: Dụng cụ, [5]: Vật tư, [6]: TCKT, [7]: Kết quả
                if len(raw_cells) >= 7:
                    tt = raw_cells[0]
                    name = raw_cells[1]
                    
                    # Nếu là hàng tiêu đề phụ (Ví dụ: "2 Kiểm tra hệ thống nguồn điện:") -> Không có số người/thời gian
                    if raw_cells[2] == "" and raw_cells[3] == "":
                        continue # Bỏ qua dòng tiêu đề nhóm việc, chỉ lấy dòng việc thực tế
                        
                    workers = int(raw_cells[2]) if raw_cells[2].isdigit() else 1
                    duration = int(raw_cells[3]) if raw_cells[3].isdigit() else 0
                    tool = raw_cells[4]
                    material = raw_cells[5]
                    tckt = raw_cells[6]
                    
                    tasks_list.append({
                        "tt": tt,
                        "name": name,
                        "norm_workers": workers,
                        "norm_minutes": duration,
                        "tool": tool,
                        "material": material,
                        "tckt": tckt
                    })
            
            # Nhân bản dữ liệu nạp vào các số phiếu tương ứng (Ví dụ: Phiếu 02, 03)
            for cycle in current_cycles:
                parsed_data.append({
                    "device_name": current_device,
                    "cycle_code": f"Phiếu {cycle}",
                    "tasks": tasks_list
                })
                
    return parsed_data