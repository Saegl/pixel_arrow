from dataclasses import dataclass
import pygame as pg
from flecs import Scene, Component, System
from flecs.framework import GameFramework
from square_mover.networking import NetworkingProcess
from square_mover.network_packets import GameState, PlayerAction

MOVE_SPEED = 3
SQUARE_SIZE = 25


@dataclass
class Pos(Component):
    "Position as a 2d Vector in a World"
    vec: pg.math.Vector2 = pg.math.Vector2()


class SendPlayerActions(System):
    def __init__(self, net: NetworkingProcess) -> None:
        self.net = net
    
    def capture_action(self, keys):
        return PlayerAction(
            up=keys[pg.K_UP],
            down=keys[pg.K_DOWN],
            left=keys[pg.K_LEFT],
            right=keys[pg.K_RIGHT],
        )
    
    def on_key_down(self, event: pg.event.Event):
        action = self.capture_action(pg.key.get_pressed())
        self.net.send_action(action)

    def on_key_up(self, event):
        action = self.capture_action(pg.key.get_pressed())
        self.net.send_action(action)


class ServerUpdates(System):
    def __init__(self, net: NetworkingProcess) -> None:
        self.net = net
    
    def process(self, dt, scene: "Scene"):
        player_pos = scene.get_component(Pos)
        for state in self.net.get_events():
            state: GameState
            player_pos.vec.x = state.x
            player_pos.vec.y = state.y


class PlayerMove(System):
    "Move player pos by listening network events"

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


class Online(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        game: GameFramework
        game.debug.show = True

        print("Starting networking process")
        self.net = NetworkingProcess()
        self.net.start()
        print("process started")

        # The Main Player
        self.create_enitity(Pos())

        self.add_system(SendPlayerActions(self.net))

        # self.add_system(PlayerMove())
        self.add_system(ServerUpdates(self.net))
        self.add_system(PlayerRender())
    
    def destroy(self):
        self.net.proc.kill() # FIXME proper exit?
        super().destroy()
