import pickle # FIXME DANGEROUS!!!
import time
import trio
from square_mover.config import buffer_size, address as server_address
from square_mover.network_packets import GameState, PlayerAction


player_state = PlayerAction(False, False, False, False)
game_state = GameState(0.0, 0.0)
last_time = time.time()

MOVE_SPEED = 60.0
UPDATERATE = 60 # ticks per second

def update_game_state():
    global last_time, player_state
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    
    dx, dy = 0, 0
    if player_state.up:
        dy -= MOVE_SPEED
    if player_state.down:
        dy += MOVE_SPEED
    if player_state.left:
        dx -= MOVE_SPEED
    if player_state.right:
        dx += MOVE_SPEED
    
    game_state.x += dx * dt
    game_state.y += dy * dt


async def client_connected_signal(sock):
    data, address = await sock.recvfrom(buffer_size)
    # TODO check data
    return address


async def receiving_actions(sock):
    global player_state
    while True:
        data, address = await sock.recvfrom(buffer_size)
        player_state = pickle.loads(data)

async def sending_game_state(sock, address):
    while True:
        await trio.sleep(1 / UPDATERATE)
        update_game_state()
        await sock.sendto(pickle.dumps(game_state), address)



async def main(server_address):
    sock = trio.socket.socket(trio.socket.AF_INET, trio.socket.SOCK_DGRAM)
    await sock.bind(server_address)

    print('UDP server started, waiting for client')
    client_address = await client_connected_signal(sock)
    print("Client connected")

    async with trio.open_nursery() as nursery:
        nursery.start_soon(receiving_actions, sock)
        nursery.start_soon(sending_game_state, sock, client_address)

def run(server_address):
    trio.run(main, server_address)


if __name__ == '__main__':
    run(server_address)
