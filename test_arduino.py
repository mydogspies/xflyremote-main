import serial
import logging
import time
from config import CONFIG


class TestIO:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format=CONFIG.LOGGING_FORMAT)
        self.page_button_state = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def connect(self):
        try:
            seru = serial.Serial("COM4", 115200, timeout=1)
            seru.flush()
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
        if con.in_waiting > 0:
            disp_cmd = testio.getserialdata(con)

            # if disp_cmd[0] == "m":
            #     page = "p1"
            #     time.sleep(1)
            #     testio.sendserialdata(con, page)

            # reply to display when it queries for page set
            if disp_cmd == "s?":
                set = "s0"
                time.sleep(1)
                testio.sendserialdata(con, set)

            # set the page button state array
            if disp_cmd[0] == "b":
                page = int(disp_cmd[1:3])
                button = int(disp_cmd[3:5])
                status = testio.page_button_state[page][button]

                if status:
                    testio.page_button_state[page][button] = 0
                else:
                    testio.page_button_state[page][button] = 1
