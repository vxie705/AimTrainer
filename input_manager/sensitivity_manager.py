from typing import Tuple


class SensitivityManager:

    def __init__(self, multiplier: float = 1.0, invert_y: bool = False) -> None:
        self.multiplier = multiplier
        self.invert_y = invert_y

    def apply(self, raw_dx: float, raw_dy: float) -> Tuple[float, float]:
        dx = raw_dx * self.multiplier
        dy = raw_dy * self.multiplier
        if self.invert_y:
            dy = -dy
        return dx, dy