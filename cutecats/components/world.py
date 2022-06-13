import json
import pathlib
from dataclasses import dataclass
import pygame as pg
from flecs import Component
from flecs.image_store import ImageStore, spritesheet
from cutecats.config import screen_size


class TileSets(Component):
    def __init__(self, json_data, images: ImageStore):
        tilemap_dir = pathlib.Path('cutecats/res/tilemaps')
        tilesets = json_data
        
        # TODO: This is a hack.
        self.tileheight = 16
        self.tilewidth = 16

        self.tile_images = [pg.Surface((0, 0))]  # shift tileindex by 1

        for tileset in tilesets:
            if 'source' in tileset:
                # external tileset
                with open(tilemap_dir / tileset['source'], 'r') as f:
                    tileset_data = json.load(f)
                tileset.update(tileset_data)
            
            image_path = tileset['image']
            image_name = pathlib.Path(image_path).stem

            spritesheet_surf = getattr(images, image_name)
            tilecount = tileset['tilecount']
            firstgid = tileset['firstgid']
            assert firstgid == len(self.tile_images)
            self.tile_images.extend(spritesheet(spritesheet_surf, self.tileheight, self.tilewidth, tilecount))


@dataclass
class CollisionTiles(Component):
    width: int
    height: int
    grid: list[int]

    def get(self, x: int, y: int) -> int:
        index = y * self.width + x
        if index >= len(self.grid):
            return 0
        return self.grid[index]
    
    @staticmethod
    def from_tilemap(json_data, layerid) -> 'CollisionTiles':
        return CollisionTiles(
            width=json_data['width'],
            height=json_data['height'],
            grid=json_data['layers'][layerid]['data']
        )


# TODO copy paste
@dataclass
class DecorativeTiles(Component):
    width: int
    height: int
    grid: list[int]

    def get(self, x: int, y: int) -> int:
        index = y * self.width + x
        if index >= len(self.grid):
            return 0
        return self.grid[index]
    
    @staticmethod
    def from_tilemap(json_data, layerid) -> 'DecorativeTiles':
        return DecorativeTiles(
            width=json_data['width'],
            height=json_data['height'],
            grid=json_data['layers'][layerid]['data']
        )

@dataclass
class World(Component):
    surf: pg.Surface = pg.Surface((2000.0, 2000.0), pg.SRCALPHA)
    clipping_rect: pg.Rect = pg.Rect(0, 0, screen_size[0], screen_size[1])
    offset: pg.math.Vector2 = pg.math.Vector2(0, 0)
