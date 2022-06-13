from dataclasses import dataclass
from flecs import Scene, System
from cutecats.components.character import CharacterState, UserControlled


@dataclass
class HPRenderer(System):
    def process(self, _, scene: Scene):
        screen = scene.game.screen
        images = scene.game.res.images
        offset_between = 10.0
        offset_x = 5.0
        offset_y = 5.0
        for _, (_, cstate) in scene.get_entities(UserControlled, CharacterState):
            for i in range(cstate.hp):
                screen.blit(images.heart, (offset_x + offset_between * i, offset_y))