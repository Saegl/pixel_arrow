import pygame as pg
from dataclasses import dataclass


@dataclass
class Button:
    clickable_area: pg.Rect
    text: str
    default_image: pg.Surface
    hover_image: pg.Surface



class TextButton:
    def __init__(self, text, center_pos, font) -> None:
        self.text = text
        self.center_pos = center_pos
        self.default_image = font.render(
            text, False, (255, 255, 255)
        )
        self.hover_image = font.render(
            text, False, (200, 200, 200)
        )
        self.rect = self.default_image.get_rect(center=center_pos)
    
    def blit(self, surf, mouse_pos):
        hover = self.rect.collidepoint(mouse_pos)
        surf.blit(self.default_image if not hover else self.hover_image, self.rect)
    
    def pressed(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
