import pathlib
from dataclasses import dataclass

import pygame as pg
from flecs import Scene, System

from cutecats.components.world import DecorativeTiles, TileSets, CollisionTiles, World
from cutecats.components.position import Position
from flecs.image_store import ImageStore


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
    tile_size: int = 16

    def process(self, _, scene: Scene):
        world: World = scene.get_component(World)
        tiles: CollisionTiles = scene.get_component(CollisionTiles)
        tileset: TileSets = scene.get_component(TileSets)

        images = scene.game.res.images
        for x in range(tiles.width):
            for y in range(tiles.height):
                tile_type = tiles.get(x, y)
                if tile_type != 0:
                    world.surf.blit(
                        tileset.tile_images[tile_type],
                        (x * tileset.tilewidth, y * tileset.tilewidth),
                    )
        
        for entity, (tiles, ) in scene.get_entities(DecorativeTiles):
            tiles: DecorativeTiles
            # TODO copy paste
            for x in range(tiles.width):
                for y in range(tiles.height):
                    tile_type = tiles.get(x, y)
                    if tile_type != 0:
                        world.surf.blit(
                            tileset.tile_images[tile_type],
                            (x * tileset.tilewidth, y * tileset.tilewidth),
                        )


# lower is faster, 1 is fastest
CHARACTER_CAMERA_LAG = 20


@dataclass
class CharacterCameraClipping(System):
    def process(self, _, scene: Scene):
        world: World = scene.get_component(World)
        # TODO get component by eid method
        player_pos: Position = scene.entities[1][Position]
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
        screen.blit(clipping_surf, world.offset)


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
