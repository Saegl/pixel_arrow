from pixel_arrow.mixins import DrawMixin, UpdateMixin
from pixel_arrow.player import Player, PlayerKeys
from pixel_arrow.udpclient import Client, SpawnResponse
from pixel_arrow.vector import Vector2D


class Multiplayer(UpdateMixin, DrawMixin):
    def __init__(self, game, image_store, screen) -> None:
        self.setup_update(game)
        self.setup_draw(image_store, screen)
        self.client = Client()
        self.opponents: list[Player] = []
        
        spawners = self.client.wait_for_players()
        self.create_opponents(len(spawners.opponents))
        self.place_players(spawners)
    
    def place_players(self, spawners: SpawnResponse):
        self.game.player.location = Vector2D(spawners.player[0], spawners.player[1])
        for i, opponent in enumerate(self.opponents):
            spawn_location = spawners.opponents[i]
            opponent.location = Vector2D(spawn_location[0], spawn_location[1])
    
    def create_opponents(self, number_of_opponents: int):
        for _ in range(number_of_opponents):
            opponent = Player(Vector2D(0, 0), False, self.image_store, self.screen, self.game)
            opponent.update(PlayerKeys())
            self.opponents.append(opponent)

    def update(self, current_player_keys: PlayerKeys):
        client = self.client
        opponents_data = client.send_keys(current_player_keys.as_list())

        if not len(opponents_data) == 0 and len(opponents_data[0]) == 2:
            print("New game started")
            self.game.player.hp = 5
            self.game.player.visible = True
            self.game.arrows.arrows = []
            spawners = opponents_data
            my_spawn = spawners[client.cliend_id]
            self.game.player.location = Vector2D(my_spawn[0], my_spawn[1])
            opponents_spawn = (
                spawners[: client.cliend_id] + spawners[client.cliend_id + 1 :]
            )
            for i, opponent in enumerate(self.opponents):
                loc = opponents_spawn[i]
                opponent.location = Vector2D(loc[0], loc[1])
                opponent.visible = True
                opponent.hp = 5
        else:
            for i, opponent_data in enumerate(opponents_data):
                opponent = self.opponents[i]
                keys = PlayerKeys.from_list(opponent_data)
                opponent.update(keys)
            
            everyone_invisible = all(map(lambda o: not o.visible, self.opponents))
            player_wins = everyone_invisible and len(self.opponents) and self.game.player.visible

            if player_wins:
                self.client.winner()
    
    def draw(self):
        for opponent in self.opponents:
            opponent.draw()
