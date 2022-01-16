from dataclasses import dataclass

import pygame as pg
from pixel_arrow.components.position import Position
from flecs import Scene, System, Entity
from pixel_arrow.components.world import Tiles, World


def clamp(value: float, a: float, b: float) -> float:
    """
    Clamp value between a and b
    a <= result <= b
    """
    if value < a:
        return a
    elif value > b:
        return b
    else:
        return value


@dataclass
class MapRenderer(System):
    tile_size: int = 48

    def process(self, _, scene: Scene):
        world: World = scene.get_component(World)
        tiles: Tiles = scene.get_component(Tiles)

        images = scene.game.res.images
        for x in range(tiles.m):
            for y in range(tiles.n):
                tile_type = tiles.grid[x][y]
                if tile_type != "0":
                    world.surf.blit(
                        images.tiles[tile_type],
                        (x * self.tile_size, y * self.tile_size),
                    )


# lower is faster, 1 is fastest
CHARACTER_CAMERA_LAG = 20


@dataclass
class CharacterCameraClipping(System):
    def __init__(self, character_entity: Entity):
        self.character_entity = character_entity

    def process(self, _, scene: Scene):
        world: World = scene.get_component(World)
        player_pos = self.character_entity.get_component(Position)
        screen = scene.game.screen

        new_clipping_rect = screen.get_rect()
        new_clipping_rect.center = player_pos.v.xy

        new_clipping_rect.x = clamp(
            new_clipping_rect.x, 0, world.surf.get_width() - screen.get_width()
        )
        new_clipping_rect.y = clamp(
            new_clipping_rect.y, 0, world.surf.get_height() - screen.get_height()
        )

        dx = new_clipping_rect.x - world.clipping_rect.x
        dy = new_clipping_rect.y - world.clipping_rect.y

        world.clipping_rect.x += dx // CHARACTER_CAMERA_LAG
        world.clipping_rect.y += dy // CHARACTER_CAMERA_LAG


@dataclass
class WorldCameraClear(System):
    def process(self, _, scene: Scene):
        world: World = scene.get_component(World)
        world.surf.fill((0, 0, 0, 0), world.clipping_rect)


@dataclass
class WorldCameraRender(System):
    def process(self, _, scene: Scene):
        world: World = scene.get_component(World)
        screen = scene.game.screen
        clipping_surf = world.surf.subsurface(world.clipping_rect)
        screen.blit(clipping_surf, (0, 0))


@dataclass
class MouseCameraClipping(System):
    def process(self, _, scene: Scene):
        world: World = scene.get_component(World)
        screen = scene.game.screen

        right_click_pressed = pg.mouse.get_pressed()[2]
        x, y = pg.mouse.get_rel()
        if right_click_pressed:
            world.clipping_rect.x -= x
            world.clipping_rect.y -= y

            world.clipping_rect.x = max(0, world.clipping_rect.x)
            world.clipping_rect.y = max(0, world.clipping_rect.y)
