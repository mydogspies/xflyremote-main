# xflyremote.py v1.0
# Main class for Xflyremote
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main
import sys
import time

from udpserver import UdpServer as serv
from udpclient import UdpClient as client
from xpflyio import XpFlyIO as xpio
import logging
from config import CONFIG
import custom_exceptions as exception
from displayio import DisplayIO
import threading
import datarepo

thread_stop = threading.Event()


def my_excepthook(type, value, traceback):
    thread_stop.set()
    sys.__excepthook__(type, value, traceback)


sys.excepthook = my_excepthook


class Xflyremote:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format=CONFIG.LOGGING_FORMAT)
        self.stopexec = False
        self.db = datarepo.Datarepo()
        self.wait = True
        self.disp_cmd = ""
        self.startup = True  # flag for setting things up on first run

    def receivefromxplane(self):

        while not thread_stop.is_set():
            try:
                diff = xp.receivesubscribedvalues(server_socket)

                # parse difference and update hardware
                if len(diff) != 0:
                    try:
                        if diff['values_changed']:
                            data = "1"
                            displayio.sendserialdata(ser, data)
                    except:
                        msg = f"receivefromxplane(): First iteration over difference list (not error)."
                        logging.debug(msg)

            except exception.NetworkTimeoutError:
                logging.error("main loop: Xplane timed out.")
                break

    def receivefromdisplay(self):
        self.disp_cmd = ""

        # MAIN WAITING THREAD
        while not thread_stop.is_set():
            if ser.in_waiting > 0:
                self.disp_cmd = displayio.getserialdata(ser)
                logging.debug(f"receivefromdisplay(): {self.disp_cmd} received.")

                #  initial data sent to Arduino on first run
                if self.startup:
                    time.sleep(4)
                    sendradiovals = "*9c0000RVAL"
                    displayio.sendserialdata(ser, sendradiovals)
                    logging.debug(f"receivefromdisplay(): Startup process finished.")
                    self.startup = False

                # reply to display when it queries for page set
                if self.disp_cmd == "s?":
                    set = "s0"
                    time.sleep(1)
                    displayio.sendserialdata(ser, set)

                # get button commands and send on to xplane
                if self.disp_cmd[0] == "b":
                    bcmd = self.disp_cmd[0:6]
                    result = self.db.getbyitem("onstate", bcmd)
                    for dataref in result:
                        if dataref['type'] == "cmd":
                            xp.sendcommand(dataref['dataref'], client_socket)
                        # elif dataref['type'] == "dref":
                        #     xp.senddataref(dataref['dataref'], dataref['unittype'], self.disp_cmd[5], server_socket, beacon)

                #  receive radio frequencies array from Arduino
                if self.disp_cmd[0:2] == "rf":
                    freq_values = self.disp_cmd[3:].split()
                    print(freq_values)
                    # xp.senddataref("sim/cockpit/radios/com1_freq_hz", "float", float(freq_values[0])*100, server_socket, beacon)
                    xp.senddataref("sim/cockpit/radios/com2_freq_hz", "float", float(freq_values[1]) * 100,
                                   server_socket, beacon)
                    # xp.senddataref("sim/cockpit/radios/nav1_freq_hz", "float", float(freq_values[2])*100, server_socket, beacon)
                    # xp.senddataref("sim/cockpit/radios/nav2_freq_hz", "float", float(freq_values[3])*100, server_socket, beacon)

    def subdatarefsindb(self):
        drefs = self.db.getbyitem("type", "dref")
        for ref in drefs:
            if ref['sub'] == 1:
                xp.subscribedataref(ref['dataref'], 1, server_socket, beacon)
                msg = f"subdatarefsindb(): Subscribed to {ref}."
                logging.debug(msg)


if __name__ == '__main__':
    xp = xpio()
    displayio = DisplayIO()
    xfly = Xflyremote()

    # initiate new sockets and find xplane
    server_socket = serv().socket()
    client_socket = client().socket()
    beacon_socket = serv().socket()
    beacon = xpio().findbeacon(beacon_socket)

    # initiate connection with display hardware
    ser = displayio.connect()

    # subscribe to all drefs in databse
    xfly.subdatarefsindb()

    # start the loops for sending and receiving data
    trecvxp = threading.Thread(target=xfly.receivefromxplane)
    trecvdisp = threading.Thread(target=xfly.receivefromdisplay)
    trecvxp.start()
    trecvdisp.start()
