import pygame as pg

from flecs import Scene, GameFramework
from pixel_arrow.systems.arrow_movement import ArrowMovement
from pixel_arrow.systems.collision_utils import CollisionBoxUpdate
from pixel_arrow.systems.debug import CollisionsDebugRenderer
from pixel_arrow.systems.hud import HPRenderer

from pixel_arrow.components.world import Tiles, World
from pixel_arrow.components.position import Position
from pixel_arrow.components.animation import Animation
from pixel_arrow.components.character import (
    CharacterState,
    UserControlled,
    CharacterMovement,
    character_animations,
    create_player,
)
from pixel_arrow.components.collision import Collision

from pixel_arrow.systems.usercontrol import UserControl
from pixel_arrow.systems.worldrender import (
    CharacterCameraClipping,
    MapRenderer,
    WorldCameraRender,
    WorldCameraClear,
)
from pixel_arrow.systems.animation import AnimationRenderer
from pixel_arrow.systems.character_movement import UpdateCharacterMovement
from pixel_arrow.systems.gravity import Gravity
from pixel_arrow.systems.background import BackgroundRenderer


class SingleplayerScene(Scene):
    def __init__(self, game: GameFramework) -> None:
        super().__init__(game)

        images = game.res.images

        self.tiles = Tiles.from_file("map.txt")

        self.create_enitity(self.tiles, World())
        self.player = create_player(self, self.tiles)

        ### Game mechanics
        self.add_system(UserControl())
        self.add_system(Gravity())
        self.add_system(UpdateCharacterMovement())
        self.add_system(ArrowMovement())
        self.add_system(CollisionBoxUpdate())

        ### On screen render
        self.add_system(BackgroundRenderer(images.background))

        ### On World Render
        self.add_system(CharacterCameraClipping())
        self.add_system(WorldCameraClear())
        self.add_system(MapRenderer())
        self.add_system(AnimationRenderer())
        self.add_system(WorldCameraRender())

        ### HUD Render
        self.add_system(HPRenderer())

        ### Debug
        # self.add_system(CollisionsDebugRenderer())

    def on_keydown(self, event: pg.event.Event):
        if event.key == pg.K_ESCAPE:
            self.game.pop()
