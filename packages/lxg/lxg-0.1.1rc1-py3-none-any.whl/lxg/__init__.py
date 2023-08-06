from .version import get_version

VERSION = (0, 1, 1, 'rc', 1)

__version__ = get_version(VERSION)

from .loggable import *
