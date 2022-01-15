import pygame as pg
from dataclasses import dataclass

from flecs import Component, Scene
from flecs.image_store import load_animation

from pixel_arrow.components.position import Position
from pixel_arrow.components.animation import Animation, AnimationState
from pixel_arrow.components.collision import Collision

arrow_animations = [
    AnimationState(
        *load_animation(
            "pixel_arrow/res/images/Objects/Obj-Arrow-Idle-12x12.png", 36, 3
        ),
        cyclic=True
    ),
    AnimationState(
        *load_animation(
            "pixel_arrow/res/images/Objects/Obj-Arrow-Stuck-12x12.png", 36, 9
        ),
        cyclic=False
    ),
]


def launch_arrow(scene: Scene, pos: pg.math.Vector2, left: bool):
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
