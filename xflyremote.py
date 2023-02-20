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

    try:
        beacon = xp.findip()
        xp.sendcommand("sim/lights/nav_lights_on")
    except exception.VersionNotSupportedError:
        exit(0)
    except exception.XpNotFoundError:
        exit(0)
