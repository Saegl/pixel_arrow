import subprocess
from time import sleep

# subprocess.Popen(['python', '-m', 'pip', 'install', 'pygame'])

number_of_clients = 1

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
