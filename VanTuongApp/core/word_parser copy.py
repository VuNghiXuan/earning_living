import os
import re
from docx import Document

def parse_maintenance_word_file(file_path):
    if not os.path.exists(file_path):
        return []

    doc = Document(file_path)
    elements = []
    for p in doc.paragraphs:
        if p.text.strip(): 
            elements.append(('text', p.text.strip()))
    for t in doc.tables:
        elements.append(('table', t))

    parsed_blocks = []
    current_device = ""
    current_cycle_code = "Phiếu 01"
    current_cycle_name = "Bảo quản định kỳ"

    for el_type, el_content in elements:
        if el_type == 'text':
            text_line = el_content
            device_match = re.search(r'(?:TÊN\s*TRANG\s*BỊ\s*:\s*|\d+\.\s+)(.+)', text_line, re.IGNORECASE)
            if device_match and "PHIẾU" not in text_line.upper():
                temp_name = device_match.group(1).strip().replace(' ', ' ')
                if len(temp_name) > 5:
                    current_device = temp_name
                continue
                
            cycle_match = re.search(r'PHIẾU\s*SỐ\s*:\s*([\d\s,–\-]+)(?:\(([^)]+)\))?', text_line, re.IGNORECASE)
            if cycle_match:
                current_cycle_code = f"Phiếu {cycle_match.group(1).strip()}"
                current_cycle_name = cycle_match.group(2).strip() if cycle_match.group(2) else "Bảo dưỡng định kỳ"

        elif el_type == 'table':
            table = el_content
            if len(table.rows) < 2 or len(table.columns) < 5: 
                continue

            tasks = []
            prev_tool, prev_material, prev_tckt = "", "", ""

            for row in table.rows:
                cells = row.cells
                if not cells or len(cells) < 5: 
                    continue
                
                tt = cells[0].text.strip()
                if not re.match(r'^\d+(\.\d+)?$', tt): 
                    continue

                name = cells[1].text.strip().replace('\n', ' ')
                
                try:
                    w_txt = cells[2].text.strip()
                    workers = int(re.search(r'\d+', w_txt).group()) if w_txt else 1
                except: workers = 1

                try:
                    m_txt = cells[3].text.strip()
                    minutes = int(re.search(r'\d+', m_txt).group()) if m_txt else 0
                except: minutes = 0

                tool = cells[4].text.strip() if len(cells) > 4 else ""
                material = cells[5].text.strip() if len(cells) > 5 else ""
                tckt = cells[6].text.strip() if len(cells) > 6 else ""

                if tool in ["//", "-", ""]: tool = prev_tool
                else: prev_tool = tool
                
                if material in ["//", "-", ""]: material = prev_material
                else: prev_material = material
                
                if tckt in ["//", "-", ""]: tckt = prev_tckt
                else: prev_tckt = tckt

                tasks.append({
                    "tt": tt, "name": name, "norm_workers": workers,
                    "norm_minutes": minutes, "tool": tool, "material": material, "tckt": tckt
                })

            if tasks and current_device:
                raw_nums = re.findall(r'\d+', current_cycle_code)
                cycle_list = [f"Phiếu {int(n)}" for n in raw_nums] if raw_nums else [current_cycle_code]

                for c_code in cycle_list:
                    parsed_blocks.append({
                        "device_name": current_device, "cycle_code": c_code,
                        "cycle_name": current_cycle_name, "tasks": tasks
                    })
                    
    return parsed_blocks