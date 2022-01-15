import importlib
import sys
from typing import TYPE_CHECKING, Type, Any
from collections import defaultdict
from functools import reduce

import pygame as pg

from flecs.filewatcher import FileWatcher

if TYPE_CHECKING:
    from flecs.framework import GameFramework
    from flecs.system import System
    from flecs.component import Component


class Scene:
    def __init__(self, game: "GameFramework") -> None:
        self.game = game
        self.entities: defaultdict[int, dict[Any, Any]] = defaultdict(dict)
        self.components: defaultdict[Type["Component"], set[int]] = defaultdict(set)
        self.systems: list["System"] = []
        self._last_entity_id = -1

        self.systems_watcher = FileWatcher("pixel_arrow/systems")

    def create_enitity(self, *components) -> int:
        self._last_entity_id += 1
        entity_id = self._last_entity_id

        for component in components:
            self.components[type(component)].add(entity_id)
            self.entities[entity_id][type(component)] = component

        return entity_id

    def remove_entity(self, entity_id: int):
        for component_type in self.entities[entity_id]:
            self.components[component_type].remove(entity_id)
        del self.entities[entity_id]

    def get_entities(self, *query):
        components = [self.components[q] for q in query]
        if len(components) == 0:
            yield None
        eids = reduce(set.intersection, components)
        for eid in eids:
            components = []
            for component_type in query:
                components.append(self.entities[eid][component_type])
            yield eid, components

    def get_component(self, component_type: Type["Component"]) -> "Component":
        if len(self.components[component_type]) != 1:
            raise ValueError("Cannot get one component, collection len is not 1")

        eid = -1
        for c in self.components[component_type]:
            eid = c
        return self.entities[eid][component_type]

    def add_system(self, system):
        system.scene = self
        self.systems.append(system)
    
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
        self.systems_hot_reload()
        for system in self.systems:
            system.process(dt, self)

    def on_keydown(self, _: pg.event.Event):
        pass

    def on_keyup(self, _: pg.event.Event):
        pass

    def on_mouse_button_up(self, e: pg.event.Event):
        for system in self.systems:
            system.on_mouse_button_up(e)

    def destroy(self):
        print(f"{type(self).__name__} destroyed")
        self.systems_watcher.kill()

    def on_quit(self, _: pg.event.Event):
        self.destroy()
        pg.quit()
        sys.exit()
