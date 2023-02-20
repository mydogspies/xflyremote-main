# testdatarepo.py
# Unittest for the Datarepo class in datarepo.py
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main
import unittest
import datarepo


class TestDatarepo(unittest.TestCase):

    repo = datarepo.Datarepo()

    def testgetbydataref(self):
        self.assertEqual(self.repo.getbydataref("sim/test/test"), [{'dataref': 'sim/test/test', 'type': 'cmd', 'units': 'testunits', 'info': 'This is a test and can not be used in sim', 'id': 136336198132705534}], "Failed getbydataref()")

    def testgetbyidx(self):
        self.assertEqual(self.repo.getbyidx(136336198132705534), [{'dataref': 'sim/test/test', 'type': 'cmd', 'units': 'testunits', 'info': 'This is a test and can not be used in sim', 'id': 136336198132705534}], "Failed getbyidx()")

    def testadd(self):
        testref = {"dataref": "sim/test/test",
                   "type": "cmd",
                   "units": "testunits",
                   "info": "This is a test and can not be used in sim"}
        self.assertEqual(self.repo.add(testref), False, "Failed add()")