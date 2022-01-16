import pygame as pg
from dataclasses import dataclass
from functools import cache

from flecs import Component, Scene
from flecs.image_store import ImageStore, scale_nx, spritesheet, hflips

from pixel_arrow.components.position import Position
from pixel_arrow.components.animation import Animation, AnimationState
from pixel_arrow.components.collision import Collision


@cache
def load_arrow_animations(images: ImageStore) -> list[AnimationState]:
    arrow_idle = spritesheet(scale_nx(images.arrow_idle12x12, 3), 36, 3)
    arrow_stuck = spritesheet(scale_nx(images.arrow_stuck12x12, 3), 36, 9)
    return [
        AnimationState(
            hflips(arrow_idle), arrow_idle,
            cyclic=True
        ),
        AnimationState(
            hflips(arrow_stuck), arrow_stuck,
            cyclic=False
        ),
    ]


def launch_arrow(scene: Scene, pos: pg.math.Vector2, left: bool):
    arrow_animations = load_arrow_animations(scene.game.res.images)
    scene.create_enitity(
        Arrow(),
        Position(pos),
        Animation(
            arrow_animations,
            look_left=left,
        ),
        Collision(
            pg.Rect(pos.x, pos.y, 36, 12),
            tiles=scene.tiles.grid,
            offset=pg.math.Vector2(0.0, 12.0),
        ),
    )


@dataclass
class Arrow(Component):
    frames_since_stuck = 0
