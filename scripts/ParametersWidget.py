from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton, QGridLayout, QSpinBox
from PySide6.QtCore import Qt
import sys
import os
import json
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import threading


class ParameterWidget(QWidget):
    def __init__(self, data, osc_client):
        super().__init__()
        self.name = data["name"]
        self.address = data["address"]
        self.value = data["value"]
        self.data_type = data.get("type", "float")  # デフォルトはfloat
        self.mode = data.get("mode", "send")  # JSONのmodeを取得 (デフォルト: send)
        self.osc_client = osc_client

        layout = QGridLayout()
        self.label = QLabel(f"{self.name}: {self.value}")

        if self.data_type == "float":
            self.slider = QSlider(Qt.Horizontal)
            self.slider.setMinimum(0)
            self.slider.setMaximum(100)
            self.slider.setValue(int(self.value * 100))
            self.slider.setTickInterval(1)
            self.slider.valueChanged.connect(self.on_slider_change)
            layout.addWidget(self.slider, 1, 0, 1, 2)

        elif self.data_type == "int":
            self.spinbox = QSpinBox()
            self.spinbox.setMinimum(0)
            self.spinbox.setMaximum(100)
            self.spinbox.setValue(int(self.value))
            self.spinbox.valueChanged.connect(self.on_spinbox_change)
            layout.addWidget(self.spinbox, 1, 0, 1, 2)

        elif self.data_type == "bool":
            self.button = QPushButton("OFF" if not self.value else "ON")
            self.button.setCheckable(True)
            self.button.setChecked(bool(self.value))
            self.button.clicked.connect(self.on_button_toggle)
            layout.addWidget(self.button, 1, 0, 1, 2)

        # modeボタンを初期設定
        self.mode_button = QPushButton()
        self.mode_button.clicked.connect(self.toggle_mode)
        self.update_mode_button()  # 初期状態を反映

        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.mode_button, 0, 1)
        self.setLayout(layout)

    def update_mode_button(self):
        """モードボタンの表示を更新"""
        if self.mode == "send":
            self.mode_button.setText("Send Mode")
        else:
            self.mode_button.setText("Receive Mode")

    def toggle_mode(self):
        """モードを切り替え"""
        self.mode = "receive" if self.mode == "send" else "send"
        self.update_mode_button()

    def on_slider_change(self, value):
        if self.mode == "send":
            normalized_value = value / 100.0
            self.label.setText(f"{self.name}: {normalized_value:.2f}")
            self.osc_client.send_message(self.address, normalized_value)

    def on_spinbox_change(self, value):
        if self.mode == "send":
            self.label.setText(f"{self.name}: {value}")
            self.osc_client.send_message(self.address, int(value))

    def on_button_toggle(self):
        if self.mode == "send":
            new_state = self.button.isChecked()
            self.button.setText("ON" if new_state else "OFF")
            self.label.setText(f"{self.name}: {new_state}")
            self.osc_client.send_message(self.address, bool(new_state))

    def update_value(self, value):
        """受信モード時に値を更新"""
        if self.data_type == "float":
            self.slider.setValue(int(value * 100))
            self.label.setText(f"{self.name}: {value:.2f}")
        elif self.data_type == "int":
            self.spinbox.setValue(int(value))
            self.label.setText(f"{self.name}: {value}")
        elif self.data_type == "bool":
            self.button.setChecked(bool(value))
            self.button.setText("ON" if value else "OFF")
            self.label.setText(f"{self.name}: {value}")

    def get_value(self):
        """現在の値を取得"""
        if self.data_type == "float":
            return self.slider.value() / 100.0
        elif self.data_type == "int":
            return self.spinbox.value()
        elif self.data_type == "bool":
            return self.button.isChecked()


class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.osc_client = SimpleUDPClient("127.0.0.1", 9000)
        self.parameters = []

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
                    "name": "Json Load Error",
                    "address": "/avatar/parameters/Hair001",
                    "value": 0.0,
                    "type": "float"
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

        # Reloadボタン
        reload_button = QPushButton("Reload Data")
        reload_button.clicked.connect(self.loadData)
        layout.addWidget(reload_button, 0, 0, 1, 2)

        # Send Allボタン
        send_all_button = QPushButton("Send All")
        send_all_button.clicked.connect(self.send_all_parameters)
        layout.addWidget(send_all_button, 1, 0, 1, 2)

        self.parameters = []
        for index, param in enumerate(self.data.get("params", [])):
            param_widget = ParameterWidget(param, self.osc_client)
            self.parameters.append(param_widget)

            row = index % 10
            column = index // 10
            layout.addWidget(param_widget, row + 2, column)  # +2 はボタン2つ分のスペース確保

        self.setWindowTitle("Hand Tracking Sliders")

    def send_all_parameters(self):
        """すべての Send Mode のパラメーターを送信"""
        for param in self.parameters:
            if param.mode == "send":
                value = param.get_value()
                self.osc_client.send_message(param.address, value)
                # print(f"Sent: {param.address} -> {value}")

    def receive_osc_data(self, address, *args):
        for param in self.parameters:
            if param.address == address and param.mode == "receive":
                param.update_value(args[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainView()
    ex.show()
    sys.exit(app.exec())
