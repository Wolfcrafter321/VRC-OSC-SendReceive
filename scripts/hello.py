from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PySide6.QtCore import Qt
import sys
from pythonosc.udp_client import SimpleUDPClient

class HandSliderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.osc_client = SimpleUDPClient("127.0.0.1", 9000)  # 送信先のIPとポートを設定

    def initUI(self):
        layout = QVBoxLayout()
        self.sliders = []
        self.labels = []
        
        for i in range(10):  # 右手5本 + 左手5本
            label = QLabel(f'Finger {i+1}: 0.00')
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(0)
            slider.setTickInterval(1)
            slider.valueChanged.connect(lambda value, lbl=label, idx=i: self.update_label(value, lbl, idx))
            
            self.labels.append(label)
            self.sliders.append(slider)
            layout.addWidget(label)
            layout.addWidget(slider)
        
        self.setLayout(layout)
        self.setWindowTitle('Hand Tracking Sliders')

    def update_label(self, value, label, index):
        normalized_value = value / 100.0
        label.setText(f'{label.text().split(":")[0]}: {normalized_value:.2f}')
        self.send_osc_data(index, normalized_value)
    
    def send_osc_data(self, index, value):
        address = f"/avatar/parameters/Finger{index+1}"
        self.osc_client.send_message(address, value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HandSliderWidget()
    ex.show()
    sys.exit(app.exec())
