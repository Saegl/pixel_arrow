import json
import pygame as pg
from flecs import Scene, System

from cutecats import easings
from cutecats.components.world import DecorativeTiles, World, CollisionTiles
from cutecats.systems.worldrender import TileSets, WorldCameraClear, WorldCameraRender, MapRenderer

class OpenEffect(System):
    def __init__(self, prev_scene_screen):
        self.prev_screen = prev_scene_screen
        self.pos_y = 0

        self.duration = 50
        self.t = 1
        self.mover = easings.Mover(
            domain=(0, self.duration),
            range_=(0, 144)
        )
    
    def process(self, _, scene: Scene):
        screen = scene.game.screen
        world: World = scene.get_component(World)
        self.t += 1
        if self.t >= self.duration:
            print("OpenEffect deleted")
            return scene.del_system(self)
        
        shifted = self.mover.value(self.t)

        world.offset.y = 144 - shifted
        self.pos_y = -shifted
        screen.blit(self.prev_screen, (0, self.pos_y))


class CloseEffect:
    def __init__(self, prev_scene_screen):
        self.prev_screen = prev_scene_screen
        self.pos_y = 0

        self.duration = 50
        self.t = 1
        self.mover = easings.Mover(
            domain=(0, self.duration),
            range_=(0, 144)
        )
        self.activated = False
    
    def on_key_down(self, event):
        if event.key == pg.K_ESCAPE:
            self.activated = True
    
    def process(self, _, scene: Scene):
        if not self.activated:
            return
        
        screen = scene.game.screen
        world: World = scene.get_component(World)
        self.t += 1
        if self.t >= self.duration:
            print("CloseEffect deleted")
            scene.del_system(self)
            scene.game.pop()
            return
        
        shifted = self.mover.value(self.t)

        world.offset.y = shifted
        self.pos_y = -144 + shifted
        screen.blit(self.prev_screen, (0, self.pos_y))


class MultiplayerSettingsRenderer(System):
    def process(self, dt, scene: Scene):
        world: World = scene.get_component(World)
        label = scene.game.res.debug_font.render(
            "Options Editor", False, pg.Color("white"))
        world.surf.blit(label, (256 // 2 - label.get_width() // 2, 144 + 144 // 2))


class OptionsScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game, 'MultiplayerChooser')
        prev_scene_screen = self.game.screen.copy()

        # TODO map resource managing? not load again
        with open('cutecats/res/tilemaps/menu.json') as f:
            json_data = json.load(f)

        self.tiles = CollisionTiles.from_tilemap(json_data, 0)
        self.create_enitity(DecorativeTiles.from_tilemap(json_data, 1))
        self.create_enitity(DecorativeTiles.from_tilemap(json_data, 2))
        self.create_enitity(TileSets(json_data['tilesets'], self.game.res.images))
        
        self.world = self.create_enitity(World(
            clipping_rect=pg.Rect(0, 144, 256, 144),
            offset=pg.math.Vector2(0, 144)
        ), self.tiles)


        self.add_system(OpenEffect(prev_scene_screen))
        self.add_system(CloseEffect(prev_scene_screen))

        self.add_system(WorldCameraClear())
        self.add_system(MapRenderer(16))
        self.add_system(MultiplayerSettingsRenderer())
        self.add_system(WorldCameraRender())
