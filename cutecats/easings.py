import math


def easy_in_out_sine(x: float) -> float:
    return -(math.cos(math.pi * x) - 1) / 2


def easy_out_elastic(x: float) -> float:
    c4 = (2 * math.pi) / 3
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return 2 ** (-10 * x) * math.sin((x * 10 - 0.75) * c4) + 1


class Mover:
    def __init__(self,
        domain: tuple[float, float],
        range_: tuple[float, float],
        fn_name: str = "easy_in_out_sine"
    ):
        self.domain_scaler = domain[1] - domain[0]
        self.range_scaler = range_[1] - range_[0]
        self.fn_name = fn_name
     
    def value(self, x: float) -> float:
        domain_scaled = x / self.domain_scaler  # 0.0 to 1.0
        blend = globals()[self.fn_name](domain_scaled)
        range_scaled = blend * self.range_scaler  # range_[0] to range_[1]
        return range_scaled
