import pygame as pg
from dataclasses import dataclass
from flecs import Scene, System
from pixel_arrow.scenes.level_editor import LevelEditorScene
from pixel_arrow.scenes.singleplayer import SingleplayerScene


@dataclass
class MenuPopup(System):
    def __init__(self, scene: Scene) -> None:
        images = scene.game.res.images
        screen = scene.game.screen
        screen_rect = screen.get_rect()

        buttons_x = screen_rect.centerx - images.menu_button_default.get_width() // 2
        first_button_y = 275
        buttons_dy = 115

        first_button_pos = (buttons_x, first_button_y)
        second_button_pos = (buttons_x, first_button_y + buttons_dy)
        third_button_pos = (buttons_x, first_button_y + 2 * buttons_dy)

        self.first_button_rect = images.menu_button_default.get_rect()
        self.first_button_rect.topleft = first_button_pos

        self.second_button_rect = images.menu_button_default.get_rect()
        self.second_button_rect.topleft = second_button_pos

        self.third_button_rect = images.menu_button_default.get_rect()
        self.third_button_rect.topleft = third_button_pos

    def on_mouse_button_up(self, event: pg.event.Event):
        mouse_pos = self.scene.game.get_mouse_pos()

        if self.first_button_rect.collidepoint(mouse_pos):
            self.scene.game.push(SingleplayerScene(self.scene.game))

        if self.second_button_rect.collidepoint(mouse_pos):
            self.scene.game.push(LevelEditorScene(self.scene.game))

        if self.third_button_rect.collidepoint(mouse_pos):
            self.scene.game.pop()

    def process(self, dt, scene: Scene):
        images = scene.game.res.images
        screen = scene.game.screen
        screen_rect = screen.get_rect()

        menu_popup_rect = images.menu_popup.get_rect()
        menu_popup_rect.center = screen_rect.center

        screen.blit(
            scene.game.res.images.menu_popup,
            (menu_popup_rect.left, menu_popup_rect.top),
        )
        screen.blit(
            images.menu_button_default,
            self.first_button_rect.topleft,
        )
        screen.blit(
            images.menu_button_default,
            self.second_button_rect.topleft,
        )
        screen.blit(
            images.menu_button_default,
            self.third_button_rect.topleft,
        )

        mouse_pos = scene.game.get_mouse_pos()

        if self.first_button_rect.collidepoint(mouse_pos):
            screen.blit(
                images.menu_button_active,
                self.first_button_rect.topleft,
            )

        if self.second_button_rect.collidepoint(mouse_pos):
            screen.blit(
                images.menu_button_active,
                self.second_button_rect.topleft,
            )

        if self.third_button_rect.collidepoint(mouse_pos):
            screen.blit(
                images.menu_button_active,
                self.third_button_rect.topleft,
            )

        first_label = self.scene.game.res.font.render(
            "Start game", True, (255, 255, 255)
        )
        first_label_rect = first_label.get_rect()
        first_label_rect.center = self.first_button_rect.center
        screen.blit(first_label, first_label_rect)

        second_label = self.scene.game.res.font.render(
            "Level Editor", True, (255, 255, 255)
        )
        second_label_rect = second_label.get_rect()
        second_label_rect.center = self.second_button_rect.center
        screen.blit(second_label, second_label_rect)

        third_label = self.scene.game.res.font.render("Exit", True, (255, 255, 255))
        third_label_rect = third_label.get_rect()
        third_label_rect.center = self.third_button_rect.center
        screen.blit(third_label, third_label_rect)
