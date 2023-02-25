# udpserver.py
# Server part of the udp workflow
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main
import socket
from config import CONFIG
import logging


class UdpServer:

    def __init__(self):
        logging.basicConfig(level=CONFIG.LOGGING_LEVEL, format=CONFIG.LOGGING_FORMAT)

    def socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(CONFIG.SOCKETTIMEOUT)
        msg = f"socket(): Server socket open {str(socket.gethostname())} / {str(sock)}"
        logging.debug(msg)
        return sock

