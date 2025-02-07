from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import QPropertyAnimation, QRect, QEasingCurve

class AnimatedSidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background: #2E3440;")

        # サイドバー
        self.sidebar = QWidget(self)
        self.sidebar.setGeometry(0, 0, 150, 400)
        self.sidebar.setStyleSheet("background: #4C566A; border-right: 2px solid #D8DEE9;")

        # ボタン
        self.toggle_btn = QPushButton("☰", self)
        self.toggle_btn.setGeometry(160, 10, 40, 40)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background: #88C0D0; color: white; border-radius: 10px;
                font-size: 20px; font-weight: bold;
            }
            QPushButton:hover {
                background: #81A1C1;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)

        # アニメーション
        self.animation = QPropertyAnimation(self.sidebar, b"geometry")
        self.animation.setDuration(300)  # ミリ秒
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)

        self.sidebar_open = True

    def toggle_sidebar(self):
        if self.sidebar_open:
            self.animation.setStartValue(QRect(0, 0, 150, 400))
            self.animation.setEndValue(QRect(-150, 0, 150, 400))
        else:
            self.animation.setStartValue(QRect(-150, 0, 150, 400))
            self.animation.setEndValue(QRect(0, 0, 150, 400))

        self.animation.start()
        self.sidebar_open = not self.sidebar_open

# 実行
app = QApplication([])
window = AnimatedSidebar()
window.show()
app.exec()
