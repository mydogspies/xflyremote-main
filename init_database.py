# init_database.py
# Initiates the database from scratch with new data
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main
from datarepo import Datarepo as repo
import logging
from config import CONFIG


class InitDatabase:

    def __init__(self):
        self.dataref = {}
        logging.basicConfig(level=logging.DEBUG, format=CONFIG.LOGGING_FORMAT)

    def runinit(self):
        # Initiates a database from scratch with pre-defined datarefs
        rp = repo()

        dataref = {"dataref": "sim/lights/nav_lights_on",
                   "type": "cmd",
                   "units": "",
                   "info": "Nav lights on"}
        # for testing only
        testref = {"dataref": "sim/test/test",
                   "type": "cmd",
                   "units": "testunits",
                   "info": "This is a test and can not be used in sim"}

        if rp.add(dataref):
            logging.debug("runinit(): Added new dataref to db: " + dataref["dataref"] + "\n")
        else:
            logging.warning("runinit(): Adding dataref to db failed!")
        # for testing only
        if rp.add(testref):
            logging.debug("runinit(): Added new dataref to db: " + dataref["dataref"] + "\n")
        else:
            logging.warning("runinit(): Adding dataref to db failed!")


if __name__ == '__main__':
    init = InitDatabase()
    init.runinit()
