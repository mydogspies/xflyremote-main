# xflyremote.py
# Main class for Xflyremote
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main

import xpudp
import custom_exceptions as exception


class Xflyremote:
    def getcommands(self):
        # read all the commands from database
        pass

    def getdatarefs(self):
        # read all the datarefs from database
        pass


if __name__ == '__main__':

    xp = xpudp.XpUdp()

    try:
        beacon = xp.findip()
        print(beacon)
        xp.sendcommand("sim/lights/nav_lights_on")

    except exception.VersionNotSupportedError:
        print("Error: This Xplane version is not supported.")
        exit(0)

    except exception.XpNotFoundError:
        print("Error: Xplane not found!")
        exit(0)
