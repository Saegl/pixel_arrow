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


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("My pygame Window")

        self.clock = pygame.time.Clock()
        self.window_size = (800, 450)
        self.framerate = 60
        self.font = pygame.font.SysFont("Arial", 18)
        self.fullscreen = True
        if self.fullscreen:
            self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
            # self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
        else:
            self.display = pygame.display.set_mode(self.window_size, 0, 32)
        self.screen = Surface((1536, 864))
        self.info_text = "no info"
        self.images = ImageStore.load_images(self.screen.get_size())

        self.map = Map("map.txt", self.images, self.screen)
        self.player = Player(self.images, self.screen, self.map, self)
        self.arrows = Arrows(self.images, self.screen, self)

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
        self.player.draw()
        self.arrows.draw()

        screen.blit(self.update_fps(), (10, 0))
        screen.blit(
            self.font.render(self.info_text, 1, pygame.Color("coral")), (10, 25)
        )

        surf = pygame.transform.scale(screen, self.display.get_size())
        self.display.blit(surf, (0, 0))

    def update(self, dt):
        self.arrows.update()
        self.player.update()

    def on_keydown(self, event: Event):
        if event.key == K_a:
            self.player.attack()
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
        while True:
            self.update(dt)
            self.draw()

            for event in pygame.event.get():
                handler = self.event_handlers.get(event.type)
                if handler:
                    handler(event)

            dt = self.clock.tick_busy_loop(self.framerate)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.gameloop()
