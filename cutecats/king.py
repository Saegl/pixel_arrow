from flecs.image_store import ImageStore, spritesheet, hflips
from cutecats.components.animation import AnimationState


KING_IDLE = 0


def load_king_animations(images: ImageStore) -> list[AnimationState]:
    king = spritesheet(images.king_meowthur, 160, 80, 12 * 1)
    idle = king[:6]

    return [
        AnimationState(hflips(idle), idle, cyclic=True),
    ]
