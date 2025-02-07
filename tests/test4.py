from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtCore import QPropertyAnimation, QRect, QEasingCurve

class BounceAnimation(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background: #2E3440;")

        # ウィジェット
        self.widget = QWidget(self)
        self.widget.setGeometry(50, 50, 100, 100)
        self.widget.setStyleSheet("""
            background-color: #81A1C1;
            border-radius: 10px;
        """)

        # ボタン
        self.toggle_btn = QPushButton("Move & Bounce", self)
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
        self.toggle_btn.clicked.connect(self.toggle_move)

        # アニメーション設定
        self.animation = QPropertyAnimation(self.widget, b"geometry")
        self.animation.setDuration(700)
        self.animation.setEasingCurve(QEasingCurve.OutBounce)
        self.animation.setStartValue(QRect(50, 50, 100, 100))
        self.animation.setEndValue(QRect(250, 50, 100, 100))

    def toggle_move(self):
        self.animation.start()

# 実行
app = QApplication([])
window = BounceAnimation()
window.show()
app.exec()
