from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel, QPushButton
from PySide6.QtCore import Qt
import sys
import os
import json
from pythonosc.udp_client import SimpleUDPClient

class HandSliderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.sliders = []
        self.labels = []
        self.osc_client = SimpleUDPClient("127.0.0.1", 9000)  # 送信先のIPとポートを設定
        self.loadData()

    def loadData(self):
        file_path = os.path.join(os.path.dirname(__file__), "data.json")
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                self.data = json.load(f)
        except Exception as e:
            print("Error. Using default values.")
            self.data = {"params": []}
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.sliders.clear()
        self.labels.clear()

        # UIリロードボタンの追加
        # reload_button = QPushButton("Reload Data")
        # reload_button.clicked.connect(self.loadData)
        # layout.addWidget(reload_button)

        for i, param in enumerate(self.data.get("params", [])):
            label = QLabel(f'{param["name"]}: {param["value"]:.2f}')
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(int(param["value"] * 100))
            slider.setTickInterval(1)
            slider.valueChanged.connect(lambda value, lbl=label, addr=param["address"]: self.update_label(value, lbl, addr))
            
            self.labels.append(label)
            self.sliders.append(slider)
            layout.addWidget(label)
            layout.addWidget(slider)
        
        self.setLayout(layout)
        self.setWindowTitle('VRC OSC Sliders')

    def update_label(self, value, label, address):
        normalized_value = value / 100.0
        label.setText(f'{label.text().split(":")[0]}: {normalized_value:.2f}')
        self.send_osc_data(address, normalized_value)
    
    def send_osc_data(self, address, value):
        self.osc_client.send_message(address, value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HandSliderWidget()
    ex.show()
    sys.exit(app.exec())
