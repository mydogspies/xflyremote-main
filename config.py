# config.py
# Some global variables for logging etc
import logging


class CONFIG:
    # logger settings
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    # network settings
    XPLANEIP = "192.168.178.40"
    DATAPORT = 49000
    BEACONPORT = 49707
    SOCKETTIMEOUT = 3.0
