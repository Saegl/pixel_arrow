"""
Flecs (Fluffy Library for Entity Component System) is my implementation of
the Entity Component System (ECS). it is made to work with pygame.
One of the key features is hot-reloading: when system is changed, is automatically
reloaded the game, without having to restart the python interpreter / reload window.
Look at https://en.wikipedia.org/wiki/Entity_component_system for more info.
"""

from flecs.system import System
from flecs.scene import Scene
from flecs.component import Component
from flecs.framework import GameFramework
from flecs.config import Config

__all__ = [System, Scene, GameFramework, Component, Config]
