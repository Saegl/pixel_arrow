from flecs import Scene, System
from pixel_arrow.components.position import Position
from pixel_arrow.components.character import CharacterMovement
from pixel_arrow.components.collision import Collision

from pixel_arrow.systems.collision_utils import collide_y, collide_x


class UpdateCharacterMovement(System):
    def process(self, _, scene: Scene):
        for _, (pos, cm, collision) in scene.get_entities(
            Position, CharacterMovement, Collision
        ):
            pos: Position
            cm: CharacterMovement

            if not collide_x(collision, cm.movement.x):
                pos.v.x += cm.movement.x

            if not collide_y(collision, cm.movement.y):
                pos.v.y += cm.movement.y

            cm.movement.x = 0
            cm.movement.y = 0
