# datarepo.py
# Database interface for datarefs and commands
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main
#
# * Using PysonDB from Fredy Somy
# * https://github.com/pysonDB/pysonDB
import os

from pysondb import db
import custom_exceptions as exception
import logging
from config import CONFIG
from pathlib import Path


class Datarepo:
    # format for data us {dataref:string,type:string,units:string,info_string} (id is added automagically)

    def __init__(self):
        logging.basicConfig(level=CONFIG.LOGGING_LEVEL, format=CONFIG.LOGGING_FORMAT)

    def initdb(self):
        if Path(CONFIG.DBJSON):
            self.deletedb()

        try:
            db.getDb(CONFIG.DBJSON)
            msg = "initdb(): New database file was created with the name " + CONFIG.DBJSON
            logging.info(msg)
            return 1
        except Exception as error:
            logging.warning("initdb(): New database file could not be created")
            logging.warning(error)
            return 0

    def getall(self):
        pass

    def getbyidx(self, data_idx):
        try:
            database = db.getDb(CONFIG.DBJSON)
            query = database.getByQuery({"id": data_idx})
            return query
        except Exception as error:
            logging.warning("getbyidx(): Error when trying to run database query")
            logging.warning(error)

    def getbydataref(self, data_string):
        try:
            database = db.getDb(CONFIG.DBJSON)
            query = database.getByQuery({"dataref": data_string})
            return query
        except Exception as error:
            logging.warning("getbydataref(): Error when trying to run database query")
            logging.warning(error)
            return 0

    def add(self, data):

        if data:
            if self.getbydataref(data["dataref"]):
                logging.warning("add(): Can not add dataref that already exists in database.")
                return 0

        try:
            db.getDb(CONFIG.DBJSON).add(data)
            logging.debug("add(): Added new dataref to database: ", data)
            return 1
        except Exception as error:
            logging.error("add(): Error when trying to add data to the database")
            logging.error(error)
            return 0

    def update(self, data, data_idx):
        pass

    def deletedb(self):
        try:
            os.remove(CONFIG.DBJSON)
            logging.debug("deletedb(): Current db has been deleted")
            return 1
        except Exception as error:
            logging.error("deletedb(): Could not remove json file.")
            logging.error(error)
            return 0
