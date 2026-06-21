from PySide6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QStyledItemDelegate
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QStyleOptionViewItem

class MaxWidthDelegate(QStyledItemDelegate):
    """Delegate để giới hạn chiều rộng hiển thị tối đa 250px"""
    def sizeHint(self, option: QStyleOptionViewItem, index):
        size = super().sizeHint(option, index)
        if size.width() > 500:
            size.setWidth(500)
        return size

class CustomTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # 1. Bật thanh cuộn
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 2. Cấu hình xuống dòng (Word Wrap)
        self.setWordWrap(True)
        self.setTextElideMode(Qt.TextElideMode.ElideRight)

        # 3. Cấu hình Header
        header = self.horizontalHeader()
        # Dùng ResizeToContents để nó co dãn theo chữ
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        # 4. Gắn Delegate để giới hạn chiều rộng
        delegate = MaxWidthDelegate(self)
        self.setItemDelegate(delegate)

        # 5. Cấu hình hàng
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def apply_style(self, style_sheet):
        self.setStyleSheet(style_sheet)

    def resizeEvent(self, event):
        """Đảm bảo bảng cập nhật khi resize cửa sổ"""
        super().resizeEvent(event)
        # Giới hạn thủ công từng cột sau khi nạp dữ liệu nếu cần
        for i in range(self.columnCount()):
            if self.columnWidth(i) > 500:
                self.setColumnWidth(i, 500)