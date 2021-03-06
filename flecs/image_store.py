from pathlib import Path

import pygame as pg

from flecs.config import Config


def hflip(image: pg.Surface) -> pg.Surface:
    return pg.transform.flip(image, True, False)


def hflips(images: list[pg.Surface]) -> list[pg.Surface]:
    return list(map(hflip, images))


def fast_load(filename) -> pg.Surface:
    return pg.image.load(filename).convert()


def fast_load_alpha(filename) -> pg.Surface:
    return pg.image.load(filename).convert_alpha()


def prop_scale(source: pg.Surface, target: pg.Surface):
    x1, y1 = source.get_size()
    x2, y2 = target.get_size()
    k = max(x2 / x1, y2 / y1)
    newsize = (x1 * k, y1 * k)
    return pg.transform.scale(source, newsize)


def scale_nx(image: pg.Surface, n: int):
    x, y = image.get_size()
    return pg.transform.scale(image, (n * x, n * y))


def spritesheet(image: pg.Surface, tile_width: int, tile_height, count: int):
    # TODO: tile height and width
    width, height = image.get_size()

    sprites = []
    for y in range(height // tile_height):
        for x in range(width // tile_width):
            sprites.append(
                image.subsurface(
                    pg.Rect(x * tile_width, y * tile_height, tile_width, tile_height)
                )
            )
    sprites = sprites[:count]
    return sprites


class ImageStore:
    def __getattr__(self, name: str) -> pg.Surface:
        return self.__dict__[name]

    def __setattr__(self, name: str, value: pg.Surface) -> None:
        self.__dict__[name] = value

    @staticmethod
    def load_images(config: Config) -> "ImageStore":
        store = ImageStore()
        for file in Path(config.images_folder).rglob("*.png"):
            setattr(store, file.stem, fast_load_alpha(str(file)))
        return store
