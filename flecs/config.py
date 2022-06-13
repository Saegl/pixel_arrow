from dataclasses import dataclass


@dataclass
class Config:
    caption: str  # Window Title
    fullscreen: bool
    flags: int  # Pygame display mode flags
    window_size: tuple[int, int]  # When not fullscreen
    screen_size: tuple[
        int, int
    ]  # Virtual Screen Size active in both fullscreen and windowed
    framerate: int
    use_busy_loop: bool  # More tick precise and more cpu usage

    images_folder: str
    game_font_folder: str ## TODO game_font_path
    debug_font_size: int
    
    enable_hot_reload: bool
    systems_module_prefix: str


    @staticmethod
    def from_obj_attrs(obj: object) -> "Config":
        attrs = {}
        for fieldname, field in Config.__dataclass_fields__.items():
            value = getattr(obj, fieldname)
            if hasattr(field.type, "__origin__"):
                # Check for generic types
                if not isinstance(value, field.type.__origin__):
                    raise TypeError(f"{fieldname} must be of type {field.type}")
            elif not isinstance(value, field.type):
                raise TypeError(f"{fieldname} must be of type {field.type}")
            attrs[fieldname] = getattr(obj, fieldname)
        return Config(**attrs)
