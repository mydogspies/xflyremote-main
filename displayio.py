import serial
from config import CONFIG
import logging


class DisplayIO:

    def connect(self):
        ser = serial.Serial(CONFIG.SERIALPORT, 9600, timeout=1)
        ser.flush()
        msg = f"connect(): Connected to {ser}"
        logging.debug(msg)
        return ser

    def getserialdata(self, serial_connection):
        data = serial_connection.readline().decode('utf-8').rstrip()
        msg = f"getserialdata(): String received: {data}"
        logging.debug(msg)
        return data
