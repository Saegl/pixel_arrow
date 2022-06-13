import sys
import ctypes
import time
from typing import Sequence
import pygame as pg

from flecs.resources import Resources
from flecs.scene import Scene
from flecs.config import Config
from flecs.debug_screen import DebugScreen
from flecs.event_handler import EventHandler


class GameFramework:
    def __init__(self, config: Config) -> None:
        pg.init()
        pg.display.set_caption(config.caption)

        self.config = config
        self.clock = pg.time.Clock()


        try:
            # TODO config high_dpi
            ctypes.windll.user32.SetProcessDPIAware()
        except AttributeError:
            # Non windows machine
            pass

        if config.fullscreen:
            self.display = pg.display.set_mode(config.window_size, pg.FULLSCREEN | config.flags)
        else:
            self.display = pg.display.set_mode(config.window_size, config.flags, depth=24)
            # self.display = pg.display.set_mode((1280, 720))
        self.screen = pg.Surface(config.screen_size)
        self.is_fullscreen = config.fullscreen

        self.screen_scale = 1
        self.screen_x_offset = 0
        self.screen_y_offset = 0

        if config.use_busy_loop:
            self.sync_fps = self.clock.tick_busy_loop
        else:
            self.sync_fps = self.clock.tick
        self.pressed_keys: Sequence[bool] = pg.key.get_pressed()
        self.res = Resources.loader(config)

        self.event_handler = EventHandler()
        self.event_handler.push_layer(fallback=False, name='framework')

        self.event_handler.add_handler_by_method(self.on_quit)
        self.event_handler.add_handler_by_method(self.on_key_down)

        self.scenes: list["Scene"] = []
        self.active_scene = None
        self.debug = DebugScreen(config.screen_size, self.res.debug_font)
        
        self.display_update_time = time.perf_counter_ns()
        self.debug.info['lag'] = 0

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

    def on_key_down(self, event: pg.event.Event):
        # print(event.unicode)
        # if event.key == pg.K_ESCAPE:
        #     self.on_quit(None)
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
        if event.key == pg.K_F2:
            print("screenshot")
            pg.image.save(self.screen, "screenshot.png")
        if event.key == pg.K_ESCAPE:
            print("framework pop")
            print(self.scenes)
            self.pop()
    
    def display_update(self):
        display_dt = time.perf_counter_ns() - self.display_update_time
        self.display_update_time = time.perf_counter_ns()
        # self.debug.info['display dt ns'] = display_dt

        # 1 sec is 1_000_000_000 ns
        # Delta time between frames should be 1 / framerate
        # E.X framerate = 60  =>  1s / 60 = 0.01666s = 0_016_666_666ns
        # if dt >= 16_666_666ns we have display lag
        # log that
        # threshold = 1_000 # some ns to allow little lag
        # expected_dt = 1 / self.config.framerate * 10**9 + threshold

        # self.debug.info['lag'] += display_dt >= expected_dt

        # pg.display.update()
        pg.display.flip()

    def gameloop(self):
        dt = 0

        while True:
            self.debug.update_fps(self.clock)
            self.event_handler.dispatch_events()
            self.process(dt)
            dt = self.sync_fps(self.config.framerate)
            self.display_update()

    def on_quit(self, _: pg.event.Event = None):
        """Pop and destory all scenes"""
        print("Framework quit")
        while True:
            self.pop()
