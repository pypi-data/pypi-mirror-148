from .utils import objects


class Game:

    def __init__(self, client):
        self.client = client

    def create(self, bet: int = 100, password: str = "", crazy: bool = False, fast: bool = False) -> int:
        self.client.send_server(
            {
                "cmd": "create_game",
                "bet": bet,
                "password": password,
                "fast": fast,
                "crazy": crazy,
            }
        )

        data = self.client._get_data("players_status")
        return data["game_id"]

    def join(self, password: str, game_id) -> None:
        self.client.send_server(
            {
                "cmd": "join",
                "password": password,
                "id": game_id,
            }
        )

    def invite(self, user_id):
        self.client.send_server(
            {
                "cmd": "invite_to_game",
                "user_id": user_id,
            }
        )

    def rejoin(self, position, game_id) -> None:
        self.client.send_server(
            {
                "cmd": "rejoin",
                "p": position,
                "id": game_id,
            }
        )

    def leave(self) -> None:
        self.client.send_server(
            {
                "cmd": "leave",
            }
        )

    def publish(self) -> None:
        return self.client.send_server(
            {
                "cmd": "game_publish",
            }
        )

    def send_smile(self, smile_id: int = 16) -> None:
        self.client.send_server(
            {
                "cmd": "smile",
                "id": smile_id,
            }
        )

    def ready(self) -> None:
        self.client.send_server(
            {
                "cmd": "ready",
            }
        )

    def surrender(self) -> None:
        self.client.send_server(
            {
                "cmd": "surrender",
            }
        )

    def take(self) -> None:
        self.client.send_server(
            {
                "cmd": "take",
            }
        )

    def _pass(self) -> None:
        self.client.send_server(
            {
                "cmd": "pass",
            }
        )

    def player_swap(self, position: int) -> None:
        self.send_server(
            {
                "cmd": "player_swap",
                "id": position,
            }
        )