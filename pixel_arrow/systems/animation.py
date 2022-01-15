from dataclasses import dataclass
from flecs import Scene, System

from pixel_arrow.components.position import Position
from pixel_arrow.components.world import World
from pixel_arrow.components.animation import Animation


@dataclass
class AnimationRenderer(System):
    def get_image(self, anim: Animation):
        duration = 10  # Change image every 10 frames
        anim_state = anim.states[anim.current_state]
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
