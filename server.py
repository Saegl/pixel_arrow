import socket
import threading
from _thread import *
import pickle


class Server:
    def __init__(self) -> None:
        server = "192.168.0.103"
        port = 5555

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((server, port))

        self.sock.listen(2)
        self.player_id = 0
        self.number_of_players = 2
        self.players_data = [None] * self.number_of_players
        self.players_data_lock = threading.Lock()

        print("Waiting for a connection, Server Started")
        self.loop()

    def threaded_client(self, conn, barrier):
        client_id = self.player_id
        conn.send(str.encode(str(client_id)))
        self.player_id += 1

        while True:
            try:
                data = pickle.loads(conn.recv(64))
                # print(data)
                # with self.players_data_lock:
                self.players_data[client_id] = data

                barrier.wait()
                opponents_data = (
                    self.players_data[:client_id] + self.players_data[client_id + 1 :]
                )
                conn.send(pickle.dumps(opponents_data))
            except:
                break

        print("Lost connection")
        conn.close()

    def loop(self):
        barrier = threading.Barrier(self.number_of_players)
        while True:
            conn, addr = self.sock.accept()
            print("Connected to:", addr)

            start_new_thread(self.threaded_client, (conn, barrier))


Server()
