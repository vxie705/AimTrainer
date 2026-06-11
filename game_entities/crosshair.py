from typing import Tuple

import pygame


class Crosshair:

    def __init__(
        self,
        size: int = 20,
        thickness: int = 2,
        color: Tuple[int, int, int] = (0, 255, 0),
        gap: int = 4,
        dot_radius: int = 2,
    ) -> None:
        self.size = size
        self.thickness = thickness
        self.color = color
        self.gap = gap
        self.dot_radius = dot_radius

    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        s2 = self.size // 2
        g = self.gap
        t = self.thickness

        pygame.draw.rect(screen, self.color, (x - t // 2, y - s2, t, s2 - g))
        pygame.draw.rect(screen, self.color, (x - t // 2, y + g, t, s2 - g))
        pygame.draw.rect(screen, self.color, (x - s2, y - t // 2, s2 - g, t))
        pygame.draw.rect(screen, self.color, (x + g, y - t // 2, s2 - g, t))

        if self.dot_radius > 0:
            pygame.draw.circle(screen, self.color, (x, y), self.dot_radius)