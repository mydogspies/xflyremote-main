# datarepo.py
# Database interface for datarefs and commands
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main
#
# * Using PysonDB from Fredy Somy
# * https://github.com/pysonDB/pysonDB
from pysondb import db
import custom_exceptions as exception
import logging
from config import CONFIG


class Datarepo:
    # format for data us {dataref:string,type:string,units:string,info_string} (id is added automagically)

    database = db.getDb("xflydb")

    def __init__(self):
        logging.basicConfig(level=CONFIG.LOGGING_LEVEL, format=CONFIG.LOGGING_FORMAT)
        self.data = {}
        self.data_idx = int
        self.datalist = {}
        self.data_string = ""

    def getall(self):
        pass

    def getbyidx(self, data_idx):
        pass

    def getbydataref(self, data_string):
        query = []
        try:
            query = self.database.getBy({"dataref": data_string})
            return query
        except exception.DatabaseError:
            logging.warning("getbydataref(): Error when trying to run database query")
        finally:
            logging.debug(query)
        pass

    def add(self, data):
        if not self.getbydataref(data["dataref"]):
            try:
                self.database.add(data)
            except exception.DatabaseError:
                logging.warning("add(): Error when trying to add data to the database")
            finally:
                logging.debug("add(): Added new dataref to database: ", data)
                return 1
        else:
            logging.warning("add(): Can not add dataref that already exists in database.")
            return 0

    def addall(self, data_array):
        pass

    def update(self, data, data_idx):
        pass
