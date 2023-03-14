# init_database.py
# Initiates the database from scratch with new data
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main
import json
from datarepo import Datarepo as repo
import logging
from config import CONFIG


class InitDatabase:

    def __init__(self):
        self.dataref = {}
        logging.basicConfig(level=logging.DEBUG, format=CONFIG.LOGGING_FORMAT)

    def addataset(self, datajson):
        # Initiates a database from scratch with pre-defined datarefs
        rp = repo()
        rows = len(datajson["dataset"])
        count = 0

        for datarow in datajson["dataset"]:
            if rp.add(datarow):
                count += 1
                datastr = str(datarow)
                msg = f"addataset(): Added new dataref to db: {datastr}"
                logging.debug(msg)
            else:
                logging.warning("addataset(): Adding dataref to db failed!")

        logging.info(f"Added {count} datarefs out of {rows}")

    def initiatenewdatabase(self):

        # initiate a new database file and add the test data
        rp = repo()
        testref = {"dataref": "sim/test/test",
                   "type": "cmd",
                   "units": "testunits",
                   "unittype": "float",
                   "onstate": "0",
                   "info": "This is test data and does not correspond to any dataref in Xplane",
                   "sub": 0}
        rp.initdb()
        rp.add(testref)
        logging.info("initiatenewdataset(): Current db has been reset and re-initiated")


if __name__ == '__main__':
    init = InitDatabase()

    # init.initiatenewdatabase()

    # add dataset
    file = open("xpfly_dataset.json")
    dataset = json.load(file)
    init.addataset(dataset)
