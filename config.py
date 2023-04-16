# config.py
# Some global variables for logging etc
import logging


class CONFIG:
    # logger settings
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    # network xplane settings
    MCASTIP = "239.255.1.1"
    XPLANEIP = "192.168.178.40"
    DATAPORT = 49000
    BEACONPORT = 49707
    SOCKETTIMEOUT = 2.0
    # databse settings
    DBJSON = "xflydb.json"  # name of the json db file
    # test settings
    TESTFOLDERPATH = "/test"
    # hardware display settings
    SERIALPORT = "COM7"
    SERIALTIMEOUT = 0.01
    SERIALRATE = 115200
