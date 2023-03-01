# xflyremote.py
# Main class for Xflyremote
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main
from udpserver import UdpServer as serv
from udpclient import UdpClient as client
from xpflyio import XpFlyIO as xpio
import logging
from config import CONFIG
import custom_exceptions as exception
from displayio import DisplayIO


class Xflyremote:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format=CONFIG.LOGGING_FORMAT)


if __name__ == '__main__':
    xp = xpio()
    displayio = DisplayIO()

    # initiate new sockets and find xplane
    server_socket = serv().socket()
    client_socket = client().socket()
    beacon_socket = serv().socket()
    beacon = xpio().findbeacon(beacon_socket)

    # initiate connection with display hardware
    ser = displayio.connect()

    # send a command to xplane
    # * Just for testing
    # xp.sendcommand("sim/lights/nav_lights_on", client_socket)

    # send some datarefs
    baro = 30.00
    heading = 360
    xp.senddataref("sim/cockpit/autopilot/heading_mag", "float", heading, client_socket, beacon)
    xp.senddataref("sim/cockpit/misc/barometer_setting", "float", baro, client_socket, beacon)

    # subscribe to some datarefs
    xp.subscribedataref("sim/cockpit/autopilot/heading_mag", 1, server_socket, beacon)
    xp.subscribedataref("sim/cockpit/misc/barometer_setting", 1, server_socket, beacon)

    # check for incoming values
    while True:
        try:
            values = xp.receivesubscribedvalues(server_socket)

        except exception.NetworkTimeoutError:
            logging.error("main loop: Xplane timed out.")
            exit(0)

        # test arduino/nextion display interactivity
        if ser.in_waiting > 0:
            disp_cmd = displayio.getserialdata(ser)
            print(f"DISPLAY CMD: {disp_cmd}")
            if disp_cmd == "btn2_1":
                xp.sendcommand("sim/lights/nav_lights_on", client_socket)
            elif disp_cmd == "btn2_0":
                xp.sendcommand("sim/lights/nav_lights_off", client_socket)


