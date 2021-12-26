import sys
import pygame as pg

from pygame.locals import *
from pygame.event import Event

from pixel_arrow.framework import Scene, GameFramework
from pixel_arrow.multiplayer_scene import MultiplayerScene


class EmptyScene(Scene):
    def __init__(self, game: GameFramework) -> None:
        super().__init__(game)

    def draw(self):
        screen = self.game.screen
        res = self.game.res
        screen.blit(res.images.background, (0, 0))
        surf = pg.transform.scale(screen, self.game.display.get_size())
        self.game.display.blit(surf, (0, 0))

    def update(self, dt):
        pass

    def on_keydown(self, event: Event):
        if event.key == K_ESCAPE:
            self.game.pop()

    def on_keyup(self, _: Event):
        pass

    def on_mouse_button_up(self, _: Event):
        print("HEY")
    
    def destroy(self):
        print("Empty Scene destroyed")

    def on_quit(self, _: Event):
        pg.quit()
        sys.exit()
