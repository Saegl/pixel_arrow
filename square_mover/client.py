import pickle  # FIXME RED: THIS IS UNSAFE, DON'T RUN OUTSIDE LOCALHOST
import multiprocessing as mp
from multiprocessing.connection import Connection

import trio

from square_mover.network_packets import GameState, PlayerAction
from square_mover.config import buffer_size


async def send_action(sock, action, address):
    encoded = pickle.dumps(action)
    await sock.sendto(encoded, address)


async def receiving_game_state(network_conn: Connection, sock):
    while True:
        data, address = await sock.recvfrom(buffer_size)
        game_state = pickle.loads(data)
        network_conn.send(game_state)


async def sending_actions(network_conn: Connection, sock, address):
    while True:
        action = await trio.to_thread.run_sync(network_conn.recv)        
        await send_action(sock, action, address)


async def main(network_conn):
    server_address = ("127.0.0.1", 5555)
    print("Trio client is running")

    sock = trio.socket.socket(trio.socket.AF_INET, trio.socket.SOCK_DGRAM)
    
    print('Sending first message to connect server and auto bind client address')
    await send_action(sock, PlayerAction(True, True, True, True), server_address)

    
    async with trio.open_nursery() as nursery:
        nursery.start_soon(receiving_game_state, network_conn, sock)
        nursery.start_soon(sending_actions, network_conn, sock, server_address)


def run(network_conn):
    trio.run(main, network_conn)


if __name__ == '__main__':
    run()
