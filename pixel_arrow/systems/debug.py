import pygame as pg
from dataclasses import dataclass, field

from flecs import Scene, System

from pixel_arrow.components.collision import Collision


@dataclass
class MouseClicks(System):
    rects: list[pg.Rect] = field(default_factory=list)

    def on_mouse_button_up(self, _: pg.event.Event):
        pos = self.scene.game.get_mouse_pos()
        self.rects.append(pg.Rect(pos[0], pos[1], 100, 100))

    def process(self, dt, scene: Scene):
        scene.game.debug_info["mouse clicks"] = "active"

        for rect in self.rects:
            pg.draw.rect(scene.game.debug_screen, (255, 0, 0), rect)

        pg.draw.rect(
            scene.game.debug_screen,
            (0, 200, 0),
            pg.Rect(scene.game.screen_x_offset, scene.game.screen_y_offset, 10, 10),
        )

        mouse_pos = scene.game.get_mouse_pos()
        pg.draw.rect(
            scene.game.debug_screen,
            (0, 200, 0),
            pg.Rect(mouse_pos[0], mouse_pos[1], 10, 10),
        )


@dataclass
class CollisionsDebugRenderer(System):
    def process(self, _, scene: Scene):
        scene.game.debug_info["collisions debug"] = "active"
        for _, (colls,) in scene.get_entities(Collision):
            colls: Collision
            pg.draw.rect(
                scene.game.debug_screen,
                (200, 0, 0, 100),
                colls.box,
            )
