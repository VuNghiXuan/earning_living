from datetime import datetime, timedelta

def calculate_timeline(selected_tasks, morning_start="07:00", morning_end="11:30", afternoon_start="13:30", afternoon_end="17:00"):
    """
    Tính toán dải giờ tự động nối tiếp nhau.
    Tự động cắt khúc chuyển ca trưa và cảnh báo nếu tràn ca chiều.
    """
    fmt = "%H:%M"
    try:
        m_start = datetime.strptime(morning_start, fmt)
        m_end = datetime.strptime(morning_end, fmt)
        a_start = datetime.strptime(afternoon_start, fmt)
        a_end = datetime.strptime(afternoon_end, fmt)
    except Exception:
        m_start = datetime.strptime("07:00", fmt)
        m_end = datetime.strptime("11:30", fmt)
        a_start = datetime.strptime("13:30", fmt)
        a_end = datetime.strptime("17:00", fmt)
        
    current_time = m_start
    results = []
    
    for task in selected_tasks:
        duration_mins = int(task.get("norm_minutes", 0))
        if duration_mins <= 0:
            results.append("-")
            continue
            
        duration = timedelta(minutes=duration_mins)
        task_start = current_time
        task_end = current_time + duration
        
        # Tình huống 1: Bắt đầu ở ca sáng nhưng kết thúc tràn qua giờ nghỉ trưa
        if task_start < m_end and task_end > m_end:
            minutes_in_morning = (m_end - task_start).seconds // 60
            minutes_left = duration_mins - minutes_in_morning
            task_end = a_start + timedelta(minutes=minutes_left)
            
            # Kiểm tra xem phần còn lại có bị tràn luôn ca chiều không
            if task_end > a_end:
                display_range = f"{task_start.strftime(fmt)}-{m_end.strftime(fmt)} & {a_start.strftime(fmt)}-{a_end.strftime(fmt)} (Tràn ca chiều)"
                current_time = a_end
            else:
                display_range = f"{task_start.strftime(fmt)}-{m_end.strftime(fmt)} & {a_start.strftime(fmt)}-{task_end.strftime(fmt)}"
                current_time = task_end
                
        # Tình huống 2: Mốc bắt đầu rơi trúng hoặc sau giờ nghỉ trưa
        elif m_end <= task_start < a_start:
            task_start = a_start
            task_end = task_start + duration
            if task_end > a_end:
                display_range = f"{task_start.strftime(fmt)}-{a_end.strftime(fmt)} (Tràn ca chiều)"
                current_time = a_end
            else:
                display_range = f"{task_start.strftime(fmt)}-{task_end.strftime(fmt)}"
                current_time = task_end
                
        # Tình huống 3: Nằm trọn vẹn trong ca sáng hoặc ca chiều
        else:
            if task_end > a_end:
                display_range = f"{task_start.strftime(fmt)}-{a_end.strftime(fmt)} (Tràn ca chiều)"
                current_time = a_end
            else:
                display_range = f"{task_start.strftime(fmt)}-{task_end.strftime(fmt)}"
                current_time = task_end
            
        results.append(display_range)
        
    return results