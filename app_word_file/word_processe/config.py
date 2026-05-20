# word_processe/config.py

APP_CONFIG = {
    "title": "VĂN TƯỜNG APPS - SYSTEM PORTAL",
    "geometry": "1150x700",
    "theme": {
        "appearance_mode": "System",
        "sidebar_bg": "#102833",
        "logo_color": "#D4AF37",
        "text_primary": "#ffffff",
        "text_muted": "gray",
        "text_inactive": "#ced4da",
        "border_color": "#2b5063",
        "hover_color_dark": "#1e2e38",
        "accent_color": "#217346",
        "accent_hover": "#1e623b",
        "tab_selected": "#217346",
        "tab_selected_hover": "#1e623b",
        "tab_unselected_hover": "#e9ecef",
        "content_border_color": "#dee2e6"
    },
    "sidebar_buttons": [
        {"id": "btn_func_1", "text": "📊 Xử lý file word", "is_active": True},
        {"id": "btn_func_2", "text": "📖 Tri thức AI", "is_active": False},
        {"id": "btn_func_3", "text": "⚙️ Cấu hình hệ thống", "is_active": False}
    ],
    "tabs": [
        {
            "id": "tab_import",
            "title": "Nhập & Xử lý File Word",
            "layout_method": "_build_import_tab_layout"
        },
        {
            "id": "tab_ai",
            "title": "Phân Tích Nghiệp Vụ",
            "layout_method": "_build_placeholder_tab"
        }
    ]
}