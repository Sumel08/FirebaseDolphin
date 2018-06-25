import sys
import glob
import serial
from struct import pack
from PyQt5 import QtCore as core
import importlib


class Manager(core.QThread):
    rx_buffer = core.pyqtSignal(bytes)
    serial_port = serial.Serial()

    def __init__(self):
        core.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def init_port(self, port_name, baudrate, bytesize=serial.EIGHTBITS):
        self.serial_port.port = port_name
        self.serial_port.baudrate = baudrate
        self.serial_port.bytesize = bytesize

    def close_port(self):
        self.serial_port.close()
        return self.serial_port.is_open

    def open_port(self):
        self.serial_port.open()
        return self.serial_port.is_open

    @core.pyqtSlot(str)
    def send_data(self, data):
        print(data)
        self.serial_port.write(data.encode())

    def run(self):
        while True:
            character = self.serial_port.readline()
            self.serial_port.flushInput()
            self.rx_buffer.emit(character)
            self.sleep(0.2)

    def serial_ports(self):
        """ Lists serial port names
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result


if __name__ == '__main__':
    serial_manager = Manager()
    # print(serial_manager.serial_ports())
    serial_manager.start()
