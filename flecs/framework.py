import sys
from typing import Sequence
import pygame as pg

from flecs.resources import Resources
from flecs.scene import Scene
from flecs.config import Config
from flecs.debug_screen import DebugScreen


class GameFramework:
    def __init__(self, config: Config) -> None:
        pg.init()
        pg.display.set_caption(config.caption)

        self.config = config
        self.clock = pg.time.Clock()

        if config.fullscreen:
            self.display = pg.display.set_mode((0, 0), pg.FULLSCREEN | config.flags)
        else:
            self.display = pg.display.set_mode(config.window_size, config.flags)
        self.screen = pg.Surface(config.screen_size)
        self.is_fullscreen = config.fullscreen

        self.screen_scale = 1
        self.screen_x_offset = 0
        self.screen_y_offset = 0

        if config.use_busy_loop:
            self.sync_fps = self.clock.tick_busy_loop
        else:
            self.sync_fps = self.clock.tick
        self.display_update = pg.display.update
        self.pressed_keys: Sequence[bool] = pg.key.get_pressed()
        self.res = Resources.loader(config)
        self.event_handlers = {
            pg.QUIT: self.on_quit,
            pg.KEYDOWN: self.on_keydown,
            pg.KEYUP: self.on_keyup,
            pg.MOUSEBUTTONUP: self.on_mouse_button_up,
        }
        self.scenes: list["Scene"] = []
        self.active_scene = None
        self.debug = DebugScreen(config.screen_size, self.res.debug_font)

    def push(self, scene: "Scene"):
        # TODO Create Navigator class
        self.scenes.append(scene)
        self.active_scene = scene
        self.debug.info["active scene"] = type(self.active_scene).__name__

    def pop(self):
        try:
            closed_scene = self.scenes.pop()
            closed_scene.destroy()
            self.active_scene = self.scenes[-1]
            self.debug.info["active scene"] = type(self.active_scene).__name__
        except IndexError:
            pg.quit()
            sys.exit()

    def get_mouse_pos(self):
        mouse_pos = pg.mouse.get_pos()
        return (
            1 / self.screen_scale * (mouse_pos[0] - self.screen_x_offset),
            1 / self.screen_scale * (mouse_pos[1] - self.screen_y_offset),
        )

    def process(self, dt):
        self.debug.screen.fill((0, 0, 0, 0))
        self.pressed_keys = pg.key.get_pressed()
        self.active_scene.process(dt)
        screen_size = self.screen.get_size()
        display_size = self.display.get_size()

        self.screen_scale = min(
            display_size[0] / screen_size[0], display_size[1] / screen_size[1]
        )
        screen_rect = pg.Rect(
            0, 0, screen_size[0] * self.screen_scale, screen_size[1] * self.screen_scale
        )
        display_rect = pg.Rect(0, 0, display_size[0], display_size[1])
        screen_rect.center = display_rect.center

        self.screen_x_offset = screen_rect.x
        self.screen_y_offset = screen_rect.y

        surf = pg.transform.scale(self.screen, screen_rect.size)
        self.display.blit(surf, (self.screen_x_offset, self.screen_y_offset))
        if self.debug.show:
            self.debug.update_screen()
            debug_surf = pg.transform.scale(self.debug.screen, screen_rect.size)
            self.display.blit(debug_surf, (self.screen_x_offset, self.screen_y_offset))

    def on_keydown(self, event: pg.event.Event):
        if event.key == pg.K_F11:
            if not self.is_fullscreen:
                self.display = pg.display.set_mode(
                    (0, 0), pg.FULLSCREEN | self.config.flags
                )
            else:
                self.display = pg.display.set_mode(
                    self.config.window_size, self.config.flags
                )
            self.is_fullscreen = not self.is_fullscreen
        if event.key == pg.K_F1:
            self.debug.show = not self.debug.show
        self.active_scene.on_keydown(event)

    def on_keyup(self, event: pg.event.Event):
        self.active_scene.on_keyup(event)

    def on_mouse_button_up(self, event: pg.event.Event):
        self.active_scene.on_mouse_button_up(event)

    def dispatch_events(self):
        for event in pg.event.get():
            handler = self.event_handlers.get(event.type)
            if handler:
                handler(event)
            else:
                pass
                # print(f"Event is not processed: {pg.event.event_name(event.type)}")

    def gameloop(self):
        dt = 0

        while True:
            self.debug.update_fps(self.clock)
            self.dispatch_events()
            self.process(dt)
            dt = self.sync_fps(self.config.framerate)
            self.display_update()

    def on_quit(self, _: pg.event.Event = None):
        """Pop and destory all scenes"""
        while True:
            self.pop()
