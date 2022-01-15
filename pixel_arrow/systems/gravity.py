from dataclasses import dataclass
from flecs import Scene, System
from pixel_arrow.components.character import CharacterMovement
from pixel_arrow.components.collision import Collision

from pixel_arrow.systems.collision_utils import collide_y


@dataclass
class Gravity(System):
    def process(self, _, scene: Scene):
        for _, (cm, collision) in scene.get_entities(CharacterMovement, Collision):
            cm: CharacterMovement
            collision: Collision

            if not collide_y(collision, cm.momentum.y):
                cm.movement.y += cm.momentum.y
                cm.momentum.y += 0.2
            else:
                cm.momentum.y = 0.1
