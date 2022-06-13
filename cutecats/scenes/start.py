import json
from dataclasses import dataclass
import pygame as pg
from flecs import Scene, GameFramework, System

from cutecats.king import KING_IDLE, load_king_animations
from cutecats.meowolas import MEOWOLAS_IDLE, load_meowolas_animations
from cutecats.meowtar import MEOWTAR_IDLE, load_meowtar_animations
from cutecats.meow_knight import MEOW_KNIGHT_IDLE, load_meow_knight_animations

from cutecats.components.world import DecorativeTiles, World, CollisionTiles
from cutecats.components.position import Position
from cutecats.components.animation import Animation

from cutecats.systems.worldrender import TileSets, WorldCameraClear, WorldCameraRender, MapRenderer
from cutecats.systems.animations_render import AnimationRenderer
from cutecats.systems.background import BackgroundRenderer
from cutecats.systems.scenes_utils import FallBackToFramework
from cutecats.systems.ui import TextButton

from cutecats.scenes.fight import FightScene
from cutecats.scenes.options import OptionsScene
from cutecats.scenes.multiplayer_chooser import MultiplayerChooser

from cutecats import easings


class OpenEffect(System):
    def __init__(self) -> None:
        self.duration = 75
        self.t = 1

        self.mover = easings.Mover(
            domain=(0, 75),
            range_=(0, 144)
        )
    
    def process(self, dt, scene: Scene):
        world: World = scene.get_component(World)
        self.t += 1
        
        if self.t >= self.duration:
            return scene.del_system(self)

        world.offset.y = 144 - self.mover.value(self.t)


@dataclass
class OnWorldMenu(System):
    def __init__(self, scene: Scene) -> None:
        images = scene.game.res.images
        screen = scene.game.screen

        screen_rect = screen.get_rect()
        self.single_player_button = TextButton(
            'SinglePlayer',
            (screen_rect.centerx, 88),
            scene.game.res.debug_font
        )

        self.multiplayer_button = TextButton(
            'MultiPlayer',
            (screen_rect.centerx, 88 + 16),
            scene.game.res.debug_font
        )

        self.options_button = TextButton(
            'Options',
            (screen_rect.centerx, 88 + 16 * 2),
            scene.game.res.debug_font
        )

    def on_mouse_button_up(self, event: pg.event.Event):
        mouse_pos = self.scene.game.get_mouse_pos()

        if self.single_player_button.pressed(mouse_pos):
            print("SinglePlayer")
            self.scene.game.push(FightScene(self.scene.game))

        if self.multiplayer_button.pressed(mouse_pos):
            print("MultiPlayer")
            # self.scene.game.push(FightScene(self.scene.game))
            self.scene.game.push(MultiplayerChooser(self.scene.game))
        
        if self.options_button.pressed(mouse_pos):
            print("Options")
            self.scene.game.push(OptionsScene(self.scene.game))

    def process(self, dt, scene: Scene):
        images = scene.game.res.images
        world: World = scene.get_component(World)
        world_surf = world.surf

        world_surf.blit(images.logo, (0, 0))

        mouse_pos = scene.game.get_mouse_pos()
        
        self.single_player_button.blit(world_surf, mouse_pos)
        self.multiplayer_button.blit(world_surf, mouse_pos)
        self.options_button.blit(world_surf, mouse_pos)



class StartScene(Scene):
    def __init__(self, game: "GameFramework") -> None:
        super().__init__(game, "StartScene")
        images = game.res.images

        with open('cutecats/res/tilemaps/menu.json') as f:
            json_data = json.load(f)

        self.tiles = CollisionTiles.from_tilemap(json_data, 0)
        self.create_enitity(DecorativeTiles.from_tilemap(json_data, 1))
        self.create_enitity(DecorativeTiles.from_tilemap(json_data, 2))
        self.create_enitity(TileSets(json_data['tilesets'], self.game.res.images))
        
        self.world = self.create_enitity(World(
            offset=pg.math.Vector2(0, 144)
        ), self.tiles)
        self.meow_knight = self.create_enitity(
            Position(pg.math.Vector2(-8, 65)),
            Animation(load_meow_knight_animations(images), current_state=MEOW_KNIGHT_IDLE, look_left=True),
        )

        self.meowalas = self.create_enitity(
            Position(pg.math.Vector2(180, 80)),
            Animation(load_meowolas_animations(images), current_state=MEOWOLAS_IDLE),
        )

        self.meotar = self.create_enitity(
            Position(pg.math.Vector2(-55, 48)),
            Animation(load_meowtar_animations(images), current_state=MEOWTAR_IDLE, look_left=True),
        )

        self.king_meowthur = self.create_enitity(
            Position(pg.math.Vector2(105, 48)),
            Animation(load_king_animations(images), current_state=KING_IDLE),
        )

        ### On screen render
        self.add_system(BackgroundRenderer(images.bg1))
        self.add_system(OpenEffect())

        ### On World Render
        self.add_system(WorldCameraClear())
        self.add_system(MapRenderer(16))
        self.add_system(AnimationRenderer())
        self.add_system(OnWorldMenu(self))
        self.add_system(WorldCameraRender())

        ### Scene behaviour
        self.add_system(FallBackToFramework())
