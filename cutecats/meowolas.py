from flecs.image_store import ImageStore, spritesheet, hflips
from cutecats.components.animation import AnimationState


MEOWOLAS_IDLE = 0
MEOWOLAS_RUN = 1
MEOWOLAS_JUMP = 2
MEOWOLAS_ATTACK_1 = 3
MEOWOLAS_ATTACK_2 = 4
MEOWOLAS_ATTACK_3 = 5
MEOWOLAS_ATTACK_4 = 6
MEOWOLAS_ATTACK_4_CYCLE = 7
MEOWOLAS_DODGE = 8
MEOWOLAS_TAKE_DAMAGE = 9
MEOWOLAS_DEATH = 10


def load_meowolas_animations(images: ImageStore) -> list[AnimationState]:
    meowolas = spritesheet(images.meowolas, 80, 80, 12 * 13)
    idle = meowolas[:6]
    run = meowolas[12 * 1:12 * 1 + 8]
    jump = meowolas[12 * 2:12 * 2 + 12]
    attack_1 = meowolas[12 * 3:12 * 3 + 5]
    attack_2 = meowolas[12 * 4:12 * 4 + 8]
    attack_3 = meowolas[12 * 7:12 * 7 + 8]
    attack_4 = meowolas[12 * 9:12 * 9 + 11]
    attack_4_cycle = meowolas[12 * 8:12 * 8 + 3]
    dodge = meowolas[12 * 10:12 * 10 + 9]
    take_damage = meowolas[12 * 11:12 * 11 + 3]
    death = meowolas[12 * 12:12 * 12 + 6]

    return [
        AnimationState(hflips(idle), idle, cyclic=True),
        AnimationState(hflips(run), run, cyclic=True, image_duration=8),
        AnimationState(hflips(jump), jump, cyclic=False),
        AnimationState(hflips(attack_1), attack_1, cyclic=False, image_duration=6),
        AnimationState(hflips(attack_2), attack_2, cyclic=False, image_duration=6),
        AnimationState(hflips(attack_3), attack_3, cyclic=False, image_duration=6),
        AnimationState(hflips(attack_4), attack_4, cyclic=False, image_duration=6),
        AnimationState(hflips(attack_4_cycle), attack_4_cycle, cyclic=True, image_duration=6),
        AnimationState(hflips(dodge), dodge, cyclic=False, image_duration=4),
        AnimationState(hflips(take_damage), take_damage, cyclic=False),
        AnimationState(hflips(death), death, cyclic=False),
    ]