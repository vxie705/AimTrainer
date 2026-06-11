from enum import Enum, auto
from typing import List, Tuple

import pygame


class GameEvent(Enum):
    QUIT = auto()
    SHOOT = auto()
    SHOOT_RELEASE = auto()
    RESTART = auto()
    TOGGLE_PAUSE = auto()
    SENSITIVITY_UP = auto()
    SENSITIVITY_DOWN = auto()
    TARGET_SIZE_UP = auto()
    TARGET_SIZE_DOWN = auto()
    TOGGLE_MODE = auto()
    FULLSCREEN = auto()


class EventHandler:

    def __init__(self) -> None:
        self._events: List[GameEvent] = []
        self._mouse_rel: Tuple[float, float] = (0.0, 0.0)
        self._mouse_pos: Tuple[int, int] = (0, 0)
        self._keys_pressed: set = set()
        self._raw_dx: float = 0.0
        self._raw_dy: float = 0.0

    def update(self) -> None:
        self._events.clear()

        self._raw_dx, self._raw_dy = pygame.mouse.get_rel()
        self._mouse_pos = pygame.mouse.get_pos()
        self._keys_pressed = set()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._events.append(GameEvent.QUIT)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._events.append(GameEvent.SHOOT)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self._events.append(GameEvent.SHOOT_RELEASE)

            elif event.type == pygame.KEYDOWN:
                self._keys_pressed.add(event.key)
                self._process_keydown(event.key)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
            self._events.append(GameEvent.SENSITIVITY_UP)
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            self._events.append(GameEvent.SENSITIVITY_DOWN)
        if keys[pygame.K_LEFTBRACKET]:
            self._events.append(GameEvent.TARGET_SIZE_DOWN)
        if keys[pygame.K_RIGHTBRACKET]:
            self._events.append(GameEvent.TARGET_SIZE_UP)

    def _process_keydown(self, key: int) -> None:
        if key == pygame.K_ESCAPE or key == pygame.K_p:
            self._events.append(GameEvent.TOGGLE_PAUSE)
        elif key == pygame.K_r:
            self._events.append(GameEvent.RESTART)
        elif key == pygame.K_m:
            self._events.append(GameEvent.TOGGLE_MODE)
        elif key == pygame.K_F11:
            self._events.append(GameEvent.FULLSCREEN)
        elif key == pygame.K_EQUALS or key == pygame.K_KP_PLUS:
            self._events.append(GameEvent.SENSITIVITY_UP)
        elif key == pygame.K_MINUS or key == pygame.K_KP_MINUS:
            self._events.append(GameEvent.SENSITIVITY_DOWN)
        elif key == pygame.K_LEFTBRACKET:
            self._events.append(GameEvent.TARGET_SIZE_DOWN)
        elif key == pygame.K_RIGHTBRACKET:
            self._events.append(GameEvent.TARGET_SIZE_UP)

    @property
    def events(self) -> List[GameEvent]:
        return self._events

    @property
    def raw_mouse_rel(self) -> Tuple[float, float]:
        return self._raw_dx, self._raw_dy

    @property
    def mouse_pos(self) -> Tuple[int, int]:
        return self._mouse_pos

    @property
    def keys_pressed(self) -> set:
        return self._keys_pressed

    def has_event(self, event_type: GameEvent) -> bool:
        return event_type in self._events