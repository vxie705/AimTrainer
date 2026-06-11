from enum import Enum, auto
from typing import Tuple

import pygame


class TargetState(Enum):
    SPAWNING = auto()
    ALIVE = auto()
    DYING = auto()
    EXPIRED = auto()
    DEAD = auto()


class Target:

    def __init__(
        self,
        x: float,
        y: float,
        radius: int,
        color: Tuple[int, int, int],
        hit_color: Tuple[int, int, int],
        lifetime_ms: int,
    ) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.hit_color = hit_color
        self.current_color = color
        self.lifetime_ms = lifetime_ms
        self.state = TargetState.SPAWNING

        self._spawn_timer: float = 0.0
        self._alive_timer: float = 0.0
        self._dying_timer: float = 0.0

        self.spawn_duration_ms = 150
        self.dying_duration_ms = 120

        self._spawn_scale: float = 0.0

    def update(self, dt_ms: float) -> None:
        if self.state == TargetState.SPAWNING:
            self._update_spawning(dt_ms)
        elif self.state == TargetState.ALIVE:
            self._update_alive(dt_ms)
        elif self.state == TargetState.DYING:
            self._update_dying(dt_ms)

    def _update_spawning(self, dt_ms: float) -> None:
        self._spawn_timer += dt_ms
        progress = min(self._spawn_timer / self.spawn_duration_ms, 1.0)
        self._spawn_scale = progress
        if progress >= 1.0:
            self.state = TargetState.ALIVE
            self._spawn_scale = 1.0
            self._alive_timer = 0.0

    def _update_alive(self, dt_ms: float) -> None:
        self._alive_timer += dt_ms
        if self._alive_timer >= self.lifetime_ms:
            self.state = TargetState.EXPIRED

    def _update_dying(self, dt_ms: float) -> None:
        self._dying_timer += dt_ms
        if self._dying_timer >= self.dying_duration_ms:
            self.state = TargetState.DEAD

    def hit(self) -> bool:
        if self.state == TargetState.ALIVE:
            self.state = TargetState.DYING
            self._dying_timer = 0.0
            self.current_color = self.hit_color
            return True
        return False

    @property
    def position(self) -> Tuple[float, float]:
        return (self.x, self.y)

    @property
    def draw_radius(self) -> float:
        return self.radius * self._spawn_scale

    @property
    def is_clickable(self) -> bool:
        return self.state == TargetState.ALIVE

    @property
    def is_alive(self) -> bool:
        return self.state in (TargetState.SPAWNING, TargetState.ALIVE)

    @property
    def is_removable(self) -> bool:
        return self.state in (TargetState.EXPIRED, TargetState.DEAD)

    def draw(self, screen: pygame.Surface) -> None:
        if self.state == TargetState.DEAD:
            return
        color = self.current_color if self.state == TargetState.DYING else self.color
        r = int(self.draw_radius)
        if r < 1:
            return
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), r)
        pygame.draw.circle(
            screen, (255, 255, 255), (int(self.x), int(self.y)), r, max(1, r // 10)
        )