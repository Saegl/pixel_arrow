import pygame as pg


class MultiHandler:
    def __init__(self):
        self.listeners = []
    
    def add_listener(self, listener):
        self.listeners.append(listener)
    
    def __call__(self, event: pg.event.Event):
        for listener in self.listeners:
            listener(event)
    
    def is_empty(self):
        return len(self.listeners) == 0


class HandlersLayer:
    def __init__(self, fallback: bool, name: str='Unnamed'):
        self.handlers: dict[int, MultiHandler] = {}
        self.fallback = fallback
        self.name = name

    def set_handler(self, event_type, handler: MultiHandler):
        self.handlers[event_type] = handler

    def get_handler(self, event_type) -> MultiHandler:
        return self.handlers.get(event_type, MultiHandler())

class EventHandler:
    def __init__(self) -> None:
        self.chain: list[HandlersLayer] = []
        self.event_name_to_type: dict[str, int] = {
            'on_quit': pg.QUIT,
            'on_key_down': pg.KEYDOWN,
            'on_key_up': pg.KEYUP,
            'on_mouse_button_down': pg.MOUSEBUTTONDOWN,
            'on_mouse_button_up': pg.MOUSEBUTTONUP,
        }
    
    @property
    def framework_layer(self) -> HandlersLayer:
        """
        Framework layer is the last layer in the chain
        It is always available and initialized by GameFramework
        """
        return self.chain[0]
    
    @property
    def active_layer(self) -> HandlersLayer:
        return self.chain[-1]

    def push_layer(self, fallback: bool, name: str='Unnamed') -> None:
        print("PUSH LAYER:", name)
        self.chain.append(HandlersLayer(fallback, name))
    
    def pop_layer(self) -> None:
        print("POP LAYER", self.active_layer.name)
        self.chain.pop()

    def add_handler(self, event_type, handler) -> None:
        mhandler = self.active_layer.get_handler(event_type)
        mhandler.add_listener(handler)
        self.active_layer.set_handler(event_type, mhandler)
    
    def add_handler_by_name(self, event_name, handler) -> None:
        event_type = self.event_name_to_type[event_name]
        self.add_handler(event_type, handler)
    
    def add_handler_by_method(self, method) -> None:
        event_name = method.__name__
        event_type = self.event_name_to_type[event_name]
        self.add_handler(event_type, method)
    
    def dispatch_events(self) -> None:
        for event in pg.event.get():
            self.process_event(event)
    
    def get_handler_from_chain(self, event_type) -> MultiHandler:
        for layer in reversed(self.chain):
            handler = layer.get_handler(event_type)
            if not handler.is_empty():
                return handler
            if not layer.fallback:
                break
        return MultiHandler()

    def process_event(self, event: pg.event.Event) -> None:
        handler = self.get_handler_from_chain(event.type)
        if not handler.is_empty():
            handler(event)
        else:
            pass
            # print(f"Event is not processed: {pg.event.event_name(event.type)}")
