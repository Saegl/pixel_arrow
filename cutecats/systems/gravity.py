from dataclasses import dataclass
from flecs import Scene, System

from cutecats.components.character import CharacterMovement
from cutecats.components.collision import Collision
from cutecats.systems.collision_utils import collide_y

# 0.2 default
FALLING_ACCELERATION = 0.3

@dataclass
class Gravity(System):
    def process(self, _, scene: Scene):
        for _, (cm, collision) in scene.get_entities(CharacterMovement, Collision):
            cm: CharacterMovement
            collision: Collision

            if not collide_y(collision, cm.momentum.y):
                cm.movement.y += cm.momentum.y
                cm.momentum.y += FALLING_ACCELERATION
            else:
                cm.momentum.y = 0.1
