import pygame as pg

from flecs import Scene, GameFramework
from pixel_arrow.systems.arrow_movement import ArrowMovement
from pixel_arrow.systems.collision_utils import CollisionBoxUpdate
from pixel_arrow.systems.debug import CollisionsDebugRenderer
from pixel_arrow.systems.hud import HPRenderer, TilesetRenderer

from pixel_arrow.components.world import Tiles, World
from pixel_arrow.components.position import Position
from pixel_arrow.components.animation import Animation
from pixel_arrow.components.character import (
    CharacterState,
    UserControlled,
    CharacterMovement,
    character_animations,
)
from pixel_arrow.components.collision import Collision

from pixel_arrow.systems.usercontrol import UserControl
from pixel_arrow.systems.worldrender import (
    CharacterCameraClipping,
    MapRenderer,
    MouseCameraClipping,
    WorldCameraRender,
    WorldCameraClear,
)
from pixel_arrow.systems.animation import AnimationRenderer
from pixel_arrow.systems.character_movement import UpdateCharacterMovement
from pixel_arrow.systems.gravity import Gravity
from pixel_arrow.systems.background import BackgroundRenderer


class LevelEditorScene(Scene):
    def __init__(self, game: GameFramework) -> None:
        super().__init__(game)

        images = game.res.images

        self.tiles = Tiles.from_file("map.txt")

        self.create_enitity(self.tiles, World())

        col_x_offset = 10.0
        col_y_offset = 10.0
        self.player = self.create_enitity(
            Position(pg.math.Vector2(50.0, 500.0)),
            CharacterState(),
            CharacterMovement(),
            UserControlled(),
            Animation(character_animations),
            Collision(
                pg.Rect(0.0, 0.0, 72.0 - col_x_offset * 2, 72.0 - col_y_offset),
                self.tiles.grid,
                offset=pg.math.Vector2(col_x_offset, col_y_offset),
            ),
        )

        ### Game mechanics
        # self.add_system(UserControl())
        # self.add_system(Gravity())
        # self.add_system(UpdateCharacterMovement())
        # self.add_system(ArrowMovement())
        # self.add_system(CollisionBoxUpdate())

        ### On screen render
        self.add_system(BackgroundRenderer(images.background))

        ### On World Render
        self.add_system(MouseCameraClipping())
        self.add_system(WorldCameraClear())
        self.add_system(MapRenderer())
        self.add_system(AnimationRenderer())
        self.add_system(WorldCameraRender())

        ### HUD Render
        # self.add_system(HPRenderer())
        self.add_system(TilesetRenderer())

        ### Debug
        # self.add_system(CollisionsDebugRenderer())

    def on_keydown(self, event: pg.event.Event):
        if event.key == pg.K_ESCAPE:
            self.game.pop()
