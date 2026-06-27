from PySide6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QStyledItemDelegate, QApplication, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStyleOptionViewItem

class MaxWidthDelegate(QStyledItemDelegate):
    """Delegate giúp giới hạn chiều rộng nhưng vẫn cho phép sửa nội dung"""
    def createEditor(self, parent, option, index):
        # Trả về một QLineEdit để bảng sử dụng khi vào chế độ edit
        editor = QLineEdit(parent)
        return editor

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        if size.width() > 250:
            size.setWidth(250)
        return size

class CustomTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.apply_default_style() # Gọi hàm áp dụng style ngay khi khởi tạo

    def setup_ui(self):
        # 1. Cấu hình chọn: Chọn từng ô, cho phép bôi đen text để copy
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        
        # 2. MỞ KHÓA: Cho phép click đúp hoặc gõ phím để sửa nội dung
        self.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked | 
            QAbstractItemView.EditTrigger.SelectedClicked |
            QAbstractItemView.EditTrigger.AnyKeyPressed
        )

        # 3. Bật màu xen kẽ
        self.setAlternatingRowColors(True)

        # 4. Cấu hình hiển thị
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setWordWrap(True)
        self.setTextElideMode(Qt.TextElideMode.ElideRight)

        # 5. Gán Delegate đã sửa để giới hạn chiều rộng cột
        delegate = MaxWidthDelegate(self)
        self.setItemDelegate(delegate)
        
        # 6. Cấu hình Header
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        # Tắt viền focus xanh mặc định của Windows
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def apply_default_style(self):
        """Thiết lập phong cách giống bảng tính Excel chuyên nghiệp"""
        style = """
            QTableWidget { 
                gridline-color: #e0e0e0; 
                background-color: #ffffff; 
                alternate-background-color: #f2f7f9; 
                border: 1px solid #d1d1d1;
                selection-background-color: transparent; /* Tắt mặc định để kiểm soát bằng item:selected */
            }
            QHeaderView::section { 
                background-color: #417690; 
                color: #ffffff; 
                padding: 8px; 
                border: 1px solid #355d71; 
                font-weight: bold;
                font-size: 13px;
            }
            QTableWidget::item { 
                padding: 5px; 
            }
            /* Hiệu ứng di chuột vào (Hover) - Cốt lõi của giao diện Django */
            QTableWidget::item:hover {
                background-color: #d1e5ef; 
                color: #000000;
            }
            /* Khi hàng được chọn */
            QTableWidget::item:selected {
                background-color: #79aec8; 
                color: #ffffff;
            }
        """
        self.setStyleSheet(style)

    def apply_style(self, style_sheet):
        # Hàm này để override style nếu cần, nhưng tạm thời chúng ta dùng default
        pass

    # def keyPressEvent(self, event):
    #     """
    #     Xử lý phím tắt:
    #     - Esc: Thoát chế độ edit ô
    #     - Ctrl+C: Copy dữ liệu vùng chọn
    #     """
    #     if event.key() == Qt.Key_Escape and self.state() == QAbstractItemView.State.EditingState:
    #         self.closePersistentEditor(self.currentItem())
    #         return

    #     if event.matches(event.StandardKey.Copy):
    #         if self.state() == QAbstractItemView.State.EditingState:
    #             # Nếu đang edit text, để text tự copy (Ctrl+C trong ô)
    #             super().keyPressEvent(event)
    #         else:
    #             # Nếu không edit, dùng hàm copy tùy chỉnh
    #             self.copy_selection_to_clipboard()
    #     else:
    #         # Cho phép gõ phím, xóa để sửa
    #         super().keyPressEvent(event)

    def copy_selection_to_clipboard(self):
        """Copy dữ liệu vùng chọn vào clipboard"""
        selection = self.selectedIndexes()
        if not selection: return
        
        # Sắp xếp để đảm bảo copy đúng thứ tự
        rows = sorted(set(index.row() for index in selection))
        cols = sorted(set(index.column() for index in selection))
        
        result = ""
        for row in rows:
            row_data = []
            for col in cols:
                item = self.item(row, col)
                row_data.append(item.text() if item else "")
            # Nối các ô bằng phím Tab, các hàng bằng phím Enter
            result += "\t".join(row_data) + "\n"
        
        # Gửi dữ liệu vào clipboard của hệ thống
        QApplication.clipboard().setText(result)