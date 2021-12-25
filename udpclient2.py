from udpclient import *


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
