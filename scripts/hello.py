from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PySide6.QtCore import Qt
import sys

class HandSliderWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.sliders = []
        self.labels = []

        for i in range(10):  # 右手5本 + 左手5本
            label = QLabel(f'{"R" if i < 5 else "L"} Finger {i+1}: 0.00')
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(0)
            slider.setTickInterval(1)
            slider.valueChanged.connect(lambda value, lbl=label: self.update_label(value, lbl))

            self.labels.append(label)
            self.sliders.append(slider)
            layout.addWidget(label)
            layout.addWidget(slider)

        self.setLayout(layout)
        self.setWindowTitle('Hand Tracking Sliders')

    def update_label(self, value, label):
        label.setText(f'{label.text().split(":")[0]}: {value / 100:.2f}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HandSliderWidget()
    ex.show()
    sys.exit(app.exec())
