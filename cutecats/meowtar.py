from flecs.image_store import ImageStore, spritesheet, hflips
from cutecats.components.animation import AnimationState


MEOWTAR_IDLE = 0


def load_meowtar_animations(images: ImageStore) -> list[AnimationState]:
    meowtar = spritesheet(images.meowtar_the_blue, 160, 80, 12 * 1)
    idle = meowtar[:6]

    return [
        AnimationState(hflips(idle), idle, cyclic=True),
    ]
