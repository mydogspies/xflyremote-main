# XpUdo
# Main class for Xflyremote
# This class does all the
# * For the UDP code I have used big parts of charlylima's code from his Github repo. See notes below.
# License: GPLv3
# UDP part of the code based in big part on the library from charlylima. Eternally grateful to the author.
# https://github.com/charlylima/XPlaneUDP/blob/master/XPlaneUdp.py

import xpudp
import custom_exceptions as exception


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
