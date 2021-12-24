import socket
import pickle


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.103"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.cliend_id = int(self.connect())

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(64))
        except socket.error as e:
            print(e)


if __name__ == "__main__":
    n = Client()

    while True:
        sended_message = [False] * 5
        print(f"{n.cliend_id} Sended", sended_message)
        received_message = n.send(sended_message)
        print("Received", received_message)
        from time import sleep

        sleep(3)
