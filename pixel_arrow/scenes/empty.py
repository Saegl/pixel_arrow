import pygame as pg

from flecs import Scene, GameFramework


class EmptyScene(Scene):
    def __init__(self, game: GameFramework) -> None:
        super().__init__(game)

    def on_keydown(self, event: pg.event.Event):
        if event.key == pg.K_ESCAPE:
            self.game.pop()
