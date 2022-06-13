from dataclasses import dataclass
import pygame as pg
from flecs import Component


@dataclass
class AnimationState:
    images_left: list[pg.Surface]
    images_right: list[pg.Surface]
    cyclic: bool = False
    image_duration: int = 10

    def __len__(self):
        # TODO what if len(images_left) != len(images_right)?
        return len(self.images_left)

    @property
    def duration(self):
        return len(self) * self.image_duration


@dataclass
class Animation(Component):
    states: list[AnimationState]
    current_state: int = 0
    frames: int = 0
    look_left: bool = False
