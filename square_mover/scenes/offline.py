from dataclasses import dataclass
import pygame as pg
from flecs import Scene, Component, System


MOVE_SPEED = 5
SQUARE_SIZE = 10


@dataclass
class Pos(Component):
    "Position as a 2d Vector in a World"
    vec: pg.math.Vector2 = pg.math.Vector2()


class PlayerMove(System):
    "Move player pos by listening keyboard arrow keys"

    def process(self, dt, scene: "Scene"):
        keys = scene.game.pressed_keys
        dx = 0
        dy = 0
        if keys[pg.K_UP]:
            dy -= MOVE_SPEED
        if keys[pg.K_DOWN]:
            dy += MOVE_SPEED
        if keys[pg.K_LEFT]:
            dx -= MOVE_SPEED
        if keys[pg.K_RIGHT]:
            dx += MOVE_SPEED

        player_pos = scene.get_component(Pos)
        player_pos.vec.x += dx
        player_pos.vec.y += dy


class PlayerRender(System):
    "Render main player on game screen according to his position"

    def process(self, dt, scene: "Scene"):
        scene.game.screen.fill(pg.Color("black"))
        for _, (pos,) in scene.get_entities(Pos):
            pg.draw.rect(
                scene.game.screen,
                pg.Color("green"),
                (pos.vec.x, pos.vec.y, SQUARE_SIZE, SQUARE_SIZE),
            )


class Offline(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

        # The Main Player
        self.create_enitity(Pos())

        self.add_system(PlayerMove())
        self.add_system(PlayerRender())
