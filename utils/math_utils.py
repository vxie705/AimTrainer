import math
from typing import Tuple


def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))


def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def inside_circle(
    point: Tuple[float, float],
    center: Tuple[float, float],
    radius: float,
) -> bool:
    return distance(point, center) <= radius