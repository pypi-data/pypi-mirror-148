import socket
import json
import requests
import threading
import random


class SocketListener:

    def __init__(self, client):
        self.client = client
        self.alive = False
        self.socket = None
        self.handlers = {}

    def create_connection(self, server_id: str = None, ip: str = None, port: int = None):
        """
        **Parametrs**
            - server_id ::
                "u1" - Emerald
                "u2" - Sapphire
                "u3" - Amethyst
                "u4" - Topaz
                None - random
        """
        if not ip:
            servers = self.get_servers()["user"]
            server = servers[server_id] if server_id else list(random.choice(list(servers.items())))[1]
            ip = server["host"]
            port = server["port"]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print((ip, port))
            self.socket.connect((ip, port))
        except Exception as e:
            if "error" in self.handlers:
                self.handlers["error"](e)
        self.alive = True
        threading.Thread(target=self.receive_messages).start()

    def send_server(self, data: dir):
        s_data = (json.dumps(data, separators=(',', ':')).replace("{}", '')+'\n').encode()
        self.socket.send(s_data)

    def get_servers(self):
        while 1:
            try:
                response = requests.get(f"{self.api_url}servers.json").json()
                return response
            except Exception as e:
                if "error" in self.handlers:
                    self.handlers["error"](e)
                continue

    def event(self, command: str = "all"):
        def register_handler(handler):
            if command in self.handlers:
                self.handlers[command].append(handler)
            else:
                self.handlers[command] = [handler]
            return handler

        return register_handler

    def error(self):
        def register_handler(handler):
            self.handlers["error"] = handler
            return handler

        return register_handler

    def receive_messages(self):
        self.logger.debug(f"{self.tag}: Start listener")
        while self.alive:
            buffer = bytes()
            while self.alive:
                try:
                    r = self.socket.recv(4096)
                except Exception as e:
                    if "error" in self.handlers:
                        self.handlers["error"](e)
                    self.alive = False
                    return
                buffer = buffer + r
                read = len(r)
                if read != -1:
                    if read in [0, 1]: continue
                    try:
                        d = buffer.decode()
                    except:
                        continue
                    if d.endswith('\n'):
                        buffer = bytes()
                        for str in d.strip().split('\n'):
                            try:
                                data = json.loads(str)
                            except Exception as e:
                                continue
                            self.logger.debug(f"{self.tag}: {data}")
                            for handler_command in self.handlers:
                                if handler_command in ["all", data["cmd"]]:
                                    for handler in self.handlers[handler_command]:
                                        handler(data)
                            self.receive.append(data)
                    else:
                        continue
                else:
                    self.socket.close()
                    return

    def listen(self, force: bool = False):
        while len(self.receive) == 0:
            if force:
                return {"cmd": "empty"}
        r = self.receive[0]
        del self.receive[0]
        return r

    def _get_data(self, type, force: bool = False):
        data = self.listen(force=force)
        while 1:
            if data["cmd"] in [type, "err", "empty", "alert"]:
                return data
            data = self.listen(force=force)