from typing import Type
from flecs.component import Component


class Entity:
    def __init__(self) -> None:
        self.components: dict[Type[Component], Component] = {}

    def add_component(self, component: Component) -> None:
        self.components[type(component)] = component
    
    def get_component(self, component_type: Type[Component]) -> Component:
        return self.components[component_type]
