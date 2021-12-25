import socket
from pickle import dumps, loads
from random import shuffle


server = "0.0.0.0"
port = 5555
buffer_size = 38

number_of_players = 3
players_data = [[False] * 5 for _ in range(number_of_players)]
players_addresses = []
spawn_places = [(50, 500), (1400, 50), (100, 50)]
last_player = 0

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind((server, port))

def send_spawn():
    print("SPAWN SENDED")
    shuffle(spawn_places)
    for addr in players_addresses:
        socket.sendto(dumps(spawn_places[:number_of_players]), addr)


print("UDP server started")

while True:
    message, address = socket.recvfrom(buffer_size)
    message = loads(message)

    if message == 0: # Get Player Id
        socket.sendto(dumps(last_player), address)
        players_addresses.append(address)
        last_player += 1
        if last_player == number_of_players:
            send_spawn()
            
    elif message == -1: # Player Wins
        send_spawn()
    else: # Send players keys
        client_id = message[0]
        data = message[1:]
        players_data[client_id] = data
        
        opponents_data = (
            players_data[:client_id] + players_data[client_id + 1 :]
        )
        socket.sendto(dumps(opponents_data), address)
