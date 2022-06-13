import json
import pygame as pg
from flecs import Scene, GameFramework, System

from cutecats.meow_knight import load_meow_knight_animations

from cutecats.components.world import DecorativeTiles, World, CollisionTiles
from cutecats.components.position import Position
from cutecats.components.animation import Animation
from cutecats.components.collision import Collision
from cutecats.components.character import CharacterMovement, CharacterState, UserControlled

from cutecats.systems.worldrender import TileSets, WorldCameraClear, WorldCameraRender, MapRenderer
from cutecats.systems.animations_render import AnimationRenderer
from cutecats.systems.usercontrol import UserControl
from cutecats.systems.scenes_utils import FallBackToFramework
from cutecats.systems.character_movement import UpdateCharacterMovement
from cutecats.systems.gravity import Gravity
from cutecats.systems.collision_utils import CollisionBoxUpdate
from cutecats.systems.background import BackgroundRenderer
from cutecats.systems.hud import HPRenderer


class BlackBackground(System):
    def process(self, dt, scene: "Scene"):
        scene.game.screen.fill((0, 0, 0))


class FightScene(Scene):
    def __init__(self, game: "GameFramework") -> None:
        super().__init__(game, "FightScene")
        images = game.res.images

        meow_knight_animations = load_meow_knight_animations(images)

        with open('cutecats/res/tilemaps/map1.json') as f:
            json_data = json.load(f)

        self.tiles = CollisionTiles.from_tilemap(json_data, 0)
        self.create_enitity(DecorativeTiles.from_tilemap(json_data, 1))
        self.create_enitity(DecorativeTiles.from_tilemap(json_data, 2))
        
        self.create_enitity(TileSets(json_data['tilesets'], self.game.res.images))
        
        
        self.world = self.create_enitity(World(), self.tiles)
        self.player = self.create_enitity(
            Position(pg.math.Vector2(0, 0)),
            Animation(meow_knight_animations),
            Collision(pg.Rect(0, 0, 16, 16), self.tiles, offset=pg.math.Vector2(32, 32 + 16)),
            CharacterMovement(),
            CharacterState(),
            UserControlled()
        )

        ### Game mechanics
        self.add_system(UserControl())
        self.add_system(Gravity())
        self.add_system(UpdateCharacterMovement())
        self.add_system(CollisionBoxUpdate())

        ### On screen render
        self.add_system(BackgroundRenderer(images.bg1))
        # self.add_system(BlackBackground())

        ### On World Render
        self.add_system(WorldCameraClear())
        self.add_system(MapRenderer(16))
        self.add_system(AnimationRenderer())
        self.add_system(WorldCameraRender())

        ### HUD
        self.add_system(HPRenderer())

        ### Scene behaviour
        self.add_system(FallBackToFramework())

        from cutecats.systems.debug_utils import CollisionsDebugRenderer
        # self.add_system(CollisionsDebugRenderer())
