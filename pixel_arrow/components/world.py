import pygame as pg
from dataclasses import dataclass
from flecs import Component
from pixel_arrow.config import screen_size


@dataclass
class Tiles(Component):
    width: int
    height: int
    grid: list[list[str]]

    @staticmethod
    def from_file(filename) -> "Tiles":
        tiles = Tiles(100, 100, [["0"] * 100 for _ in range(100)])

        with open(filename, "r", encoding="utf-8") as f:
            width, height = map(int, f.readline().split())

            for y in range(height):
                line = f.readline()
                for x in range(width):
                    cellval = line[x]
                    tiles.grid[x][y] = cellval

            tiles.width = width
            tiles.height = height

        return tiles


@dataclass
class World(Component):
    surf: pg.Surface = pg.Surface((2000.0, 2000.0), pg.SRCALPHA)
    clipping_rect: pg.Rect = pg.Rect(0, 0, screen_size[0], screen_size[1])
