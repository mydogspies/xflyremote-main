import socket
import struct
import platform
import custom_exceptions as exception


class XpUdp:
    # network variables
    NETIP = "239.255.1.1"
    XPLANEIP = "192.168.178.40"
    DATAPORT = 49000
    BEACONPORT = 49707
    SOCKETTIMEOUT = 3.0

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(3.0)

        self.datarefs = {}  # {idx,dataref}
        self.datarefidx = 0
        self.beacondata = {}
        self.xplanevalues = {}
        self.defaultfreq = 1

    def __del__(self):
        # - Add dataref reset
        self.socket.close()

    def defsocket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock

    def sendcommand(self, dataref):

        # sendcommand(self, dataref)
        # Sends a Command-type dataref to Xplane

        addr = (self.XPLANEIP, self.DATAPORT)
        data = struct.pack('=5s500s', b'CMND', dataref.encode('utf-8'))
        # print("Dataref command sent: ", data)
        self.defsocket().sendto(data, addr)

    def findip(self):

        # findip(self)
        # Lookup function to find the Xplane beacon on the network
        # original code by charlylima (see notes on top)

        self.beacondata = {}
        sock = self.defsocket()

        if platform.system() == "Windows":
            sock.bind(('', self.BEACONPORT))
        else:
            sock.bind((self.NETIP, self.BEACONPORT))

        mreq = struct.pack("=4sl", socket.inet_aton(self.NETIP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock.settimeout(self.SOCKETTIMEOUT)

        try:
            packet, sender = sock.recvfrom(1472)
            print("Xplane beacon: ", packet.hex())

            # decode data
            header = packet[0:5]
            if header != b"BECN\x00":
                print("Header error: Unknown packet from " + sender[0])

            else:
                data = packet[5:21]
                beacon_major_version = 0
                beacon_minor_version = 0
                application_host_id = 0
                xplane_version_number = 0
                role = 0
                port = 0
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
                    print("Beacon version: {}.{}.{}".format(beacon_major_version, beacon_minor_version,
                                                            application_host_id))
                else:
                    print("Version {}.{}.{} beacon not supported.".format(beacon_major_version,
                                                                          beacon_minor_version,
                                                                          application_host_id))
                    raise exception.VersionNotSupportedError()

        except socket.timeout:
            raise exception.XpNotFoundError()
        finally:
            sock.close()