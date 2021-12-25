import sys
import pygame
from pygame.event import Event

from pygame.locals import *
from pygame.surface import Surface
from arrows import Arrows

from image_store import ImageStore
from player import Player
from gamemap import Map
from vector import Vector2D
from udpclient import Client


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("My pygame Window")

        self.clock = pygame.time.Clock()
        self.window_size = (800, 450)
        self.framerate = 60
        self.font = pygame.font.SysFont("Arial", 18)
        self.fullscreen = False
        if self.fullscreen:
            self.display = pygame.display.set_mode(
                (0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF
            )
            # self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
        else:
            self.display = pygame.display.set_mode(self.window_size, 0, 32)
        self.screen = Surface((1536, 864))
        self.info_text = "no info"
        self.images = ImageStore.load_images(self.screen.get_size())

        self.map = Map("map.txt", self.images, self.screen)
        self.player = Player(Vector2D(50.0, 500.0), True, self.images, self.screen, self.map, self)
        self.arrows = Arrows(self.images, self.screen, self)

        self.opponents = []
        self.everyone_invisible = False

        self.event_handlers = {
            QUIT: self.on_quit,
            KEYDOWN: self.on_keydown,
            KEYUP: self.on_keyup,
        }

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, 1, pygame.Color("coral"))
        return fps_text

    def draw(self):
        screen = self.screen
        screen.blit(self.images.background, (0, 0))

        self.map.draw()
        self.arrows.draw()

        self.player.draw()
        for opponent in self.opponents:
            opponent.draw()

        screen.blit(self.update_fps(), (10, 0))
        screen.blit(
            self.font.render(self.info_text, 1, pygame.Color("coral")), (10, 25)
        )

        surf = pygame.transform.scale(screen, self.display.get_size())
        self.display.blit(surf, (0, 0))

    def update(self, dt, opponents):
        self.arrows.update()
        self.player.update()

        self.everyone_invisible = True
        for i, opponent_data in enumerate(opponents):
            opponent = self.opponents[i]
            (
                opponent.attacking,
                opponent.moving_right,
                opponent.moving_left,
                opponent.moving_down,
                opponent.moving_up,
            ) = opponent_data
            opponent.update()
            if opponent.visible: self.everyone_invisible = False
        self.everyone_invisible = self.everyone_invisible and self.player.visible

    def create_opponents(self, opponents_spawn):
        for opponent_spawn in opponents_spawn:
            pos = Vector2D(opponent_spawn[0], opponent_spawn[1])
            opponent = Player(pos, False, self.images, self.screen, self.map, game)
            opponent.update()
            self.opponents.append(opponent)

    def on_keydown(self, event: Event):
        if event.key == K_a:
            self.player.attacking = True
        if event.key == K_RIGHT:
            self.player.moving_right = True
        if event.key == K_LEFT:
            self.player.moving_left = True
        if event.key == K_DOWN:
            self.player.moving_down = True
        if event.key == K_UP:
            self.player.moving_up = True
        if event.key == K_ESCAPE:
            self.on_quit()

    def on_keyup(self, event: Event):
        if event.key == K_RIGHT:
            self.player.moving_right = False
        if event.key == K_LEFT:
            self.player.moving_left = False
        if event.key == K_DOWN:
            self.player.moving_down = False
        if event.key == K_UP:
            self.player.moving_up = False

    def on_quit(self, __event: Event = None):
        pygame.quit()
        sys.exit()

    def gameloop(self):
        dt = 0
        client = Client()
        spawners = client.wait_for_players()
        my_spawn = spawners[client.cliend_id]
        self.player.location = Vector2D(my_spawn[0], my_spawn[1])
        opponents_spawn = spawners[:client.cliend_id] + spawners[client.cliend_id + 1:]
        self.create_opponents(opponents_spawn)
        
        while True:
            opponents_data = client.send(
                [
                    self.player.attacking,
                    self.player.moving_right,
                    self.player.moving_left,
                    self.player.moving_down,
                    self.player.moving_up,
                ]
            )
            if len(opponents_data[0]) == 2:
                print("New game started")
                self.player.hp = 5
                self.player.visible = True
                self.arrows.arrows = []
                spawners = opponents_data
                my_spawn = spawners[client.cliend_id]
                self.player.location = Vector2D(my_spawn[0], my_spawn[1])
                opponents_spawn = spawners[:client.cliend_id] + spawners[client.cliend_id + 1:]
                for i, opponent in enumerate(self.opponents):
                    loc = opponents_spawn[i]
                    opponent.location = Vector2D(loc[0], loc[1])
                    opponent.visible = True
                    opponent.hp = 5
            else:
                self.update(dt, opponents_data)
            self.draw()

            for event in pygame.event.get():
                handler = self.event_handlers.get(event.type)
                if handler:
                    handler(event)

            pygame.display.update()
            # dt = self.clock.tick_busy_loop(self.framerate)
            if self.everyone_invisible:
                client.winner()
            dt = self.clock.tick(self.framerate)


def main():
    game = Game()
    game.gameloop()

if __name__ == "__main__":
    game = Game()
    game.gameloop()
