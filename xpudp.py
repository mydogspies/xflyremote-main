# xpudp.py
# All the UDP functionality for the communication between Xplane and Xflyremote
# A lot of the code is based directly on the fantastic XplaneUdp repo from charlylima (see notes below).
# License: GPLv3
# * UDP part of the code based in big part on the library from charlylima. Eternally grateful to the author.
# * https://github.com/charlylima/XPlaneUDP/blob/master/XPlaneUdp.py
#
import socket
import struct
import platform
import custom_exceptions as exception
from config import CONFIG
import logging
from time import sleep
import binascii


class XpUdp:
    # network variables
    MULTCASTIP = "239.255.1.1"
    XPLANEIP = CONFIG.XPLANEIP
    DATAPORT = CONFIG.DATAPORT
    BEACONPORT = CONFIG.BEACONPORT
    SOCKETTIMEOUT = CONFIG.SOCKETTIMEOUT

    def __init__(self):
        logging.basicConfig(level=CONFIG.LOGGING_LEVEL, format=CONFIG.LOGGING_FORMAT)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(3.0)

        self.datarefs = {}  # {idx,dataref}
        self.datarefidx = 0
        self.beacondata = {}
        self.xplanevalues = {}
        self.defaultfreq = 1

    def __del__(self):
        for i in range(len(self.datarefs)):
            self.subscribedataref(next(iter(self.datarefs.values())), freq=0)
        self.socket.close()

    def defsocket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock

    def sendcommand(self, dataref):
        # Sends a Command-type dataref to Xplane

        addr = (self.XPLANEIP, self.DATAPORT)
        data = struct.pack('=5s500s', b'CMND', dataref.encode('utf-8'))
        self.socket.sendto(data, addr)

    def senddataref(self, dataref, value, vtype="float"):
        # Sends a dataref to Xplane

        cmd = b"DREF\x00"
        dataref = dataref + "\x00"
        string = dataref.ljust(500).encode()
        data = "".encode()

        if vtype == "float":
            data = struct.pack("<5sf500s", cmd, value, string)
        elif vtype == "int":
            data = struct.pack("<5sif500s", cmd, value, string)
        elif vtype == "bool":
            data = struct.pack("<5sIf500s", cmd, value, string)

        assert (len(data) == 509)

        self.socket.sendto(data, (self.beacondata["IP"], self.DATAPORT))
        logging.debug("senddataref(): " + str(data))

    def subscribedataref(self, dataref, freq=None):
        # subscribes to datarefs

        idx = -9999

        if freq is None:
            freq = self.defaultfreq

        if dataref in self.datarefs.values():
            idx = list(self.datarefs.keys())[list(self.datarefs.values()).index(dataref)]

            if freq == 0:
                if dataref in self.xplanevalues.keys():
                    del self.xplanevalues[dataref]
                del self.datarefs[idx]

        else:
            idx = self.datarefidx
            self.datarefs[self.datarefidx] = dataref
            self.datarefidx += 1

        cmd = b"RREF\x00"
        string = dataref.encode()
        data = struct.pack("<5sii400s", cmd, freq, idx, string)

        assert (len(data) == 413)

        self.socket.sendto(data, (self.beacondata["IP"], self.beacondata["Port"]))
        logging.debug("subscribedataref(): Added: " + str(data))

        if self.datarefidx % 100 == 0:
            sleep(0.2)

    def getvalues(self):
        # get values from subscribed datarefs

        try:
            data, addr = self.socket.recvfrom(1472)
            retvalues = {}
            header = data[0:5]

            if header != b"RREF,":
                print("Unknown packet: ", binascii.hexlify(data))
            else:
                values = data[5:]
                lenvalue = 8
                numvalues = int(len(values) / lenvalue)

                for i in range(0, numvalues):
                    singledata = data[(5 + lenvalue * i):(5 + lenvalue * (i + 1))]
                    (idx, value) = struct.unpack("<if", singledata)

                    if idx in self.datarefs.keys():

                        if 0.0 > value > -0.001:
                            value = 0.0
                        retvalues[self.datarefs[idx]] = value

            self.xplanevalues.update(retvalues)

        except Exception as error:
            logging.error("getvalues(): Xplane timed out.")
            logging.error(error)

        logging.debug("getvalues(): " + str(self.xplanevalues))
        return self.xplanevalues

    def findip(self):

        # findip(self)
        # Lookup function to find the Xplane beacon on the network
        # original code by charlylima (see notes on top)

        self.beacondata = {}
        sock = self.defsocket()

        if platform.system() == "Windows":
            sock.bind(('', self.BEACONPORT))
        else:
            sock.bind((self.MULTCASTIP, self.BEACONPORT))

        mreq = struct.pack("=4sl", socket.inet_aton(self.MULTCASTIP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock.settimeout(self.SOCKETTIMEOUT)

        try:
            packet, sender = sock.recvfrom(1472)
            msg_beacon_id = "findip(): Xplane beacon: " + packet.hex()
            logging.debug(msg_beacon_id)

            # decode data
            header = packet[0:5]
            if header != b"BECN\x00":
                msg_unknown_packet = "findip(): Unknown packet from " + sender(0)
                logging.error(msg_unknown_packet)

            else:
                data = packet[5:21]
                (
                    beacon_major_version,  # 1 at the time of X-Plane 10.40
                    beacon_minor_version,  # 1 at the time of X-Plane 10.40
                    application_host_id,  # 1 for X-Plane, 2 for PlaneMaker
                    xplane_version_number,  # 104014 for X-Plane 10.40b14
                    role,  # 1 for master, 2 for extern visual, 3 for IOS
                    port,  # port number X-Plane is listening on
                ) = struct.unpack("<BBiiIH", data)

                hostname = packet[21:-1]
                hostname = hostname[0:hostname.find(0)]
                if beacon_major_version == 1 \
                        and beacon_minor_version <= 2 \
                        and application_host_id == 1:
                    self.beacondata["IP"] = sender[0]
                    self.beacondata["Port"] = port
                    self.beacondata["hostname"] = hostname.decode()
                    self.beacondata["XPlaneVersion"] = xplane_version_number
                    self.beacondata["role"] = role

                    msg_beacon_version = "Beacon version: {}.{}.{}".format(beacon_major_version, beacon_minor_version,
                                                                           application_host_id)
                    logging.debug(msg_beacon_version)
                else:
                    msg_no_support = "Version {}.{}.{} beacon not supported.".format(beacon_major_version,
                                                                                     beacon_minor_version,
                                                                                     application_host_id)
                    logging.error(msg_no_support)
                    raise exception.VersionNotSupportedError()

        except socket.timeout:
            logging.error("findip(): Xplane client not found (socket timeout).")
            raise exception.XpNotFoundError()

        finally:
            sock.close()
