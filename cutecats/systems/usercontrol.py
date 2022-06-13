from collections import defaultdict
from dataclasses import dataclass

import pygame as pg
from flecs import System, Scene

from cutecats.components.character import (
    CharacterState,
    UserControlled,
    CharacterMovement,
)

from cutecats.components.animation import Animation
from cutecats.components.collision import Collision
from cutecats.systems.collision_utils import on_ground

from cutecats.meow_knight import *


CHARACTER_SPEED = 2.0
CHARACTER_JUMP_MOMENTUM = 6


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
    dodging: bool = False

    @staticmethod
    def from_pressed(pressed: defaultdict[int, bool]) -> "PlayerKeys":
        return PlayerKeys(
            attacking=pressed[pg.K_a],
            moving_right=pressed[pg.K_RIGHT],
            moving_left=pressed[pg.K_LEFT],
            moving_down=pressed[pg.K_DOWN],
            moving_up=pressed[pg.K_UP],
            dodging=pressed[pg.K_d]
        )

    @staticmethod
    def from_list(arr: list[bool]) -> "PlayerKeys":
        return PlayerKeys(
            attacking=arr[0],
            moving_right=arr[1],
            moving_left=arr[2],
            moving_down=arr[3],
            moving_up=arr[4],
            dodging=arr[5],
        )

    def as_list(self) -> list[bool]:
        return [
            self.attacking,
            self.moving_right,
            self.moving_left,
            self.moving_down,
            self.moving_up,
            self.dodging
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
            cstate: CharacterState
            keys = PlayerKeys.from_pressed(scene.game.pressed_keys)
            collision: Collision
            anim: Animation

            attack1_anim = anim.states[MEOW_KNIGHT_ATTACK_1]
            attack2_anim = anim.states[MEOW_KNIGHT_ATTACK_2]
            attack3_anim = anim.states[MEOW_KNIGHT_ATTACK_3]

            dodge_anim = anim.states[MEOW_KNIGHT_DODGE]

            if not keys.moving(): # can start attack only when not moving
                # Start attack
                if not cstate.first_attack and keys.attacking and on_ground(collision):
                    print('Attack 1 started')
                    cstate.first_attack = True
                
                # Key down for double attack
                elif cstate.first_attack and not keys.attacking:
                    cstate.ready_for_second_attack = True
                
                # Double attack
                elif cstate.first_attack and keys.attacking and cstate.ready_for_second_attack and not cstate.second_attack:
                    print("DOUBLE ATTACK Started")
                    cstate.ready_for_second_attack = False
                    cstate.second_attack = True
                
                # Key down for triple attack
                if cstate.second_attack and not keys.attacking:
                    cstate.ready_for_third_attack = True

                elif cstate.second_attack and keys.attacking and cstate.ready_for_third_attack and not cstate.third_attack:
                    print("Triple attack Started")
                    cstate.ready_for_third_attack = False
                    cstate.third_attack = True
            
            if not cstate.dodge_cooldown:
                cstate.dodge_cooldown += 1

            if keys.dodging and not keys.moving() and not cstate.attacking and not cstate.dodge and cstate.dodge_cooldown:
                print("DODGE start")
                cstate.dodge = True
                cstate.dodge_cooldown = - dodge_anim.duration * 2

            if cstate.first_attack:
                cstate.frames_since_attack += 1

            # Gravity momeuntum
            if keys.moving_up and on_ground(collision):
                cmove.momentum.y -= CHARACTER_JUMP_MOMENTUM

            # Left/right movement
            if keys.moving_left and not cstate.first_attack:
                cmove.movement.x -= CHARACTER_SPEED
                anim.look_left = True
            if keys.moving_right and not cstate.first_attack:
                cmove.movement.x += CHARACTER_SPEED
                anim.look_left = False
            
                
            if cstate.second_attack and cstate.frames_since_attack == attack1_anim.duration:
                ## Double attack slide
                cmove.movement.x += 10 * ((-1) if anim.look_left else 1)
            
            if cstate.third_attack and cstate.frames_since_attack == attack1_anim.duration + attack2_anim.duration:
                ## Triple attack slide
                cmove.movement.x += 10 * ((-1) if anim.look_left else 1)
            
            if cstate.dodge:
                ## Dodge slide
                cmove.movement.x += 1.5 * ((-1) if anim.look_left else 1)

            ## Animation State
            new_state = anim.current_state
            if cstate.first_attack:
                if cstate.third_attack and cstate.frames_since_attack >= attack1_anim.duration + attack2_anim.duration:
                    new_state = MEOW_KNIGHT_ATTACK_3
                elif cstate.second_attack and cstate.frames_since_attack >= attack1_anim.duration:
                    new_state = MEOW_KNIGHT_ATTACK_2
                else:
                    new_state = MEOW_KNIGHT_ATTACK_1
            elif on_ground(collision):
                if not keys.moving():
                    new_state = MEOW_KNIGHT_IDLE
                else:
                    new_state = MEOW_KNIGHT_RUN
            else:  # In air
                new_state = MEOW_KNIGHT_JUMP
            if cstate.dodge:
                new_state = MEOW_KNIGHT_DODGE

            if new_state != anim.current_state:
                anim.current_state = new_state
                anim.frames = 0  # If state changed, reset animation frame counter

            # Attack
            # safe_offest = 5.0
            # if cstate.attacking and cstate.frames_since_attack == 40:
            #     rect = collision.box

            #     if anim.look_left:
            #         x = rect.left - 36 - safe_offest
            #     else:
            #         x = rect.right + safe_offest

            #     pos = pg.math.Vector2(x, rect.centery)
                # launch_arrow(scene, pos, anim.look_left)

            
            if not cstate.second_attack and cstate.first_attack and cstate.frames_since_attack == attack1_anim.duration:
                ## Attack1 ended
                cstate.first_attack = False
                cstate.ready_for_second_attack = False
                cstate.ready_for_third_attack = False
                cstate.frames_since_attack = 0
                cstate.third_attack = False
                print("Attack 1 ended")
            elif not cstate.third_attack and cstate.second_attack and cstate.first_attack and cstate.frames_since_attack == attack1_anim.duration + attack2_anim.duration:
                cstate.first_attack = False
                cstate.ready_for_second_attack = False
                cstate.ready_for_third_attack = False
                cstate.frames_since_attack = 0
                cstate.second_attack = False
                print("DOUBLE ATTACK ENDED")
            elif cstate.third_attack and cstate.frames_since_attack == attack1_anim.duration + attack2_anim.duration + attack3_anim.duration:
                cstate.first_attack = False
                cstate.ready_for_second_attack = False
                cstate.ready_for_third_attack = False
                cstate.frames_since_attack = 0
                cstate.second_attack = False
                cstate.third_attack = False
                print("THIRD ATTACK ENDED")
            
            if cstate.dodge and anim.frames >= dodge_anim.duration:
                cstate.dodge = False
                print("DODGE END")
