import serial
import logging
import time
from config import CONFIG


class TestIO:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format=CONFIG.LOGGING_FORMAT)
        # self.page_button_state = [
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # ]

    def connect(self):
        try:
            seru = serial.Serial("COM4", 115200, timeout=0.01)
            msg = f"connect(): Connected to {seru}"
            logging.debug(msg)
            return seru
        except Exception as error:
            msg = f"connect(): Could not connect to serial port."
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
        send = serial_connection.write(data.encode('utf-8'))
        time.sleep(0.1)
        serial_connection.flush()
        msg = f"sendserialdata(): Data sent: {send}"
        logging.debug(msg)
        return send


if __name__ == '__main__':

    testio = TestIO()

    # initiate connection with display hardware
    con = testio.connect()

    while True:
        if con.in_waiting > 2:
            disp_cmd = testio.getserialdata(con)

            # reply to display when it queries for page set
            if disp_cmd == "s?":
                set = "set0"
                testio.sendserialdata(con, set)

