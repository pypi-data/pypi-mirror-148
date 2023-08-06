__title__ = "loto_online.py"
__author__ = "Zakovskiy"
__license__ = "MIT"
__copyright__ = "Copyright 2022-2022 Zakovskiy"
__version__ = "1.0.0"

from .lotoonline import Client
from .authorization import Authorization
from .game import Game
from .friend import Friend
from .socket_listener import SocketListener

from .utils import objects

from requests import get
from json import loads

__newest__ = loads(get("https://pypi.python.org/pypi/loto_online.py/json").text)["info"]["version"]

if __version__ != __newest__:
    exit(f"New version of {__title__} available: {__newest__} (Using {__version__})")