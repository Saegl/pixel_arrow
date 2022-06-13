import json
import pygame as pg
from cutecats.systems.scenes_utils import FallBackToFramework
from cutecats.systems.ui import TextButton
from flecs import Scene, System

from cutecats import easings
from cutecats.components.world import DecorativeTiles, World, CollisionTiles
from cutecats.systems.worldrender import TileSets, WorldCameraClear, WorldCameraRender, MapRenderer
from cutecats.config import screen_size

from cutecats.scenes.new_server_dialog import NewServerDialog


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
    def __init__(self, scene: Scene):
        font = scene.game.res.debug_font
        self.new_server = TextButton('New Server', (0, 0), font)
        self.scan_local = TextButton('Scan local', (0, 0), font)
        self.join_by_ip = TextButton('Join by IP', (0, 0), font)
        self.back = TextButton('Back', (0, 0), font)
    
    def on_mouse_button_up(self, event: pg.event.Event):
        mouse_pos = self.scene.game.get_mouse_pos()
        mouse_pos = (mouse_pos[0], mouse_pos[1] + 144)

        if self.new_server.pressed(mouse_pos):
            print("New Server")
            self.scene.game.push(NewServerDialog(self.scene.game))
        elif self.scan_local.pressed(mouse_pos):
            print("Scan local")
        elif self.join_by_ip.pressed(mouse_pos):
            print("Join by IP")
        elif self.back.pressed(mouse_pos):
            self.scene.get_system(CloseEffect).activated = True

    def process(self, dt, scene: Scene):
        world: World = scene.get_component(World)
        font = scene.game.res.debug_font
        label = font.render(
            "Multiplayer Settings", False, pg.Color("white"))
        
        # After Open Effect world is shifted by 144 pixels
        y_start = 144
        padd = 16
        mpadd = 8
        swidth, sheight = screen_size
        lwidth, lheight = label.get_size()

        box_color = (102, 57, 49)
        
        right_box_width = 16 * 5

        left_box_x = padd
        left_box_y = y_start + padd + mpadd + lheight
        left_box_width = swidth - padd * 2 - right_box_width - mpadd
        left_box_height = sheight - padd * 2 - lheight - mpadd

        right_box_x = left_box_x + left_box_width + mpadd
        right_box_y = left_box_y
        right_box_height = left_box_height


        world.surf.blit(label, (swidth // 2 - lwidth // 2, y_start + padd))

        pg.draw.rect(world.surf, box_color,
            (
                left_box_x, left_box_y,
                left_box_width, left_box_height
            )
        )
        pg.draw.rect(world.surf, box_color,
            (
                right_box_x, right_box_y,
                right_box_width, right_box_height
            )
        )

        mouse_pos = self.scene.game.get_mouse_pos()
        mouse_pos = (mouse_pos[0], mouse_pos[1] + y_start)

        self.new_server.rect.topleft = (right_box_x + mpadd, right_box_y + 4)
        self.new_server.blit(world.surf, mouse_pos)

        self.scan_local.rect.topleft = (right_box_x + mpadd, right_box_y + 4 + mpadd + lheight)
        self.scan_local.blit(world.surf, mouse_pos)

        self.join_by_ip.rect.topleft = (right_box_x + mpadd, right_box_y + 4 + mpadd * 2 + lheight * 2)
        self.join_by_ip.blit(world.surf, mouse_pos)

        self.back.rect.topleft = (right_box_x + mpadd, right_box_y + 4 + mpadd * 3 + lheight * 3)
        self.back.blit(world.surf, mouse_pos)


class MultiplayerChooser(Scene):
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
        self.add_system(MultiplayerSettingsRenderer(self))
        self.add_system(WorldCameraRender())
