from dataclasses import dataclass


@dataclass
class Vector2D:
    x: float
    y: float

    @property
    def xy(self) -> tuple[float, float]:
        return self.x, self.y
