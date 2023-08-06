import base64
import hashlib
from datetime import datetime
from .utils import objects


class Authorization:

    def __init__(self, client) -> None:
        self.client = client

    def get_session_key(self) -> None:
        data = {
            "cmd": "c",
            "l": "ru",
            "tz": "+02:00",
            "t": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z",
            "pl": self.client.pl,
            "p": 13,
        }
        if self.client.pl == "ios":
            data.update({
                "v": "1.8.0",
                "ios": "14.4",
                "d": "iPhone8,4",
                "n": "loto.ios",
            })
        else:
            data.update({
                "v": "1.8.0",
                "d": "xiaomi cactus",
                "and": 28,
                "n": f"loto.{self.client.pl}",
            })
        self.client.send_server(data)

    def sign(self, key: str) -> dict:
        hash = base64.b64encode(hashlib.md5((f"{key}fnd;vnbwk;vb ejkwfkjew fwek fewkj fjekw; f;kao oboiboniuj").encode()).digest()).decode()
        self.client.send_server(
            {
                "cmd": "sign",
                "hash": hash,
            }
        )
        return self.client.listen()

    def signin_by_access_token(self, token: str, name: str = "") -> int:
        self.client.token = token
        self.client.send_server(
            {
                "cmd": "authorization",
                "token": token,
                "ln": "ru",
                "device_token": "",
                "name": name,
                "version": "app.android.1.8.0.(build 30.11.1979 0:00)",
            }
        )
        user = self.client._get_data("user_update")["user"]
        self.client.uid = user["id"]
        self.client.logger.debug(f"{self.client.tag}: Success auth")
        return user

    def google_auth(self, id_token: str) -> dict:
        self.client.send_server(
            {
                "cmd": "loto_google_auth",
                "id_token": id_token,
            }
        )
        return self.client.listen()