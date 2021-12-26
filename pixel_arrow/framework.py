from dataclasses import dataclass
import sys
from collections import defaultdict

import pygame as pg
from pygame import Surface
from pygame.event import Event
from pygame.font import Font
from pygame.locals import *

from pixel_arrow import config
from pixel_arrow.image_store import ImageStore


@dataclass
class Resources:
    images: ImageStore
    font: Font


class GameFramework:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption(config.caption)
        self.clock = pg.time.Clock()

        if config.fullscreen:
            self.display = pg.display.set_mode((0, 0), pg.FULLSCREEN | pg.DOUBLEBUF)
            # self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
        else:
            self.display = pg.display.set_mode(config.window_size, 0, 32)
        self.screen = Surface(config.screen_size)

        if config.use_busy_loop:
            self.sync_fps = self.clock.tick_busy_loop
        else:
            self.sync_fps = self.clock.tick
        self.display_update = pg.display.update
        self.pressed_keys = defaultdict(bool)
        self.res = Resources(
            ImageStore.load_images(self.screen.get_size()),
            pg.font.SysFont("Arial", 18)
        )
        self.event_handlers = {
            QUIT: self.on_quit,
            KEYDOWN: self.on_keydown,
            KEYUP: self.on_keyup,
            MOUSEBUTTONUP: self.on_mouse_button_up,
        }
        self.scenes = []
        self.active_scene = None
    
    def push(self, scene: 'Scene'):
        self.scenes.append(scene)
        self.active_scene = scene
    
    def pop(self):
        try:
            closed_scene = self.scenes.pop()
            closed_scene.destroy()
            self.active_scene = self.scenes[-1]
        except IndexError:
            pg.quit()
            sys.exit()

    
    def draw(self):
        self.active_scene.draw()

    def update(self, dt):
        self.active_scene.update(dt)

    def on_keydown(self, event: Event):
        self.pressed_keys[event.key] = True
        self.active_scene.on_keydown(event)
    
    def on_keyup(self, event: Event):
        self.pressed_keys[event.key] = False
        self.active_scene.on_keyup(event)
    
    def on_mouse_button_up(self, event: Event):
        self.active_scene.on_mouse_button_up(event)
    
    def dispatch_events(self):
        for event in pg.event.get():
            handler = self.event_handlers.get(event.type)
            if handler:
                handler(event)

    def gameloop(self):
        dt = 0

        while True:
            self.dispatch_events()
            self.update(dt)
            self.draw()
            self.display_update()
            dt = self.sync_fps(config.framerate)
    
    def on_quit(self, e: Event = None):
        self.active_scene.on_quit(e)


# TODO Abstract methods
class Scene:
    def __init__(self, game: GameFramework) -> None:
        self.game = game
        self.entities = []
    
    def create_enitty(*components):
        pass

    def draw(self):
        pass

    def update(self, dt):
        pass

    def on_keydown(self, _: Event):
        pass

    def on_keyup(self, _: Event):
        pass

    def on_mouse_button_up(self, _: Event):
        pass

    def destroy(self):
        pass

    def on_quit(self, _: Event):
        pass
