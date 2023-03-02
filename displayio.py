import serial
from config import CONFIG
import logging


class DisplayIO:

    def connect(self):
        try:
            ser = serial.Serial(CONFIG.SERIALPORT, 9600, timeout=1)
            ser.flush()
            msg = f"connect(): Connected to {ser}"
            logging.debug(msg)
            return ser
        except Exception as error:
            msg = f"connect(): Could not connect to serial port {CONFIG.SERIALPORT}"
            logging.error(msg)
            logging.debug(error)
            return 0

    def getserialdata(self, serial_connection):
        try:
            data = serial_connection.readline().decode('utf-8').rstrip()
            msg = f"getserialdata(): String received: {data}"
            logging.debug(msg)
            return data
        except Exception as error:
            msg = f"connect(): Error receiving serial data!"
            logging.error(msg)
            logging.debug(error)
            return 0
