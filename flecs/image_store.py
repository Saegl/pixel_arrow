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


def load_animation(imagename, tile_size, count):
    image = fast_load_alpha(imagename)
    image = scale_nx(image, 3)

    m, n = image.get_size()

    images_right = []
    for x in range(m // tile_size):
        for y in range(n // tile_size):
            images_right.append(
                image.subsurface(
                    pg.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                )
            )
    images_right = images_right[:count]
    images_left = hflips(images_right)
    return [images_left, images_right]


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
