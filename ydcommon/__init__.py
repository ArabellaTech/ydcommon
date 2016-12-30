"""
YD Technology common libraries
"""

VERSION = (0, 1, 63)

__version__ = '.'.join((str(each) for each in VERSION[:4]))


def get_version():
    """
    Returns shorter version (digit parts only) as string.
    """
    version = '.'.join((str(each) for each in VERSION[:3]))
    if len(VERSION) > 3:
        version += str(VERSION[3])
    return version
