# styles/table_styles.py
COLOR_BORDER_LIGHT = "#CBD5E1"
COLOR_TEXT_MAIN = "#1E293B"
FONT_SIZE_TABLE = "14px"

TABLE_WIDGET_STYLE = f"""
    QTableWidget {{ 
        gridline-color: #E2E8F0; 
        border: 1px solid {COLOR_BORDER_LIGHT}; 
        background-color: #FFFFFF; 
        font-size: {FONT_SIZE_TABLE};
        color: {COLOR_TEXT_MAIN};
    }}
    QHeaderView::section {{ 
        background-color: #F1F5F9; 
        color: {COLOR_TEXT_MAIN}; 
        font-weight: bold; 
        padding: 8px;
        border: 1px solid {COLOR_BORDER_LIGHT};
    }}
"""