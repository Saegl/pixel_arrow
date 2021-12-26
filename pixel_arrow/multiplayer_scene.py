import sys
import pygame as pg
from pygame.event import Event

from pygame.locals import *
from pygame.surface import Surface

from pixel_arrow.arrows import Arrows
from pixel_arrow.image_store import ImageStore
from pixel_arrow.player import Player, PlayerKeys
from pixel_arrow.gamemap import Map
from pixel_arrow.vector import Vector2D
from pixel_arrow.framework import Scene, GameFramework
from pixel_arrow.multiplayer import Multiplayer


class MultiplayerScene(Scene):
    def __init__(self, game: GameFramework) -> None:
        super().__init__(game)

        self.info_text = "no info"
        
        images = game.res.images

        map2 = self.create_enitty()

        self.map = Map("map.txt", images, self.game.screen)
        self.player = Player(
            Vector2D(50.0, 500.0), True, images, self.game.screen, self
        )
        self.arrows = Arrows(images, self.game.screen, self)
        self.multiplayer = Multiplayer(self, images, self.game.screen)

    def update_fps(self):
        fps = str(int(self.game.clock.get_fps()))
        fps_text = self.game.res.font.render(fps, 1, pg.Color("coral"))
        return fps_text

    def draw(self):
        screen = self.game.screen
        res = self.game.res

        screen.blit(res.images.background, (0, 0))

        self.map.draw()
        self.arrows.draw()
        self.player.draw()
        self.multiplayer.draw()

        screen.blit(self.update_fps(), (10, 0))
        screen.blit(res.font.render(self.info_text, 1, pg.Color("coral")), (10, 25))

        surf = pg.transform.scale(screen, self.game.display.get_size())
        self.game.display.blit(surf, (0, 0))

    def update(self, dt):
        self.arrows.update()
        current_player_keys = PlayerKeys.from_pressed(self.game.pressed_keys)
        self.player.update(current_player_keys)
        self.multiplayer.update(current_player_keys)

    def on_keydown(self, event: Event):
        if event.key == K_ESCAPE:
            self.game.pop()

    def on_keyup(self, _: Event):
        pass

    def destroy(self):
        print("Multiplayer Scene Destroyed")

    def on_quit(self, _: Event = None):
        pg.quit()
        sys.exit()