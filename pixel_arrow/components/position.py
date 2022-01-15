import pygame as pg
from dataclasses import dataclass
from flecs import Component


@dataclass
class Position(Component):
    v: pg.math.Vector2
