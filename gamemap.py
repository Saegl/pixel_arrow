import pygame
from pygame.rect import Rect

from mixins import DrawMixin
from vector import Vector2D


def cell_to_rect(x, y, tile_size):
    return pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)


class Map(DrawMixin):
    def __init__(self, filename, image_store, screen) -> None:
        self.setup_draw(image_store, screen)

        self.tile_size = 48

        with open(filename, "r", encoding="utf-8") as f:
            m, n = map(int, f.readline().split())
            # self.cells = [[0] * n for _ in range(m)]
            self.cells = [[0] * 100 for _ in range(100)]

            for y in range(n):
                line = f.readline()
                for x in range(m):
                    cellval = line[x]
                    self.cells[x][y] = cellval

            self.m = m
            self.n = n

    def draw(self):
        screen = self.screen
        for x in range(self.m):
            for y in range(self.n):
                tile_type = self.cells[x][y]
                if tile_type != '0':
                    screen.blit(
                        self.image_store.tiles[tile_type], (x * self.tile_size, y * self.tile_size)
                    )
    
    def grid_loc(self, point: Vector2D) -> Vector2D:
        return Vector2D(point.x // self.tile_size, point.y // self.tile_size)
    
    def tile_type(self, pos: Vector2D) -> str:
        return self.cells[pos.x][pos.y]
    
    def cell_to_rect(self, pos: Vector2D) -> Rect:
        x = pos.x
        y = pos.y
        tile_size = self.tile_size
        return pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
