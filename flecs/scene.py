import importlib
import sys
from typing import TYPE_CHECKING, Type, TypeVar
from collections import defaultdict
from functools import reduce

import pygame as pg

from flecs.filewatcher import FileWatcher

from flecs.entity import Entity

if TYPE_CHECKING:
    from flecs.framework import GameFramework
    from flecs.system import System
    from flecs.component import Component


T = TypeVar('T')

class Scene:
    def __init__(self, game: "GameFramework", name: str = 'Unnamed') -> None:
        self.game = game
        self.entities: defaultdict[Entity] = defaultdict(dict)
        self.components: defaultdict[Type["Component"], set[Entity]] = defaultdict(set)
        self.systems: list['System'] = []

        # TODO: move to GameFramework
        if game.config.enable_hot_reload:
            self.systems_watcher = FileWatcher("pixel_arrow/systems")
        
        self.game.event_handler.push_layer(fallback=True, name=name)

    def create_enitity(self, *components: tuple['Component']) -> Entity:
        entity = Entity()
        for cmp in components:
            entity.add_component(cmp)
            self.components[type(cmp)].add(entity)
        return entity

    def remove_entity(self, entity: Entity) -> None:
        for component_type in self.entities[entity]:
            self.components[component_type].remove(entity)
        del self.entities[entity]

    def get_entities(self, *query: tuple[Type['Component']]):
        entities_by_component = [self.components[q] for q in query]
        entities = reduce(set.intersection, entities_by_component)
        for entity in entities:
            returned_components = []
            for component_type in query:
                returned_components.append(entity.get_component(component_type))
            yield entity, returned_components

    def get_component(self, component_type: Type[T]) -> T:
        if len(self.components[component_type]) != 1:
            raise ValueError("Cannot get one component, collection len is not 1")

        for entity in self.components[component_type]:
            return entity.get_component(component_type)
        raise ValueError("Unreachable code")

    def add_system(self, system):
        system.scene = self
        self.systems.append(system)

        for event_name in self.game.event_handler.event_name_to_type:
            if hasattr(system, event_name):
                self.game.event_handler.add_handler_by_method(
                    getattr(system, event_name)
                )
    
    def del_system(self, system):
        system.scene = None
        self.systems.remove(system)

        # TODO remove handlers from event_handler
    
    def get_system(self, system_type: Type["System"]) -> "System":
        for system in self.systems:
            if isinstance(system, system_type):
                return system
        raise ValueError(f"System {system_type} not found")

    def systems_hot_reload(self):
        for updated_file in self.systems_watcher.get_updates():
            print("File changed", updated_file)
            for i, system in enumerate(self.systems):
                file_module_name = self.game.config.systems_module_prefix + updated_file
                if system.__module__ == file_module_name:
                    system_module = importlib.import_module(file_module_name)
                    try:
                        system_module = importlib.reload(system_module)
                    except Exception as e:
                        print(e)
                        print("Hot reloading aborted")
                        continue
                    updated_cls = getattr(system_module, system.__class__.__name__)
                    print(f"{system.__class__.__name__} updated from {updated_cls}")
                    self.systems[i] = updated_cls()
                    self.systems[i].scene = self

    def process(self, dt):
        if self.game.config.enable_hot_reload:
            self.systems_hot_reload()
        for system in self.systems:
            system.process(dt, self)

    def destroy(self):
        print(f"{type(self).__name__} destroyed")
        if self.game.config.enable_hot_reload:
            self.systems_watcher.kill()
        
        self.game.event_handler.pop_layer()
