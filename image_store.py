import pygame
from pygame import Rect, Surface


def hflip(image: Surface) -> Surface:
    return pygame.transform.flip(image, True, False)


def hflips(images: list[Surface]) -> list[Surface]:
    return list(map(hflip, images))


def fast_load(filename) -> Surface:
    return pygame.image.load(filename).convert()


def fast_load_alpha(filename) -> Surface:
    return pygame.image.load(filename).convert_alpha()


def prop_scale(source: Surface, target: Surface):
    x1, y1 = source.get_size()
    x2, y2 = target.get_size()
    k = max(x2 / x1, y2 / y1)
    newsize = (x1 * k, y1 * k)
    return pygame.transform.scale(source, newsize)


def scale_nx(image: Surface, n: int):
    x, y = image.get_size()
    return pygame.transform.scale(image, (n * x, n * y))


def load_animation(imagename, tile_size, count):
    image = fast_load_alpha(imagename)
    image = scale_nx(image, 3)

    m, n = image.get_size()

    images_right = []
    for x in range(m // tile_size):
        for y in range(n // tile_size):
            images_right.append(
                image.subsurface(
                    Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                )
            )
    images_right = images_right[:count]
    images_left = hflips(images_right)
    return [images_left, images_right]


class ImageStore:
    def __getattr__(self, name: str):
        return self.__dict__[name]

    def __setattr__(self, name: str, value) -> None:
        self.__dict__[name] = value

    @staticmethod
    def load_images(screen_size):
        background_image = fast_load("Main/Backgrounds/merged-full-background.png")
        background_image = pygame.transform.scale(background_image, screen_size)

        arrow_image = fast_load_alpha("Main\Objects\Obj-Arrow-Idle-12x12.png")
        arrow_image = scale_nx(arrow_image, 3)

        heart = fast_load_alpha("Main/UI/UI-Lives.png")
        heart = scale_nx(heart, 3)

        store = ImageStore()
        store.background = background_image

        store.animations = [
            load_animation("Main/Player/Player-Idle-24x24.png", 72, 3),
            load_animation("Main/Player/Player-Run-24x24.png", 72, 8),
            load_animation("Main/Player/Player-Jump-24x24.png", 72, 4),
            load_animation("Main/Player/Player-Attack-24x24.png", 72, 5),
        ]

        keys = "0123456789abcdefghijklmnopqrstuvwxyz"
        store.tiles = {}
        for i in range(1, len(keys)):
            tile_image = fast_load_alpha(f"Main/Tiles/Tile-{str(i).zfill(2)}.png")
            tile_image = scale_nx(tile_image, 2)
            store.tiles[keys[i]] = tile_image

        store.arrow = arrow_image.subsurface(Rect(0, 0, 36, 36))
        store.arrow_left = hflip(store.arrow)

        store.arrow_stuck = load_animation(
            "Main\Objects\Obj-Arrow-Stuck-12x12.png", 36, 9
        )

        store.heart = heart

        return store
