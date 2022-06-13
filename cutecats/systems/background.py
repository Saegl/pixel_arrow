from dataclasses import dataclass
import pygame as pg

from flecs import Scene, System


@dataclass
class BackgroundRenderer(System):
    image: pg.Surface

    def process(self, dt, scene: Scene):
        scene.game.screen.blit(self.image, (0, 0))
