# xpflyio.py
# The command interface for sending and receiving datarefs between app  and Xplane
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main
# * UDP part of the code based in part on the library from charlylima. Eternally grateful to the author.
# * https://github.com/charlylima/XPlaneUDP/blob/master/XPlaneUdp.py
import platform
import struct
from udpserver import socket
from config import CONFIG
import logging
from time import sleep


class XpFlyIO:

    def __init__(self):
        logging.basicConfig(level=CONFIG.LOGGING_LEVEL, format=CONFIG.LOGGING_FORMAT)
        self.beacon = {}
        self.datarefs = {}
        self.xpvals = {}
        self.refindex = 0

    def sendcommand(self, dataref, server_socket: socket):
        address = (CONFIG.XPLANEIP, CONFIG.DATAPORT)
        data_string = struct.pack('=5s500s', b'CMND', dataref.encode('utf-8'))
        server_socket.sendto(data_string, address)
        return 1

    def findbeacon(self, server_socket: socket):

        if platform.system() == "Windows":
            server_socket.bind(('', CONFIG.BEACONPORT))
        else:
            server_socket.bind((CONFIG.MCASTIP, CONFIG.BEACONPORT))

        request = struct.pack("=4sl", socket.inet_aton(CONFIG.MCASTIP), socket.INADDR_ANY)
        server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, request)
        server_socket.settimeout(CONFIG.SOCKETTIMEOUT)

        try:
            packet, sender = server_socket.recvfrom(1472)
            msg_beacon = f"findbeacon(): Xplane beacon found: {str(packet.hex())}"
            logging.debug(msg_beacon)

            header = packet[0:5]
            if header != b"BECN\x00":
                msg_unknown_packet = f"findip(): Unknown packet from {sender(0)}"
                logging.error(msg_unknown_packet)
            else:
                data = packet[5:21]
                (
                    major_version,
                    minor_version,
                    host_id,
                    xplane_version,
                    role,
                    port,
                ) = struct.unpack("<BBiiIH", data)

                hostname = packet[21:-1]
                hostname = hostname[0:hostname.find(0)]
                if major_version == 1 and minor_version <= 2 and host_id == 1:
                    self.beacon["ip"] = sender[0]
                    self.beacon["port"] = port
                    self.beacon["hostname"] = hostname.decode()
                    self.beacon["version"] = xplane_version
                    self.beacon["role"] = role

                    address = f"{self.beacon['ip']}:{self.beacon['port']}"
                    msg_beacon_found = f"findbeacon(): Beacon found on {address} with Xplane version {self.beacon['version']}"
                    logging.debug(msg_beacon_found)
                    logging.info("Xflyremote connected to Xplane")
                    return self.beacon
                else:
                    msg_nobeacon = "findip(): Could not connect. This version of the Xplane beacon is not supported."
                    logging.error(msg_nobeacon)
                    return 0

        except Exception as error:
            msg_timeout = "findbeacon(): Socket timed out (xplane not found)."
            logging.error(msg_timeout)
            logging.error(error)

        finally:
            server_socket.close()

    def senddataref(self, dataref, datatype, value, server_socket: socket, beacon):
        dataref += "\x00"
        datastring = dataref.ljust(500).encode()
        data = b"''"
        command = b"DREF\x00"

        if datatype == "float":
            data = struct.pack("<5sf500s", command, value, datastring)
        elif datatype == "int":
            data = struct.pack("<5sif500s", command, value, datastring)
        elif datatype == "bool":
            data = struct.pack("<5sIf500s", command, value, datastring)

        server_socket.sendto(data, (beacon["ip"], CONFIG.DATAPORT))
        msg = f"senddataref(): Sent {str(data)} to Xplane with value {value}."
        logging.debug(msg)

    def subscribedataref(self, dataref, frequency, server_socket : socket, beacon):

        if dataref in self.datarefs.values():
            index = list(self.datarefs.keys())[list(self.datarefs.values()).index(dataref)]

            if frequency == 0:
                if dataref in self.xpvals.keys():
                    del self.xpvals[dataref]
                del self.datarefs[index]
        else:
            index = self.refindex
            self.datarefs[self.refindex] = dataref
            self.refindex += 1

        datastring = dataref.encode()
        command = b"RREF\x00"
        data = struct.pack("<5sii400s", command, frequency, index, datastring)
        server_socket.sendto(data, (beacon["ip"], beacon["port"]))
        msg = f"subscribedataref(): Subscribed {str(data)}."
        logging.debug(msg)
        if self.refindex % 100 == 0:
            sleep(0.2)

    def receivesubscribedvalues(self, client_socket : socket):

        try:
            data, address = client_socket.recvfrom(1472)
            returnvalues = {}

            header = data[0:5]
            if header != b"RREF,":
                msg_unknown = f"receivesubscribedvalues(): Uknown header {str(header)}"
                logging.warning(msg_unknown)
            else:
                values = data[5:]
                length = 8
                itemcount = int(len(values) / length)

                for i in range(0, itemcount):
                    datarow = data[(5 + length * i):(5 + length * (i + 1))]
                    (index, value) = struct.unpack("<if", datarow)

                    if index in self.datarefs.keys():

                        if 0.0 > value > -0.001:
                            value = 0.0
                        returnvalues[self.datarefs[index]] = value

            self.xpvals.update(returnvalues)

        except Exception as error:
            logging.error("receivesubscribedvalues(): Xplane timed out.")
            logging.error(error)

        msg_received = f"receivesubscribedvalues(): Received {str(self.xpvals)}"
        logging.debug(msg_received)
        return self.xpvals

