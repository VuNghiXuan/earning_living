# =====================================================================
# 📋 THÔNG TIN DOANH NGHIỆP & ỨNG DỤNG
# =====================================================================
COMPANY_NAME = "⭐QUÂN CHỦNG HẢI QUÂN"
DEPARTMENT_NAME = "✨Lữ đoàn 189"
APP_NAME = "ÚNG DỰNG QUẢN LÝ"
MISSION_NAME = "Công tác: Bảo quản dự phòng, kiểm sửa định kỳ đối với trang bị Tàu ngầm Kilo 636"

# =====================================================================
# 🎨 BẢNG MÀU GIAO DIỆN CHUẨN CHÍNH QUY (NAVY THEME - FLAT REVOLUTION)
# =====================================================================
# 🟦 Khối cấu trúc Sidebar & Chỉ huy (Vùng tối trang nghiêm)
COLOR_BG_DARK           = "#07162C"  # Xanh biển đêm thẫm - Nền Sidebar gốc
COLOR_BG_BRAND          = "#0A2240"  # Xanh Navy đậm - Khối thông tin đơn vị & Header bảng
COLOR_BG_HEADER         = "#0D2B52"  # Xanh đại dương - Nền của Header chính
COLOR_BG_FOOTER         = "#091F3C"  # Xanh thẫm dịu - Nền của Footer dưới đáy

# ⬜ Khối vùng nội dung làm việc (Vùng sáng phẳng, dịu mắt, tương phản cao)
COLOR_BG_TAB_CONTENT    = "#F8FAFC"  # Nền vùng nội dung Tab: Trắng xám siêu dịu mắt
COLOR_BORDER_LIGHT      = "#E2E8F0"  # Màu viền mảnh thanh lịch cho khung, bảng
COLOR_TEXT_MAIN         = "#1E293B"  # Chữ chính vùng nội dung: Xanh đen tối (Cực rõ nét)
COLOR_TEXT_MUTED        = "#64748B"  # Chữ phụ / Ghi chú: Xanh xám gọn gàng

# 🎗️ Khối màu nhận diện Quân hiệu & Trạng thái
COLOR_PRIMARY           = "#F1C40F"  # Vàng ánh kim Quân hiệu - Chỉ thị hoạt động/Nút bấm chỉ huy
COLOR_TEXT_WHITE        = "#FFFFFF"  # Trắng tinh chỉnh cho vùng Sidebar/Header tối
COLOR_TEXT_DEFAULT      = "#D1DFEE"  # Trắng bạc ánh xanh - Chữ mặc định của Menu Sidebar
COLOR_NAVY_ACTIVE       = "#1D4ED8"  # Xanh biển hoàng gia khi kích hoạt/hover vùng sáng

# 🟢 Khối hành động và trạng thái kỹ thuật
COLOR_SUCCESS           = "#10B981"  # Xanh lá cây - Đạt chuẩn, hoạt động tốt (🟢)
COLOR_WARNING           = "#F59E0B"  # Cam - Cần bảo dưỡng, kiểm tra (🟡)
COLOR_CRITICAL          = "#EF4444"  # Đỏ - Hỏng hóc, dừng hoạt động (🔴)

# 🖱️ Hiệu ứng tương tác trên Sidebar
COLOR_ITEM_HOVER        = "#133765"  # Xanh sáng hơn khi rê chuột (Hover)
COLOR_ITEM_SELECTED     = "#1C4E8C"  # Xanh định vị khi Click chọn (Selected)

# =====================================================================
# 📋 CẤU HÌNH KÍCH THƯỚC CHỮ (FONT SIZE CHÍNH QUY)
# =====================================================================
FONT_SIZE_COMPANY     = "16px"       # Tên đơn vị (QUÂN CHỦNG HẢI QUÂN) - To, trang nghiêm
FONT_SIZE_APP         = "14px"       # Tên phần mềm quản lý
FONT_SIZE_MENU        = "14px"       # Chữ trên các nút điều hướng Sidebar
FONT_SIZE_REGULAR     = "13px"       # Chữ hiển thị thông tin tiêu chuẩn
FONT_SIZE_TABLE       = "13px"       # Cỡ chữ chuẩn cho các ô dữ liệu trong bảng
FONT_SIZE_HEADER_TAB  = "14px"       # Cỡ chữ tiêu đề nhóm QGroupBox trong Tab

# =====================================================================
# 🖌️ STYLESHEET KHUNG TRÊN & KHUNG DƯỚI (HEADER & FOOTER)
# =====================================================================
HEADER_STYLE = f"""
    QFrame {{
        background-color: transparent;
        
        padding: 5px 15px;
    }}
    QLabel {{
        color: {COLOR_TEXT_MAIN};
        font-weight: bold;
        font-size: 14px;
    }}
"""

FOOTER_STYLE = f"""
    QFrame {{
        background-color: transparent;
        
        padding: 5px 15px;
    }}
    QLabel {{
        color: {COLOR_TEXT_MUTED};
        font-size: 11px;
    }}
"""
# =====================================================================
# 🗂️ STYLESHEET CẤU TRÚC SIDEBAR THANH ĐIỀU HƯỚNG MẸ
# =====================================================================
SIDEBAR_CONTAINER_STYLE = f"""
    background-color: {COLOR_BG_DARK}; 
    color: {COLOR_TEXT_WHITE};
    border-right: 1px solid #102A45;
"""

BRAND_FRAME_STYLE = f"""
    QFrame {{
        background-color: {COLOR_BG_BRAND};
        border-bottom: 2px solid {COLOR_PRIMARY};
        padding: 10px;
    }}
    QLabel {{ color: {COLOR_TEXT_WHITE}; }}
"""

TOGGLE_BTN_STYLE = f"""
    QPushButton {{
        background-color: transparent;
        color: {COLOR_TEXT_MUTED};
        border: none;
        font-size: 16px;
        padding: 10px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_ITEM_HOVER};
        color: {COLOR_TEXT_WHITE};
        border-radius: 4px;
    }}
"""

MENU_ITEM_STYLE = f"""
    QPushButton {{
        background-color: transparent;
        color: {COLOR_TEXT_DEFAULT};
        border: none;
        border-left: 4px solid transparent;
        font-size: {FONT_SIZE_MENU};
        font-weight: bold;
        padding: 15px 5px;
        text-align: left;
    }}
    QPushButton:hover {{
        background-color: {COLOR_ITEM_HOVER};
        color: {COLOR_TEXT_WHITE};
    }}
"""

MENU_ITEM_SELECTED_STYLE = f"""
    QPushButton {{
        background-color: {COLOR_ITEM_SELECTED};
        border-left: 4px solid {COLOR_PRIMARY};
        color: {COLOR_PRIMARY};
        font-size: {FONT_SIZE_MENU};
        font-weight: bold;
        padding: 15px 5px;
        text-align: left;
    }}
"""

# =====================================================================
# ⚓ STYLESHEET THANH CHỌN TAB NỘI DUNG (QTabBar) - PHẲNG, TINH TẾ
# =====================================================================
TAB_BAR_STYLE = f"""
    QTabWidget::pane {{
        border: 1px solid {COLOR_BORDER_LIGHT};
        background-color: {COLOR_BG_TAB_CONTENT};
        top: -1px;
    }}
    QTabBar::tab {{
        background-color: #FFFFFF;
        color: {COLOR_TEXT_MUTED};
        font-size: {FONT_SIZE_REGULAR};
        font-weight: 500;
        padding: 10px 20px;
        border: 1px solid {COLOR_BORDER_LIGHT};
        border-bottom: transparent;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 4px;
    }}
    QTabBar::tab:hover {{
        background-color: #F1F5F9;
        color: {COLOR_NAVY_ACTIVE};
    }}
    QTabBar::tab:selected {{
        background-color: {COLOR_BG_TAB_CONTENT};
        color: {COLOR_BG_BRAND};
        font-weight: bold;
        border-top: 3px solid {COLOR_BG_BRAND};
        border-bottom: 1px solid {COLOR_BG_TAB_CONTENT};
    }}
"""

# =====================================================================
# ⚙️ STYLESHEET NỀN SÁNG CHO CÁC KHỐI CHỨC NĂNG TRONG TAB SETTING
# =====================================================================
SETTING_GROUP_BOX_STYLE = f"""
    QGroupBox {{ 
        font-size: {FONT_SIZE_HEADER_TAB}; 
        font-weight: bold; 
        color: {COLOR_BG_BRAND}; 
        border: 1px solid {COLOR_BORDER_LIGHT}; 
        border-radius: 6px;
        margin-top: 15px; 
        padding: 20px; 
        background-color: #FFFFFF;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 5px;
        left: 10px;
    }}
"""

SETTING_INPUT_STYLE = f"""
    QDateEdit, QTimeEdit, QComboBox {{
        background-color: #FFFFFF;
        color: {COLOR_TEXT_MAIN};
        border: 1px solid #CBD5E1;
        padding: 6px 10px;
        border-radius: 4px;
        font-size: {FONT_SIZE_REGULAR};
        min-width: 150px;
    }}
    QDateEdit:hover, QTimeEdit:hover, QComboBox:hover {{
        border: 1px solid {COLOR_NAVY_ACTIVE};
    }}
    QDateEdit:focus, QTimeEdit:focus, QComboBox:focus {{
        border: 1px solid {COLOR_BG_BRAND};
        background-color: #F8FAFC;
    }}
    QDateEdit:read-only, QTimeEdit:read-only {{
        background-color: #F1F5F9;
        color: {COLOR_TEXT_MUTED};
        border: 1px solid {COLOR_BORDER_LIGHT};
    }}
"""

SETTING_LABEL_STYLE = f"color: {COLOR_TEXT_MAIN}; font-size: {FONT_SIZE_REGULAR}; font-weight: 500;"

# =====================================================================
# 📊 STYLESHEET BẢNG BIỂU HỆ THỐNG PHẲNG (QTABLEWIDGET)
# =====================================================================
TABLE_WIDGET_STYLE = f"""
    QTableWidget {{ 
        gridline-color: #E2E8F0; 
        border: 1px solid {COLOR_BORDER_LIGHT}; 
        background-color: #FFFFFF; 
        font-size: {FONT_SIZE_TABLE};
        color: {COLOR_TEXT_MAIN};
        alternate-background-color: #F8FAFC; /* Màu xen kẽ các dòng */
    }}
    QHeaderView::section {{ 
        background-color: #F1F5F9; 
        color: {COLOR_TEXT_MAIN}; 
        font-weight: bold; 
        padding: 8px;
        border: 1px solid {COLOR_BORDER_LIGHT};
    }}
    /* Tùy chỉnh thanh cuộn cho đồng bộ */
    QScrollBar:vertical {{
        width: 12px;
        background: #F1F5F9;
    }}
    QScrollBar:horizontal {{
        height: 12px;
        background: #F1F5F9;
    }}
    QTableWidget::item {{
        padding: 5px; /* Tạo khoảng thở cho nội dung */
    }}
"""

# =====================================================================
# 🛠️ STYLESHEET NÚT BẤM ĐỒNG BỘ (BẢN SẮC, ĐỘ TƯƠNG PHẢN CAO)
# =====================================================================
# 📅 Nút bấm Lập kế hoạch: Vàng chỉ huy cao cấp, chữ tối tương phản nét căng
BTN_PLAN_STYLE = f"""
    QPushButton {{
        background-color: {COLOR_PRIMARY};
        color: {COLOR_BG_DARK};
        font-size: {FONT_SIZE_REGULAR};
        font-weight: bold;
        border: 1px solid #D4AC0D;
        border-radius: 4px;
        padding: 7px 16px;
    }}
    QPushButton:hover {{
        background-color: #F39C12;
        color: #000000;
    }}
    QPushButton:pressed {{
        background-color: #D35400;
        color: {COLOR_TEXT_WHITE};
    }}
"""

# ⚓ Nút bấm Danh mục / Chính quy: Xanh Navy, chữ trắng phẳng thanh lịch
BTN_CATEGORY_STYLE = f"""
    QPushButton {{
        background-color: {COLOR_BG_BRAND};
        color: {COLOR_TEXT_WHITE};
        font-size: {FONT_SIZE_REGULAR};
        font-weight: bold;
        border: 1px solid #133765;
        border-radius: 4px;
        padding: 7px 16px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_ITEM_SELECTED};
        border-color: {COLOR_PRIMARY};
    }}
    QPushButton:pressed {{
        background-color: {COLOR_BG_DARK};
        border-color: #111A24;
    }}
"""

# 📡 Nút bấm Cấu hình / Lưu trữ: Khung viền sắc nét, nhẹ nhàng
BTN_SETTING_STYLE = f"""
    QPushButton {{
        background-color: #FFFFFF;
        color: {COLOR_BG_BRAND};
        font-size: {FONT_SIZE_REGULAR};
        font-weight: bold;
        border: 1px solid {COLOR_BG_BRAND};
        border-radius: 4px;
        padding: 7px 16px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_BG_BRAND};
        color: {COLOR_TEXT_WHITE};
    }}
    QPushButton:pressed {{
        background-color: {COLOR_BG_DARK};
        color: {COLOR_TEXT_WHITE};
    }}
"""

# =====================================================================
# 📐 STYLESHEET BỔ SUNG CHO TRẠNG THÁI SIDEBAR CO GỌN (COLLAPSED)
# =====================================================================
MENU_ITEM_COLLAPSED_STYLE = f"""
    QPushButton {{
        background-color: transparent;
        color: {COLOR_TEXT_DEFAULT};
        border: none;
        border-left: 4px solid transparent;
        font-size: {FONT_SIZE_MENU};
        font-weight: bold;
        padding: 15px 0px;
        text-align: center;
    }}
    QPushButton:hover {{
        background-color: {COLOR_ITEM_HOVER};
        color: {COLOR_TEXT_WHITE};
    }}
"""

MENU_ITEM_COLLAPSED_SELECTED_STYLE = f"""
    QPushButton {{
        background-color: {COLOR_ITEM_SELECTED};
        border-left: 4px solid {COLOR_PRIMARY};
        color: {COLOR_PRIMARY};
        font-size: {FONT_SIZE_MENU};
        font-weight: bold;
        padding: 15px 0px;
        text-align: center;
    }}
"""

