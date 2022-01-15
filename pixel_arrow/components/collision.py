from dataclasses import dataclass
import pygame as pg
from flecs import Component


@dataclass
class Collision(Component):
    box: pg.Rect
    tiles: list[list[str]]
    offset: pg.math.Vector2 = pg.math.Vector2()
