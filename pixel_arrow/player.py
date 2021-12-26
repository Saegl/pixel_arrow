from collections import defaultdict
from dataclasses import dataclass

import pygame
from pygame import Surface
from pygame.locals import *

from pixel_arrow.image_store import ImageStore
from pixel_arrow.vector import Vector2D
from pixel_arrow.gamemap import Map, cell_to_rect
from pixel_arrow.mixins import DrawMixin, UpdateMixin
from pixel_arrow.arrows import Arrow, ArrowState
from pixel_arrow.collisions import collide_with


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
    def from_pressed(pressed: defaultdict[int, bool]) -> 'PlayerKeys':
        pk = PlayerKeys()
        if pressed[K_a]: pk.attacking = True
        if pressed[K_RIGHT]: pk.moving_right = True
        if pressed[K_LEFT]: pk.moving_left = True
        if pressed[K_DOWN]: pk.moving_down = True
        if pressed[K_UP]: pk.moving_up = True
        return pk
    
    @staticmethod
    def from_list(arr: list[bool]) -> 'PlayerKeys':
        pk = PlayerKeys()
        if arr[0]: pk.attacking = True
        if arr[1]: pk.moving_right = True
        if arr[2]: pk.moving_left = True
        if arr[3]: pk.moving_down = True
        if arr[4]: pk.moving_up = True
        return pk

    def as_list(self) -> list[bool]:
        arr = [False] * 5
        if self.attacking: arr[0] = True
        if self.moving_right: arr[1] = True
        if self.moving_left: arr[2] = True
        if self.moving_down: arr[3] = True
        if self.moving_up: arr[4] = True
        return arr

class Player(DrawMixin, UpdateMixin):
    def __init__(
        self,
        location: Vector2D,
        show_hp: bool,
        image_store: ImageStore,
        screen: Surface,
        game,
    ) -> None:
        self.setup_draw(image_store, screen)
        self.setup_update(game)

        self.arrow_fired = False
        self.attacking = False
        self.look_left = False

        self.hp = 5
        self.show_hp = show_hp

        self.tile_size = 48
        self._state = PlayerState.idle
        self.frames = 0

        self.location = location
        self.y_momentum = 0
        self.acceleration = Vector2D(0.0, 0.0)
        self.visible = True

        self.width = 72
        self.height = 72

    def draw(self):
        screen: Surface = self.screen
        if self.visible:
            screen.blit(self.image, self.location.xy, (0, 0, 72, 72))

        if self.show_hp:
            offset = 33
            for i in range(self.hp):
                screen.blit(self.image_store.heart, (33.0 + offset * i, 10.0))

    # TODO Liskov substitution violation
    def update(self, keys: PlayerKeys):
        self.frames += 1
        if keys.attacking:
            self.attacking = True

        ## Movement by arrow keys
        player_movement = Vector2D(0.0, 0.0)
        if keys.moving_right:
            player_movement.x += 5
        if keys.moving_left:
            player_movement.x -= 5
        if keys.moving_up and self.on_ground():  # Jump
            self.y_momentum -= 7.5

        ## Collisions
        if not self.collide_y(self.y_momentum):
            self.location.y += self.y_momentum
            self.y_momentum += 0.2
        else:
            self.y_momentum = 0.1

        if not self.collide_x(player_movement.x):
            self.location.x += player_movement.x

        if not self.collide_y(player_movement.y):
            self.location.y += player_movement.y

        ## Player State
        if self.attacking:
            self.state = PlayerState.attack
        elif self.on_ground():
            if not self.moving(keys):
                self.state = PlayerState.idle
            else:
                self.state = PlayerState.run
        else:  # In air
            self.state = PlayerState.jump

        ## Side to look
        if keys.moving_right:
            self.look_left = False
        elif keys.moving_left:
            self.look_left = True

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: PlayerState):
        if self._state != value:
            self._state = value
            self.frames = 0

    def get_damage(self, damage: int):
        self.hp -= damage
        self.y_momentum -= 3.5
        if self.hp < 0:
            self.visible = False

    def is_cycle_animation(self):
        return self.state not in (PlayerState.jump, PlayerState.attack)

    @property
    def image(self):
        duration = 10  # Change image every 10 frames
        images = self.image_store.animations[self.state][not self.look_left]
        self.game.info_text = str(self.state)
        if self.is_cycle_animation():
            cycle = self.frames % (len(images) * duration)
            n = cycle // duration
            return images[n]
        else:
            n = self.frames // duration
            if self.state == PlayerState.attack and n == 3 and not self.arrow_fired:
                self.launch_an_arrow()
                self.arrow_fired = True

            if n >= len(images):
                if self.state == PlayerState.attack:
                    self.attacking = False
                    self.arrow_fired = False
                return images[-1]
            return images[n]

    @property
    def rect(self):
        return pygame.Rect(
            self.location.x,
            self.location.y,
            self.width,
            self.height,
        )

    @property
    def grid_loc(self):
        rect = self.rect
        return self.game.map.grid_loc(Vector2D(rect.centerx, rect.centery))

    def collide(self) -> bool:
        map_ = self.game.map
        loc = self.grid_loc
        tiles_loc = [
            Vector2D(loc.x + 1, loc.y + 1),  # bottom right
            Vector2D(loc.x + 0, loc.y + 1),  # bottom
            Vector2D(loc.x - 1, loc.y + 1),  # bottom left
            Vector2D(loc.x + 1, loc.y - 1),  # top right
            Vector2D(loc.x + 0, loc.y - 1),  # top
            Vector2D(loc.x - 1, loc.y - 1),  # top left
            Vector2D(loc.x + 1, loc.y),  # right
            Vector2D(loc.x - 1, loc.y),  # left
        ]
        collisions = filter(lambda loc: map_.cells[loc.x][loc.y] != "0", tiles_loc)
        collisions = map(
            lambda loc: cell_to_rect(loc.x, loc.y, self.tile_size), collisions
        )

        return collide_with(self.rect, list(collisions))

    def collide_y(self, dy) -> bool:
        self.location.y += dy
        ans = self.collide()
        self.location.y -= dy
        return ans

    def collide_x(self, dx) -> bool:
        self.location.x += dx
        ans = self.collide()
        self.location.x -= dx
        return ans

    def on_ground(self) -> bool:
        return self.collide_y(0.1)

    def moving(self, keys: PlayerKeys) -> bool:
        return any(
            [keys.moving_right, keys.moving_left, keys.moving_up, keys.moving_down]
        )

    def launch_an_arrow(self):
        rect = self.rect

        if self.look_left:
            x = rect.left - 36
        else:
            x = rect.right

        pos = Vector2D(x, rect.centery)
        arrow = Arrow(pos, self.look_left, ArrowState.fly)
        self.game.arrows.launch_an_arrow(arrow)
