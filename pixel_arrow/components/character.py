from dataclasses import dataclass
from functools import cache

import pygame as pg
from flecs import Component, Scene, Entity
from flecs.image_store import ImageStore, scale_nx, spritesheet, hflips

from pixel_arrow.components.world import Tiles
from pixel_arrow.components.collision import Collision
from pixel_arrow.components.animation import AnimationState, Animation
from pixel_arrow.components.position import Position


@cache
def load_character_animations(images: ImageStore) -> list[AnimationState]:
    player_idle = spritesheet(scale_nx(images.player_idle24x24, 3), 72, 72, 3)
    player_run = spritesheet(scale_nx(images.player_run24x24, 3), 72, 72, 8)
    player_jump = spritesheet(scale_nx(images.player_jump24x24, 3), 72, 72, 4)
    player_attack = spritesheet(scale_nx(images.player_attack24x24, 3), 72, 72, 5)
    character_animations = [
        AnimationState(
            hflips(player_idle), player_idle,
            cyclic=True
        ),
        AnimationState(
            hflips(player_run), player_run,
            cyclic=True
        ),
        AnimationState(
            hflips(player_jump), player_jump,
            cyclic=False
        ),
        AnimationState(
            hflips(player_attack), player_attack,
            cyclic=False
        ),
    ]
    return character_animations


def create_player(scene: Scene, tiles: Tiles) -> Entity:
    character_animations = load_character_animations(scene.game.res.images)
    col_x_offset = 10.0
    col_y_offset = 10.0
    return scene.create_enitity(
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
