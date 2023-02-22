# custom_exception.py
# Various custom exception classes
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main

class XpNotFoundError(Exception):
    args = "Could not find any running XPlane instance in the network."


class NetworkTimeoutError(Exception):
    args = "XPlane timeout."


class VersionNotSupportedError(Exception):
    args = "XPlane version not supported."


class DatabaseError(Exception):
    args = "Database error."


class CustomIOError(Exception):
    args = "Read/write error."
