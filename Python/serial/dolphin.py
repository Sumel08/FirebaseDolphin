import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication
from PyQt5.QtGui import QFont
from PyQt5 import QtCore as core
import SerialManager
import json

import datetime
import requests


class Example(QWidget):

    isConnected = False
    serial_connection = SerialManager.Manager()

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        self.btn = QPushButton('Button', self)
        self.btn.setToolTip('This is a <b>QPushButton</b> widget')
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(50, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')
        self.show()
        self.set_signals()

    def set_signals(self):
        self.btn.clicked.connect(self.connect_serial_port)

    def connect_serial_port(self):
        if not self.isConnected:
            print(self.serial_connection.serial_ports())
            # self.serial_connection.init_port("COM3", 9600)  # -> WINDOWS
            self.serial_connection.init_port("/dev/ttyACM0", 9600) # -> LINUX
            self.serial_connection.open_port()
            self.serial_connection.rx_buffer.connect(self.data_received)
            # self.btnSend.clicked.connect(self.handle_send)
            self.serial_connection.start()
            self.btn.setText("Desconectar")
            self.isConnected = True
        else:
            self.serial_connection.terminate()
            self.serial_connection.close_port()
            self.btn.setText("Conectar")
            self.isConnected = False

    @core.pyqtSlot(bytes)
    def data_received(self, data):
        data = data.decode('UTF-8')
        try:
            data = json.loads(data)
            print(data)
            date = datetime.datetime.now()
            self.new_temperature(date, data.get('temperature'))
            self.new_humidity(date, data.get('humidity'))
        except json.decoder.JSONDecodeError as err:
            print(data)
            print(str(err))

    def new_temperature(self, date, value):

        date_string = str(date.date())
        time_string = str(date.time()).split('.')[0]

        data = {
            'fields': {
                'date': {
                    'stringValue': '{} {}'.format(date_string, time_string)
                },
                'value': {
                    'stringValue': str(value)
                }
            }
        }

        url = "https://firestore.googleapis.com/v1beta1/projects/example-dba5e/databases/%28default%29/documents/temperature/" + str(int(date.timestamp()))
        payload = json.dumps(data)
        response = requests.request("PATCH", url, data=payload)

    def new_humidity(self, date, value):

        date_string = str(date.date())
        time_string = str(date.time()).split('.')[0]

        data = {
            'fields': {
                'date': {
                    'stringValue': '{} {}'.format(date_string, time_string)
                },
                'value': {
                    'stringValue': str(value)
                }
            }
        }

        url = "https://firestore.googleapis.com/v1beta1/projects/example-dba5e/databases/%28default%29/documents/humidity/" + str(int(date.timestamp()))
        payload = json.dumps(data)
        response = requests.request("PATCH", url, data=payload)

        # self.plot(data_float)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
