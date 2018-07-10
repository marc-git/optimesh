# -*- coding: utf-8 -*-
#
from __future__ import print_function

from .__about__ import (
    __version__,
    __author__,
    __author_email__,
    __website__,
    __status__,
    __license__,
)

from . import chen_holst
from . import cli
from . import laplace
from .lloyd import lloyd
from .odt import odt
from . import schloemer

__all__ = [
    "__version__",
    "__author__",
    "__author_email__",
    "__website__",
    "__status__",
    "__license__",
    "chen_holst",
    "cli",
    "laplace",
    "lloyd",
    "odt",
    "schloemer",
]

# try:
#     import pipdate
# except ImportError:
#     pass
# else:
#     if pipdate.needs_checking(__name__):
#         print(pipdate.check(__name__, __version__), end='')
