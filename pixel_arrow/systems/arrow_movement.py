import pygame as pg
from flecs import Scene, System
from pixel_arrow.components.animation import Animation
from pixel_arrow.components.character import CharacterState
from pixel_arrow.components.collision import Collision
from pixel_arrow.components.arrow import Arrow
from pixel_arrow.components.position import Position

from pixel_arrow.systems.collision_utils import collide_x


class ArrowState:
    fly = 0
    stuck = 1
    dissapear = 2


ARROW_SPEED = 15.0
ARROW_FRAMES_TO_STUCK = 360


class ArrowMovement(System):
    def process(self, dt, scene: Scene):
        for arrow_id, (arrow, pos, anim, arrow_coll) in scene.get_entities(
            Arrow, Position, Animation, Collision
        ):
            arrow: Arrow
            pos: Position
            anim: Animation
            arrow_coll: Collision

            if anim.current_state == ArrowState.fly:
                dx = -ARROW_SPEED if anim.look_left else ARROW_SPEED
                pos.v.x += dx

                if collide_x(arrow_coll, dx):
                    anim.current_state = ArrowState.stuck
            elif anim.current_state == ArrowState.stuck:
                arrow.frames_since_stuck += 1

                if arrow.frames_since_stuck > ARROW_FRAMES_TO_STUCK:
                    scene.remove_entity(arrow_id)

            # Arrow within a world
            world_rect = pg.Rect(0, 0, 2000.0, 2000.0)
            if not arrow_coll.box.colliderect(world_rect):
                scene.remove_entity(arrow_id)

            if anim.current_state != ArrowState.stuck:
                for _, (cstate, player_coll) in scene.get_entities(
                    CharacterState, Collision
                ):
                    cstate: CharacterState
                    player_coll: Collision

                    if player_coll.box.colliderect(arrow_coll.box):
                        cstate.hp -= 1
                        scene.remove_entity(arrow_id)
