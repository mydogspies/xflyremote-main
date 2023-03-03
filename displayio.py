import serial
from config import CONFIG
import logging
import time


class DisplayIO:

    def connect(self):
        try:
            ser = serial.Serial(CONFIG.SERIALPORT, 115200, timeout=1)
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

    def sendserialdata(self, serial_connection, data):
        send = serial_connection.write(bytes(data, 'utf-8'))
        time.sleep(0.1)
        msg = f"sendserialdata(): Data sent: {send}"
        logging.debug(msg)
        return send
