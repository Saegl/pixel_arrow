from dataclasses import dataclass
from flecs import Scene, System

from cutecats.components.position import Position
from cutecats.components.world import World
from cutecats.components.animation import Animation


@dataclass
class AnimationRenderer(System):
    def get_image(self, anim: Animation):
        anim_state = anim.states[anim.current_state]
        duration = anim_state.image_duration
        images = anim_state.images_left if anim.look_left else anim_state.images_right

        if anim_state.cyclic:
            cycle = anim.frames % (len(images) * duration)
            n = cycle // duration
            return images[n]
        else:
            n = anim.frames // duration
            n = min(n, len(images) - 1)
            return images[n]

    def process(self, _, scene: Scene):
        world: World = scene.get_component(World)
        for _, (pos, anim) in scene.get_entities(Position, Animation):
            anim.frames += 1
            image = self.get_image(anim)
            world.surf.blit(image, pos.v.xy)
