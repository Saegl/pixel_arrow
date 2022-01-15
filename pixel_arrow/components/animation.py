from dataclasses import dataclass
import pygame as pg
from flecs import Component


@dataclass
class AnimationState:
    images_left: list[pg.Surface]
    images_right: list[pg.Surface]
    cyclic: bool = False


@dataclass
class Animation(Component):
    states: list[AnimationState]
    current_state: int = 0
    frames: int = 0
    look_left: bool = False
