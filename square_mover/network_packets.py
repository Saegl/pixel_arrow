from dataclasses import dataclass

@dataclass
class PlayerAction:
    up: bool
    down: bool
    left: bool
    right: bool


@dataclass
class GameState:
    x: float
    y: float