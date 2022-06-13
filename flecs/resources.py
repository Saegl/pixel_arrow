from dataclasses import dataclass
import pygame as pg

from flecs.config import Config
from flecs.image_store import ImageStore


@dataclass
class Resources:
    images: ImageStore
    debug_font: pg.font.Font
    font: pg.font.Font

    @staticmethod
    def loader(config: Config) -> "Resources":
        return Resources(
            images=ImageStore.load_images(config),
            debug_font=pg.font.Font(config.game_font_folder, config.debug_font_size),
            font=pg.font.Font(config.game_font_folder, 42),
        )
