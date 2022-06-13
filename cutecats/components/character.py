import pygame as pg
from dataclasses import dataclass
from flecs import Component


@dataclass
class UserControlled(Component):
    pass


@dataclass
class CharacterState(Component):
    hp: int = 5
    
    frames_since_attack: int = 0
    ready_for_second_attack: bool = False
    ready_for_third_attack: bool = False
    
    first_attack: bool = False
    second_attack: bool = False
    third_attack: bool = False

    dodge: bool = False
    dodge_cooldown: int = 1

    @property
    def attacking(self):
        return any(
            (self.first_attack, self.second_attack, self.third_attack)
        )


@dataclass
class CharacterMovement(Component):
    movement: pg.math.Vector2 = pg.math.Vector2(0.0, 0.0)
    momentum: pg.math.Vector2 = pg.math.Vector2(0.0, 0.0)
