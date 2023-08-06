import sys
import socket
import json
import threading
from .utils import objects
from datetime import datetime
from loguru import logger
from .socket_listener import SocketListener

from .authorization import Authorization
from .game import Game
from .friend import Friend


class Client(SocketListener):

    def __init__(self, token: str = None, name: str = "", server_id: str = None, pl: str = "ios",
        debug: bool = False, tag: str = "", ip: str = None, port: int = None) -> None:
        super().__init__(self)
        self.api_url = "http://static.rstgames.com/loto/"
        self.pl = pl
        self.tag = tag
        self.uid = None
        self.receive = []
        self.info = {}
        self.logger = logger
        self.logger.remove()
        self.logger.add(sys.stderr, format="{time:HH:mm:ss.SSS}: {message}", level="DEBUG" if debug else "INFO")
        self.create_connection(server_id, ip, port)
        self.load_classes()
        #self.authorization.sign(self.authorization.get_session_key())

        if token:
            self.authorization.signin_by_access_token(token, name)

    def load_classes(self) -> None:
        self.authorization: Authorization = Authorization(self)
        self.game: Game = Game(self)
        self.friend: Friend = Friend(self)

    def get_user_info(self, user_id: int) -> objects.UserInfo:
        self.send_server(
            {
                "cmd": "get_user_info",
                "id": user_id
            }
        )
        data = self._get_data("user_info")
        if data["cmd"] != "user_info":
            raise objects.Err(data)
        return objects.UserInfo(data).UserInfo

    def get_prem_price(self) -> objects.ItemsPrice:
        self.send_server(
            {
                "cmd": "get_prem_price"
            }
        )
        return objects.ItemsPrice(self._get_data("prem_price")).ItemsPrice

    def get_points_price(self) -> objects.ItemsPrice:
        self.send_server(
            {
                "cmd": "get_points_price"
            }
        )
        return objects.ItemsPrice(self._get_data("points_price")).ItemsPrice

    def buy_prem(self, id: int = 0) -> None:
        self.send_server(
            {
                "cmd": "buy_prem",
                "id": f"ru.rstgames.loto.prem.{id}"
            }
        )

    def buy_points(self, id: int = 0) -> dict:
        self.send_server(
            {
                "cmd": "buy_points",
                "id": f"ru.rstgames.loto.points.{id}"
            }
        )

        return self.listen()

    def buy_asset(self, asset_id) -> None:
        self.send_server(
            {
                "cmd": "buy_asset",
                "id": asset_id
            }
        )

    def get_assets(self) -> objects.Assets:
        self.send_server(
            {
                "cmd": "get_assets"
            }
        )
        return objects.Assets(self._get_data("assets")).Assets

    def asset_select(self, asset_id) -> None:
        self.send_server(
            {
                "cmd": "asset_select",
                "id": asset_id
            }
        )

    def achieve_select(self, achieve_id) -> None:
        self.send_server(
            {
                "cmd": "achieve_select",
                "id": achieve_id
            }
        )

    def complaint(self, to_id) -> None:
        self.send_server(
            {
                "cmd": "complaint",
                "id": to_id,
            }
        )

    def send_user_message_code(self, code, content) -> None:
        self.send_server(
            {
                "cmd": "send_user_msg_code",
                "code": code,
                "msg": content
            }
        )

    def delete_message(self, message_id) -> None:
        self.send_server(
            {
                "cmd": "delete_msg",
                "msg_id": message_id
            }
        )

    def gift_coll_item(self, item_id: id, coll_id: str, to: int) -> dict:
        self.send_server(
            {
                "cmd": "gift_coll_item",
                "item_id": item_id,
                "coll_id": coll_id,
                "to_id": to
            }
        )
        return self.listen()

    def get_bets(self) -> objects.Bets:
        self.send_server(
            {
                "cmd": "gb"
            }
        )
        return objects.Bets(self._get_data("bets")).Bets

    def get_game_list(self, min: int = 100, max: int = 10000) -> None:
        self.send_server(
            {
                "cmd": "get_game_list",
                "min": min,
                "max": max
            }
        )

    def lookup_stop(self) -> None:
        self.send_server(
            {
                "cmd": "lookup_stop"
            }
        )

    def get_server(self) -> None:
        self.send_server(
            {
                "cmd": "get_server"
            }
        )

    def update_name(self, nickname: str = None) -> None:
        self.send_server(
            {
                "cmd": "update_name",
                "value": nickname
            }
        )

    def save_note(self, note: str, user_id: int, color: int = 0) -> None:
        self.send_server(
            {
                "cmd": "save_note",
                "note": note,
                "color": color,
                "id": user_id
            }
        )

    def leaderboard_get_by_user(self) -> dict:
        self.send_server(
            {
                "cmd": "get_leaderboard",
            }
        )
        return self._get_data("leaderboard")