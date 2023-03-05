# xflyremote.py
# Main class for Xflyremote
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main
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


class Xflyremote:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format=CONFIG.LOGGING_FORMAT)
        self.stopexec = False
        self.db = datarepo.Datarepo()
        self.wait = True
        self.disp_cmd = ""
        self.page_button_state = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def receivefromxplane(self):
        while True:
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
        while True:
            if ser.in_waiting > 0:
                self.disp_cmd = displayio.getserialdata(ser)
                logging.debug(f"receivefromdisplay(): {self.disp_cmd} received.")

            # reply to display when it queries for page set
                if self.disp_cmd == "s?":
                    set = "s0"
                    time.sleep(1)
                    displayio.sendserialdata(ser, set)

                # set the page button state array
                if self.disp_cmd[0] == "b":
                    result = self.db.getbyitem("onstate", self.disp_cmd)
                    for dataref in result:
                        xp.sendcommand(dataref['dataref'], client_socket)

    def subdatarefsindb(self):
        drefs = self.db.getbyitem("type", "dref")
        for ref in drefs:
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

    # * Just for testing
    # xp.sendcommand("sim/lights/nav_lights_on", client_socket)

    # send some datarefs
    # baro = 30.00
    # heading = 360
    # xp.senddataref("sim/cockpit/autopilot/heading_mag", "float", heading, client_socket, beacon)
    # xp.senddataref("sim/cockpit/misc/barometer_setting", "float", baro, client_socket, beacon)

    # subscribe to some datarefs
    # xp.subscribedataref("sim/cockpit/autopilot/heading_mag", 1, server_socket, beacon)
    # xp.subscribedataref("sim/cockpit/misc/barometer_setting", 1, server_socket, beacon)
    # xp.subscribedataref("sim/cockpit/electrical/nav_lights_on", 1, server_socket, beacon)

    # start the loops for sending and receiving data
    trecvxp = threading.Thread(target=xfly.receivefromxplane)
    trecvdisp = threading.Thread(target=xfly.receivefromdisplay)
    trecvxp.start()
    trecvdisp.start()
