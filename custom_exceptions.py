class XpNotFoundError(Exception):
    args = "Error: Could not find any running XPlane instance in the network."


class NetworkTimeoutError(Exception):
    args = "Error: XPlane timeout."


class VersionNotSupportedError(Exception):
    args = "Error: XPlane version not supported."
