import pygame as pg
from flecs import System


class FallBackToFramework(System):
    """
    Event fallback to framework layer
    It will pop active scene on ESCAPE and quit the game on window close
    Also provides debug features on F1, F2, see GameFramework.on_key_down
    for more details
    """
    def on_key_down(self, e: pg.event.Event):
        framework_layer = self.scene.game.event_handler.framework_layer
        default_handler = framework_layer.get_handler(e.type)
        assert framework_layer.name == 'framework'
        default_handler(e)
    
    def on_quit(self, e: pg.event.Event):
        framework_layer = self.scene.game.event_handler.framework_layer
        default_handler = framework_layer.get_handler(e.type)
        assert framework_layer.name == 'framework'
        default_handler(e)
