# xflyremote.py
# Main class for Xflyremote
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main

import xpudp
import custom_exceptions as exception
import logging
from config import CONFIG


class Xflyremote:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format=CONFIG.LOGGING_FORMAT)


if __name__ == '__main__':

    xp = xpudp.XpUdp()

    # connect to Xplane
    try:
        beacon = xp.findip()
        xp.sendcommand("sim/lights/nav_lights_on")
    except exception.VersionNotSupportedError:
        exit(0)
    except exception.XpNotFoundError:
        exit(0)

    # subscribe to datarefs
    xp.subscribedataref("sim/cockpit/autopilot/heading_mag")
    xp.subscribedataref("sim/cockpit/misc/barometer_setting")

    # change a dataref value
    baro = 30.00
    heading = 360
    xp.senddataref("sim/cockpit/misc/barometer_setting", baro, "float")
    xp.senddataref("sim/cockpit/autopilot/heading_mag", heading, "float")

    # check for incoming values
    while True:
        try:
            values = xp.getvalues()

        except exception.NetworkTimeoutError:
            print("XPlane Timeout")
            exit(0)
