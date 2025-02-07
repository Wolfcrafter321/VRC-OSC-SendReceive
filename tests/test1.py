from PySide6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout
from PySide6.QtCore import Qt, QMimeData, QPoint, QPropertyAnimation
from PySide6.QtGui import QDrag


class DraggableLabel(QLabel):
    """ドラッグ可能なラベル"""
    def __init__(self, row, col, parent=None):
        super().__init__(f"{row},{col}", parent)
        self.row = row
        self.col = col
        self.setStyleSheet("background: lightblue; border: 1px solid black; padding: 10px;")
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(60, 60)  # サイズを統一

    def mousePressEvent(self, event):
        """ドラッグ開始"""
        if event.button() == Qt.LeftButton:
            self.setWindowOpacity(0.5)  # 半透明にする
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec(Qt.MoveAction)
            self.setWindowOpacity(1.0)  # ドロップ後に元の透明度に戻す


class DragDropGrid(QWidget):
    """QGridLayout 上でドラッグ＆ドロップ可能なウィジェット"""
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # 3×3 のグリッドに番号付きのラベルを配置
        self.widgets = {}  # { (row, col): widget }
        for i in range(3):
            for j in range(3):
                label = DraggableLabel(i, j, self)
                self.layout.addWidget(label, i, j)
                self.widgets[(i, j)] = label

    def dragEnterEvent(self, event):
        """ドラッグされた時"""
        event.accept()

    def dropEvent(self, event):
        """ドロップされた時"""
        pos = event.position().toPoint()
        dragged_widget = event.source()

        if isinstance(dragged_widget, DraggableLabel):
            target_row, target_col = self.get_grid_position(pos)
            if target_row is not None and target_col is not None:
                self.swap_widgets(dragged_widget, target_row, target_col)

    def get_grid_position(self, pos: QPoint):
        """マウス位置からグリッドのセルを計算"""
        for i in range(self.layout.rowCount()):
            for j in range(self.layout.columnCount()):
                rect = self.layout.cellRect(i, j)
                if rect.contains(pos):
                    return i, j
        return None, None

    def swap_widgets(self, widget, target_row, target_col):
        """ウィジェットの位置を交換（アニメーション付き）"""
        source_row, source_col = widget.row, widget.col

        if (target_row, target_col) in self.widgets:
            target_widget = self.widgets[(target_row, target_col)]

            # アニメーションを適用して位置を変更
            self.animate_swap(widget, target_widget)

            # 位置を交換
            widget.row, widget.col = target_row, target_col
            target_widget.row, target_widget.col = source_row, source_col
            self.widgets[(source_row, source_col)], self.widgets[(target_row, target_col)] = target_widget, widget

            # ラベルのテキストを更新
            widget.setText(f"{widget.row},{widget.col}")
            target_widget.setText(f"{target_widget.row},{target_widget.col}")

    def animate_swap(self, widget1, widget2):
        """2つのウィジェットの位置をアニメーションで交換"""
        pos1 = widget1.pos()
        pos2 = widget2.pos()

        anim1 = QPropertyAnimation(widget1, b"pos")
        anim1.setDuration(300)  # 300ms
        anim1.setStartValue(pos1)
        anim1.setEndValue(pos2)

        anim2 = QPropertyAnimation(widget2, b"pos")
        anim2.setDuration(300)
        anim2.setStartValue(pos2)
        anim2.setEndValue(pos1)

        anim1.start()
        anim2.start()


if __name__ == "__main__":
    app = QApplication([])
    window = DragDropGrid()
    window.show()
    app.exec()
