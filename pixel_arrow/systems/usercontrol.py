from collections import defaultdict
from dataclasses import dataclass

import pygame as pg
from flecs import System, Scene

from pixel_arrow.components.character import (
    CharacterState,
    UserControlled,
    CharacterMovement,
)
from pixel_arrow.components.animation import Animation
from pixel_arrow.components.collision import Collision
from pixel_arrow.components.arrow import launch_arrow

from pixel_arrow.systems.collision_utils import on_ground


CHARACTER_SPEED = 7.0


class PlayerState:
    idle = 0
    run = 1
    jump = 2
    attack = 3


@dataclass
class PlayerKeys:
    attacking: bool = False
    moving_right: bool = False
    moving_left: bool = False
    moving_down: bool = False
    moving_up: bool = False

    @staticmethod
    def from_pressed(pressed: defaultdict[int, bool]) -> "PlayerKeys":
        return PlayerKeys(
            attacking=pressed[pg.K_a],
            moving_right=pressed[pg.K_RIGHT],
            moving_left=pressed[pg.K_LEFT],
            moving_down=pressed[pg.K_DOWN],
            moving_up=pressed[pg.K_UP],
        )

    @staticmethod
    def from_list(arr: list[bool]) -> "PlayerKeys":
        return PlayerKeys(
            attacking=arr[0],
            moving_right=arr[1],
            moving_left=arr[2],
            moving_down=arr[3],
            moving_up=arr[4],
        )

    def as_list(self) -> list[bool]:
        return [
            self.attacking,
            self.moving_right,
            self.moving_left,
            self.moving_down,
            self.moving_up,
        ]

    def moving(self) -> bool:
        return any(
            [self.moving_right, self.moving_left, self.moving_up, self.moving_down]
        )


@dataclass
class UserControl(System):
    def process(self, _, scene: Scene):
        for _, (_, cstate, cmove, collision, anim) in scene.get_entities(
            UserControlled, CharacterState, CharacterMovement, Collision, Animation
        ):
            keys = PlayerKeys.from_pressed(scene.game.pressed_keys)
            collision: Collision
            anim: Animation

            if keys.attacking:
                cstate.attacking = True

            if cstate.attacking:
                cstate.frames_since_attack += 1

            # Gravity momeuntum
            if keys.moving_up and on_ground(collision):
                cmove.momentum.y -= 7.5

            # Left/right movement
            if keys.moving_left:
                cmove.movement.x -= CHARACTER_SPEED
                anim.look_left = True
            if keys.moving_right:
                cmove.movement.x += CHARACTER_SPEED
                anim.look_left = False

            ## Animation State
            new_state = anim.current_state
            if cstate.attacking:
                new_state = PlayerState.attack
            elif on_ground(collision):
                if not keys.moving():
                    new_state = PlayerState.idle
                else:
                    new_state = PlayerState.run
            else:  # In air
                new_state = PlayerState.jump

            if new_state != anim.current_state:
                anim.current_state = new_state
                anim.frames = 0  # If state changed, reset animation frame counter

            # Attack
            safe_offest = 5.0
            if cstate.attacking and cstate.frames_since_attack == 30:
                rect = collision.box

                if anim.look_left:
                    x = rect.left - 36 - safe_offest
                else:
                    x = rect.right + safe_offest

                pos = pg.math.Vector2(x, rect.centery)
                launch_arrow(scene, pos, anim.look_left)

            if cstate.attacking and cstate.frames_since_attack == 50:
                cstate.attacking = False
                cstate.frames_since_attack = 0
