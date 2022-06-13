from flecs.image_store import ImageStore, spritesheet, hflips
from cutecats.components.animation import AnimationState


MEOW_KNIGHT_RUN = 0
MEOW_KNIGHT_IDLE = 1
MEOW_KNIGHT_JUMP = 2
MEOW_KNIGHT_ATTACK_1 = 3
MEOW_KNIGHT_DODGE = 4
MEOW_KNIGHT_ATTACK_2 = 5
MEOW_KNIGHT_ATTACK_3 = 6
MEOW_KNIGHT_ATTACK_4 = 7
MEOW_KNIGHT_TAKE_DAMAGE = 8
MEOW_KNIGHT_DEATH = 9


def load_meow_knight_animations(images: ImageStore) -> list[AnimationState]:
    meow_knight = spritesheet(images.meow_knight, 80, 80, 12 * 10)
    run = meow_knight[:8]
    idle = meow_knight[12 * 1:12 * 1 + 6]
    jump = meow_knight[12 * 2:12 * 2 + 12]
    attack_1 = meow_knight[12 * 3:12 * 3 + 10]
    dodge = meow_knight[12 * 4:12 * 4 + 8]
    attack_2 = meow_knight[12 * 5:12 * 5 + 4]
    attack_3 = meow_knight[12 * 6:12 * 6 + 4]
    attack_4 = meow_knight[12 * 7:12 * 7 + 8]
    take_damage = meow_knight[12 * 8:12 * 8 + 3]
    death = meow_knight[12 * 9:12 * 9 + 6]

    return [
        AnimationState(hflips(run), run, cyclic=True, image_duration=8),
        AnimationState(hflips(idle), idle, cyclic=True),
        AnimationState(hflips(jump), jump, cyclic=False),
        AnimationState(hflips(attack_1), attack_1, cyclic=False, image_duration=6),
        AnimationState(hflips(dodge), dodge, cyclic=False, image_duration=4),
        AnimationState(hflips(attack_2), attack_2, cyclic=False),
        AnimationState(hflips(attack_3), attack_3, cyclic=False),
        AnimationState(hflips(attack_4), attack_4, cyclic=False),
        AnimationState(hflips(take_damage), take_damage, cyclic=False),
        AnimationState(hflips(death), death, cyclic=False),
    ]