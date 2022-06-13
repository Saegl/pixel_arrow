import struct
from datetime import datetime
import trio

HOST = "127.0.0.1"
PORT = 12345
SERVER_ADDRESS = (HOST, PORT)
BUFFER_SIZE = 1024


class Message:
    def __init__(self, text, created=None):
        """
        Messages for UDP communication
        They contain text and time since 1 January of 2022
        Can be converted to bytes and back

        >>> m = Message('Hi')
        >>> assert m.text == 'Hi'
        
        as_bytes and from_bytes is inverse function:

        >>> n = Message.from_bytes(m.as_bytes())
        >>> assert n.text == m.text
        >>> assert n.time == m.time
        """
        self.time = created or (datetime.utcnow() - datetime(2022, 1, 1)).total_seconds()
        self.text: str = text
    
    def as_bytes(self):
        return struct.pack('d', self.time) + self.text.encode('utf8')
    
    @staticmethod
    def from_bytes(b: bytes):
        time, = struct.unpack('d', b[0:8])
        text = b[8:].decode('utf8')
        return Message(text, time)
    
    def ping_seconds(self):
        "Calc time since message creation"
        curtime = (datetime.utcnow() - datetime(2022, 1, 1)).total_seconds()
        return curtime - self.time



async def send_message(sock, address, text):
    message_bytes = Message(text).as_bytes()
    await sock.sendto(message_bytes, address)


async def receive_message(sock):
    data_bytes, address = await sock.recvfrom(BUFFER_SIZE)
    message = Message.from_bytes(data_bytes)
    print(f"{message.ping_seconds()}: {message.text}")
    return address


async def sending_input(sock, address):
    while True:
        text: str = await trio.to_thread.run_sync(input)
        await send_message(sock, address, text)


async def receiving_input(sock):
    while True:
        await receive_message(sock)


async def main_server():
    sock = trio.socket.socket(trio.socket.AF_INET, trio.socket.SOCK_DGRAM)
    await sock.bind(SERVER_ADDRESS)
    print("UDP server is started, waiting for client")

    client_address = await receive_message(sock)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(sending_input, sock, client_address)
        nursery.start_soon(receiving_input, sock)

    print("Conversation ended")


async def main_client():
    sock = trio.socket.socket(trio.socket.AF_INET, trio.socket.SOCK_DGRAM)

    await send_message(sock, SERVER_ADDRESS, input())

    async with trio.open_nursery() as nursery:
        nursery.start_soon(sending_input, sock, SERVER_ADDRESS)
        nursery.start_soon(receiving_input, sock)

    print("Conversation ended")


if __name__ == "__main__":
    fajsdfkjfalksdjf
    t = int(input("Choose: [0] Server, [1] Client> "))
    if t == 0:
        trio.run(main_server)
    else:
        trio.run(main_client)
