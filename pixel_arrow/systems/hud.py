from dataclasses import dataclass
import pygame as pg
from flecs import Scene, System
from pixel_arrow.components.character import CharacterState, UserControlled


@dataclass
class HPRenderer(System):
    def process(self, _, scene: Scene):
        screen = scene.game.screen
        images = scene.game.res.images
        offset = 33.0
        for _, (_, cstate) in scene.get_entities(UserControlled, CharacterState):
            for i in range(cstate.hp):
                screen.blit(images.heart, (10.0 + offset * i, 10.0))


@dataclass
class TilesetRenderer(System):
    def __init__(self) -> None:
        self.y_offset = 700
        self.sliding = False
        self.sliding_up = True
        self.opened = False

        self.open_rect = pg.Rect(100, 740, 380, 100)
        self.close_rect = pg.Rect(100, 45, 380, 100)

    def on_mouse_button_up(self, _):
        mouse_pose = self.scene.game.get_mouse_pos()
        if self.opened and self.close_rect.collidepoint(*mouse_pose):
            self.toggle()

        if not self.opened and self.open_rect.collidepoint(*mouse_pose):
            self.toggle()

    def toggle(self):
        if self.y_offset == 700:
            self.sliding_up = False
            self.sliding = True
        if self.y_offset == 0:
            self.sliding_up = True
            self.sliding = True

    def process(self, _, scene: Scene):
        screen = scene.game.screen
        images = scene.game.res.images

        scene.game.debug_info["sliding"] = self.sliding
        scene.game.debug_info["sliding_up"] = self.sliding_up
        scene.game.debug_info["y_offset"] = self.y_offset

        if self.sliding and self.sliding_up and self.y_offset < 700:
            self.y_offset += 50
        elif self.sliding and not self.sliding_up and self.y_offset > 0:
            self.y_offset -= 50
        else:
            self.opened = not self.sliding_up
            self.sliding = False

        screen.blit(images.tiles_list, (0, self.y_offset))

        pg.draw.rect(scene.game.debug_screen, (255, 0, 0, 100), self.open_rect)
        pg.draw.rect(scene.game.debug_screen, (255, 0, 0, 100), self.close_rect)

        tile = iter(images.tiles.values())

        for x in range(15):
            for y in range(3):
                try:
                    screen.blit(
                        next(tile),
                        (50 + (48 + 10) * x, self.y_offset + 200 + (48 + 10) * y),
                    )
                except StopIteration:
                    break
