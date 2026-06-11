import time

import pygame


class FPSManager:

    def __init__(self, fps_limit: int = 240) -> None:
        self._clock = pygame.time.Clock()
        self.fps_limit = fps_limit
        self._dt_ms: float = 0.0
        self._current_fps: float = 0.0
        self._last_time = time.perf_counter()

    def tick(self) -> None:
        self._clock.tick(self.fps_limit)
        now = time.perf_counter()
        self._dt_ms = (now - self._last_time) * 1000.0
        self._last_time = now
        self._current_fps = self._clock.get_fps()

    @property
    def dt_ms(self) -> float:
        return self._dt_ms

    @property
    def dt_seconds(self) -> float:
        return self._dt_ms / 1000.0

    @property
    def current_fps(self) -> float:
        return self._current_fps