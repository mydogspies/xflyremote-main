# testdatarepo.py
# Unittest for the Datarepo class in datarepo.py
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main
import unittest
import datarepo
import shutil
import os
from config import CONFIG


class TestDatarepo(unittest.TestCase):

    def setUp(self):
        self.repo = datarepo.Datarepo()
        # copy new datafile to the test folder for inittest
        workpath = os.getcwd() + "\\"
        src = workpath + "..\\" + CONFIG.DBJSON
        dest = workpath + CONFIG.DBJSON
        shutil.copy(src, dest)
        data = self.repo.getbydataref("sim/test/test")
        self.testid = data[0]["id"]
        print(self.id)
        self.testdata = [{
            "dataref": "sim/test/test",
            "type": "cmd",
            "units": "testunits",
            "onstate": 253,
            "offstate": 254,
            "info": "This is test data and does not correspond to any dataref in Xplane",
            "id": self.testid
        }]

    def testgetbydataref(self):

        self.assertEqual(self.repo.getbydataref("sim/test/test"), self.testdata, "Failed getbydataref()")

    def testgetbyidx(self):
        self.assertEqual(self.repo.getbyidx(self.testid), self.testdata, "Failed getbyidx()")

    def testadd(self):
        testref = {"dataref": "sim/test/test",
                   "type": "cmd",
                   "units": "testunits",
                   "onstate": 253,
                   "offstate": 254,
                   "info": "This is test data and does not correspond to any dataref in Xplane"}
        self.assertEqual(self.repo.add(testref), False, "Failed add()")
