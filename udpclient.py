import socket
from pickle import dumps, loads


buffer_size = 38

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = "192.168.0.103"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.cliend_id = self.get_player_id()

    def get_player_id(self):
        sended_message = 0
        self.client.sendto(dumps(sended_message), self.addr)
        data, addr = self.client.recvfrom(buffer_size)
        return loads(data)
    
    def wait_for_players(self):
        data, addr = self.client.recvfrom(buffer_size)
        return loads(data)
    
    def winner(self):
        self.client.sendto(dumps(-1), self.addr)

    def send(self, data):
        self.client.sendto(dumps([self.cliend_id] + data), self.addr)
        return loads(self.client.recv(buffer_size))


if __name__ == '__main__':
    client = Client()
    print(client.cliend_id)
    spawners = client.wait_for_players()
    my_spawn = spawners[client.cliend_id]
    opponents_spawn = spawners[:client.cliend_id] + spawners[client.cliend_id + 1:]
    print(f"My spawn: {my_spawn}, opponents_spawn: {opponents_spawn}")

    i = 0
    while True:
        sended_message = [True] * 5
        print(f"{client.cliend_id} Sended", sended_message)
        received_message = client.send(sended_message)
        print("Received", received_message)
        if len(received_message[0]) == 2:
            print("New game started")

        from time import sleep

        sleep(3)
        i += 1
        if i % 3 == 0:
            client.winner()
