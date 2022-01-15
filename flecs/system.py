from typing import TYPE_CHECKING, Union
import pygame as pg

if TYPE_CHECKING:
    from flecs.scene import Scene


class System:
    """
    System.scene attr is set by Scene.add_system(),
    but it is not set in __init__().
    It is used to access entities and components
    """

    scene: Union["Scene", None] = None

    def on_mouse_button_up(self, event: pg.event.Event):
        pass

    def process(self, dt, scene: "Scene"):
        pass
