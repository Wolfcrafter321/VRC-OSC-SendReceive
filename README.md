# VRC-OSC-SendReceive
Wolfy's VRChat OSC Tool 🐺

![SampleImage](/image/sample.png)

## What is This?　これは何?
You can send custom parameters to VRChat.
Just this.

このツールを使うことで、VRChatへパラメーターを送受信することができます。

それだけ。

Pythonで動き、Pyinstallerで実行することでexeとしてアプリケーションにも出来ます。

## Python Modules
### Required
- PySide6
- python-osc

### Optional
- PySide6-Examples

## Installation
~~~
git clone this-repository.
cd VRC-OSC-SendReceive
py -m venv dev_env
dev_env\Scripts\activate.bat
pip install -r pip_requirements.txt
# optional
# pip install pyinstaller
# pyinstaller --onefile --noconsole scripts\ParametersWidget.py
~~~

#### Note
This Test contains ChatGPTs generated content.