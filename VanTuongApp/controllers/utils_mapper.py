# def map_row_to_dict(row_data, config):
#     data_dict = {}
#     cols = config["columns"]      # Định nghĩa UI: {"TT": {"idx": 3...}}
#     db_fields = config["db_fields"] # Ánh xạ: {"TT": "tt"}
    
#     # Duyệt qua các key (TT, TASK, WORKERS...)
#     for key, col_info in cols.items():
#         ui_idx = col_info["idx"]
#         db_key = db_fields.get(key)
        
#         if ui_idx < len(row_data) and db_key:
#             data_dict[db_key] = str(row_data[ui_idx])
            
#     return data_dict

def map_row_to_dict(row, config):
    mapping = {}
    for key, info in config["columns"].items():
        idx = info["idx"]
        # Lấy dữ liệu từ row, nếu thiếu thì để trống
        mapping[key] = row[idx] if idx < len(row) else ""
    return mapping