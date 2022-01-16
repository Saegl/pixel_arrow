import pygame as pg

from flecs.scene import Scene
from flecs.framework import GameFramework

from pixel_arrow.systems.background import BackgroundRenderer
from pixel_arrow.systems.debug_utils import MouseClicks
from pixel_arrow.systems.ui import MenuPopup


class MenuScene(Scene):
    def __init__(self, game: GameFramework) -> None:
        super().__init__(game)

        self.add_system(BackgroundRenderer(self.game.res.images.background))
        self.add_system(MenuPopup(self))

        # self.add_system(MouseClicks())

    def on_keydown(self, event: pg.event.Event):
        if event.key == pg.K_ESCAPE:
            self.game.pop()
