# custom_exception.py
# Various custom exception classes
# License: GPLv3
# https://github.com/mydogspies/xflyremote-main


class NetworkTimeoutError(Exception):
    args = "XPlane timeout."
