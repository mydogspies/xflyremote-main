# custom_exception.py
# Various custom exception classes
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main

class XpNotFoundError(Exception):
    args = "Error: Could not find any running XPlane instance in the network."


class NetworkTimeoutError(Exception):
    args = "Error: XPlane timeout."


class VersionNotSupportedError(Exception):
    args = "Error: XPlane version not supported."


class DatabaseError(Exception):
    args = "Error: Database error."

