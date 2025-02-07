from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton, QGridLayout
from PySide6.QtCore import Qt
import sys
import os
import json
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import threading

class ParameterWidget(QWidget):
    def __init__(self, name, address, value, osc_client):
        super().__init__()
        self.name = name
        self.address = address
        self.osc_client = osc_client
        self.mode = "send" # or receive

        layout = QGridLayout()
        self.label = QLabel(f"{self.name}: {value:.2f}")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(int(value * 100))
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.on_slider_change)

        self.mode_button = QPushButton("Send Mode")
        self.mode_button.clicked.connect(self.toggle_mode)

        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.slider, 1, 0, 1, 2)
        layout.addWidget(self.mode_button, 0, 1)
        self.setLayout(layout)

    def on_slider_change(self, value):
        if self.mode == "send":
            normalized_value = value / 100.0
            self.label.setText(f"{self.name}: {normalized_value:.2f}")
            self.osc_client.send_message(self.address, normalized_value)

    def toggle_mode(self):
        if self.mode == "send":
            self.mode = "receive"
            self.mode_button.setText("Receive Mode")
        else:
            self.mode = "send"
            self.mode_button.setText("Send Mode")

    def update_value(self, value):
        self.slider.setValue(int(value * 100))
        self.label.setText(f"{self.name}: {value:.2f}")

class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.osc_client = SimpleUDPClient("127.0.0.1", 9000)
        self.parameters = []

        # 最初にレイアウトを作成
        self.setLayout(QGridLayout())

        self.loadData()

        self.dispatcher = Dispatcher()
        self.dispatcher.map("*", self.receive_osc_data)
        self.server = BlockingOSCUDPServer(("127.0.0.1", 9001), self.dispatcher)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

    def loadData(self):
        file_path = os.path.join(os.path.dirname(sys.argv[0]), "data.json")
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                self.data = json.load(f)
        except Exception as e:
            self.data = {"params": [
                {
                    "name" : "Json Load Error",
                    "address" : "/avatar/parameters/Hair001",
                    "value" : 0.0
                }
            ]}
        self.rebuildUI()

    def rebuildUI(self):
        while self.layout().count():
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        layout = self.layout()

        # リロードボタンを追加
        reload_button = QPushButton("Reload Data")
        reload_button.clicked.connect(self.loadData)
        layout.addWidget(reload_button, 0, 0, 1, 2)

        self.parameters = []
        for index, param in enumerate(self.data.get("params", [])):
            param_widget = ParameterWidget(param["name"], param["address"], param["value"], self.osc_client)
            self.parameters.append(param_widget)

            row = index % 10
            column = index // 10
            layout.addWidget(param_widget, row + 1, column)  # +1 はリロードボタンの行を確保するため

        self.setWindowTitle("Hand Tracking Sliders")

    def receive_osc_data(self, address, *args):
        for param in self.parameters:
            if param.address == address and param.mode == "receive":
                param.update_value(args[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainView()
    ex.show()
    sys.exit(app.exec())
