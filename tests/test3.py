from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import QPropertyAnimation, QRect, QEasingCurve

class ResizeAnimation(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background: #2E3440;")

        # ウィジェット
        self.widget = QWidget(self)
        self.widget.setGeometry(100, 100, 100, 100)
        self.widget.setStyleSheet("""
            background-color: #5E81AC;
            border-radius: 10px;
        """)

        # ボタン
        self.toggle_btn = QPushButton("Toggle Resize", self)
        self.toggle_btn.setGeometry(140, 250, 120, 40)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #88C0D0;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_resize)

        # アニメーション設定
        self.animation = QPropertyAnimation(self.widget, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.setStartValue(QRect(100, 100, 100, 100))
        self.animation.setEndValue(QRect(100, 100, 200, 200))

        self.is_resized = False

    def toggle_resize(self):
        if self.is_resized:
            self.animation.setStartValue(QRect(100, 100, 200, 200))
            self.animation.setEndValue(QRect(100, 100, 100, 100))
        else:
            self.animation.setStartValue(QRect(100, 100, 100, 100))
            self.animation.setEndValue(QRect(100, 100, 200, 200))
        self.animation.start()
        self.is_resized = not self.is_resized

# 実行
app = QApplication([])
window = ResizeAnimation()
window.show()
app.exec()
