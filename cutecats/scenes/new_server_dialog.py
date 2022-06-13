import pygame as pg
from flecs import Scene, System
from cutecats.systems.scenes_utils import FallBackToFramework


class DialogRender(System):
    def __init__(self, prev_screen) -> None:
        self.prev_screen = prev_screen
    
    def process(self, dt, scene: "Scene"):
        screen = scene.game.screen
        screen.blit(self.prev_screen, (0, 0))

        swidth, sheight = screen.get_size()
        dialog_box = pg.Rect(
            0, 0, 100, 100
        )
        dialog_box.center = screen.get_rect().center

        pg.draw.rect(screen, (0, 0, 0), dialog_box)



class NewServerDialog(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.prev_screen = game.screen.copy()

        self.add_system(DialogRender(self.prev_screen))
        self.add_system(FallBackToFramework())
