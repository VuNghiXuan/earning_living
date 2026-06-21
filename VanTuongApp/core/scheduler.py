from datetime import datetime, timedelta

def calculate_timeline(tasks, morning_start="07:00", morning_end="11:30", afternoon_start="13:30", afternoon_end="17:00"):
    """
    Tính toán dải giờ tự động nối tiếp cho các đầu việc được chọn.
    Tự động ngắt giờ và chuyển sang ca chiều nếu dính giờ nghỉ trưa.
    """
    time_ranges = []
    
    fmt = "%H:%M"
    m_start = datetime.strptime(morning_start, fmt)
    m_end = datetime.strptime(morning_end, fmt)
    a_start = datetime.strptime(afternoon_start, fmt)
    a_end = datetime.strptime(afternoon_end, fmt)
    
    current_time = m_start
    
    for task in tasks:
        # Lấy định mức thời gian chạy của tác vụ
        duration = timedelta(minutes=task["norm_minutes"])
        
        # Nếu đang trong giờ nghỉ trưa hoặc sát giờ nghỉ, đẩy thời gian bắt đầu sang đầu ca chiều
        if current_time >= m_end and current_time < a_start:
            current_time = a_start
            
        start_str = current_time.strftime(fmt)
        end_time = current_time + duration
        
        # Lập trình xử lý tràn ca: Nếu thời gian làm việc vượt quá mốc giờ nghỉ trưa
        if current_time < m_end and end_time > m_end:
            overtime = end_time - m_end
            current_time = a_start + overtime
        else:
            current_time = end_time
            
        end_str = current_time.strftime(fmt)
        time_ranges.append(f"{start_str} - {end_str}")
        
    return time_ranges