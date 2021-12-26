import socket
from dataclasses import dataclass
from pickle import dumps, loads

from pixel_arrow import config


@dataclass
class SpawnResponse:
    player: tuple[float]
    opponents: list[tuple[float]]


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = config.host
        self.port = config.port
        self.addr = (self.host, self.port)
        self.buffer_size = config.buffer_size
        self.cliend_id = self.get_player_id()
        print(self.cliend_id)

    def sendto_server(self, data):
        self.sock.sendto(dumps(data), self.addr)

    def recvfrom_server(self):
        data = self.sock.recv(self.buffer_size)
        return loads(data)

    def get_player_id(self):
        sended_message = 0
        self.sendto_server(sended_message)
        return self.recvfrom_server()

    def wait_for_players(self) -> SpawnResponse:
        spawners_data = self.recvfrom_server()
        player_spawn = spawners_data[self.cliend_id]
        opponents_spawn = (
            spawners_data[: self.cliend_id]
            + spawners_data[self.cliend_id + 1 :]
        )
        return SpawnResponse(player_spawn, opponents_spawn)

    def winner(self):
        self.sendto_server(-1)

    def send_keys(self, data):
        self.sendto_server([self.cliend_id] + data)
        return self.recvfrom_server()
