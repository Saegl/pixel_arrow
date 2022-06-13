from typing import Any
import pygame as pg


class DebugScreen:
    def __init__(self, screen_size: tuple[int, int], font: pg.font.Font) -> None:
        self.screen: pg.Surface = pg.Surface(screen_size, pg.SRCALPHA)
        self.info: dict[str, Any] = {}
        self.show: bool = False
        self.font: pg.font.Font = font
    
    
    def update_screen(self):
        self.screen.fill((0, 0, 0, 100))
        debug_lines = []
        for key, value in self.info.items():
            debug_lines.append(f"{key}: {value}")

        offset_x = 5.0
        offset_y = 5.0
        offset_y_between = self.font.get_height() + 3.0
        for i, line in enumerate(debug_lines):
            self.screen.blit(
                self.font.render(line, False, (255, 255, 255)),
                (offset_x, offset_y + i * offset_y_between),
            )
    
    def update_fps(self, clock: pg.time.Clock):
        self.info["FPS"] = int(clock.get_fps())
