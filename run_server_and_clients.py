import subprocess
from time import sleep

from pixel_arrow import config

# subprocess.Popen(['python', '-m', 'pip', 'install', 'pygame'])

number_of_clients = config.number_of_players

server = subprocess.Popen(['python', 'run_udpserver.py'])
print("Waiting server to start, don't close")
sleep(2)

clients = []
for _ in range(number_of_clients):
    clients.append(subprocess.Popen(['python', 'run_game.py']))

try:
    print("now you can close")
    sleep(60*60*24)
except:
    server.kill()
    for client in clients: client.kill()
