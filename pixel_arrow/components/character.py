from dataclasses import dataclass
import pygame as pg
from flecs import Component, Scene
from flecs.image_store import load_animation

from pixel_arrow.components.world import Tiles
from pixel_arrow.components.collision import Collision
from pixel_arrow.components.animation import AnimationState, Animation
from pixel_arrow.components.position import Position


character_animations = [
    AnimationState(
        *load_animation("pixel_arrow/res/images/Player/Player-Idle-24x24.png", 72, 3),
        cyclic=True
    ),
    AnimationState(
        *load_animation("pixel_arrow/res/images/Player/Player-Run-24x24.png", 72, 8),
        cyclic=True
    ),
    AnimationState(
        *load_animation("pixel_arrow/res/images/Player/Player-Jump-24x24.png", 72, 4),
        cyclic=False
    ),
    AnimationState(
        *load_animation("pixel_arrow/res/images/Player/Player-Attack-24x24.png", 72, 5),
        cyclic=False
    ),
]


def create_player(scene: Scene, tiles: Tiles) -> int:
    col_x_offset = 10.0
    col_y_offset = 10.0
    player_id = scene.create_enitity(
        Position(pg.math.Vector2(50.0, 500.0)),
        CharacterState(),
        CharacterMovement(),
        UserControlled(),
        Animation(character_animations),
        Collision(
            pg.Rect(0.0, 0.0, 72.0 - col_x_offset * 2, 72.0 - col_y_offset),
            tiles.grid,
            offset=pg.math.Vector2(col_x_offset, col_y_offset),
        ),
    )
    return player_id


@dataclass
class UserControlled(Component):
    pass


@dataclass
class CharacterState(Component):
    hp: int = 5
    attacking: bool = False
    frames_since_attack: int = 0


@dataclass
class CharacterMovement(Component):
    movement: pg.math.Vector2 = pg.math.Vector2(0.0, 0.0)
    momentum: pg.math.Vector2 = pg.math.Vector2(0.0, 0.0)
