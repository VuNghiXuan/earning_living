NORMS_TABLE_CONFIG = {
    "columns": {
        "TT": {"idx": 3, "label": "TT"},
        "TASK": {"idx": 4, "label": "Nội dung"},
        "WORKERS": {"idx": 5, "label": "Nhân công"},
        "MINUTES": {"idx": 6, "label": "Thời gian"},
        "TOOL": {"idx": 7, "label": "Dụng cụ"},
        "MATERIAL": {"idx": 8, "label": "Vật tư"},
        "TCKT": {"idx": 9, "label": "TCKT"},
        "RESULT": {"idx": 10, "label": "Kết quả"},
        "DEVICE": {"idx": 0, "label": "Máy/Thiết bị"},
        "CYCLE": {"idx": 1, "label": "Phiếu bảo dưỡng"},
        "TECH": {"idx": 2, "label": "Phiếu công nghệ"}
    },
    # Cần thêm lại key này để map_row_to_dict không bị lỗi
    "db_fields": {
        "DEVICE": "device_name",
        "CYCLE": "cycle_code",
        "TECH": "tech_name",
        "TT": "tt",
        "TASK": "task_name",
        "WORKERS": "workers",
        "MINUTES": "minutes",
        "TOOL": "tool",
        "MATERIAL": "material",
        "TCKT": "tckt",
        "RESULT": "result"
    }
}