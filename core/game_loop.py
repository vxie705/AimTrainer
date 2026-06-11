import random
from typing import Dict, List, Optional

import pygame

from config import ConfigManager
from game_entities import Crosshair, Target
from input_manager import EventHandler, GameEvent, SensitivityManager
from ui_stats import StatsManager, TextRenderer
from utils import inside_circle

from .fps_manager import FPSManager


class GameLoop:

    def __init__(self) -> None:
        self.config = ConfigManager()
        self.config.load()

        self.fps_manager = FPSManager(self.config.fps_limit)
        self.event_handler = EventHandler()
        self.sensitivity = SensitivityManager(
            self.config.sensitivity_multiplier,
            self.config.sensitivity_invert_y,
        )
        self.stats = StatsManager()
        self.text_renderer = TextRenderer(
            self.config.ui_font_name,
            self.config.ui_font_size,
            self.config.ui_text_color,
            self.config.ui_background_alpha,
        )

        self.screen: Optional[pygame.Surface] = None
        self.running: bool = False
        self.paused: bool = False
        self.game_over: bool = False
        self.current_mode: str = self.config.game_mode_mode

        self.crosshair = Crosshair(
            self.config.crosshair_size,
            self.config.crosshair_thickness,
            self.config.crosshair_color,
            self.config.crosshair_gap,
            self.config.crosshair_dot_radius,
        )

        self.crosshair_x: float = 0.0
        self.crosshair_y: float = 0.0

        self.targets: List[Target] = []
        self._spawn_timer: float = 0.0
        self.current_target_radius: int = self.config.target_radius

        self.targets_remaining: int = self.config.game_mode_total_targets

        self._spawn_times: Dict[int, float] = {}
        self._next_target_id: int = 0

    def initialize(self) -> None:
        pygame.init()

        flags = 0
        if self.config.window_fullscreen:
            flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        else:
            flags = pygame.HWSURFACE | pygame.DOUBLEBUF

        self.screen = pygame.display.set_mode(
            (self.config.window_width, self.config.window_height),
            flags,
        )
        pygame.display.set_caption(self.config.window_title)

        pygame.mouse.set_visible(False)

        self.crosshair_x = self.config.window_width / 2
        self.crosshair_y = self.config.window_height / 2
        pygame.mouse.set_pos((int(self.crosshair_x), int(self.crosshair_y)))

    def run(self) -> None:
        self.initialize()
        self.running = True
        self.reset_game()

        while self.running:
            self.fps_manager.tick()
            dt_ms = self.fps_manager.dt_ms

            self.event_handler.update()
            self._process_events()

            if not self.running:
                break

            if self.paused:
                self._render()
                continue

            raw_dx, raw_dy = self.event_handler.raw_mouse_rel
            dx, dy = self.sensitivity.apply(raw_dx, raw_dy)

            self.crosshair_x += dx
            self.crosshair_y += dy

            w, h = self.config.window_width, self.config.window_height
            self.crosshair_x = max(0, min(self.crosshair_x, w))
            self.crosshair_y = max(0, min(self.crosshair_y, h))

            self._update_targets(dt_ms)

            if not self.game_over:
                self._update_spawner(dt_ms)

            self._cleanup_targets()

            self._render()

    def _process_events(self) -> None:
        for event in self.event_handler.events:
            if event == GameEvent.QUIT:
                self.running = False

            elif event == GameEvent.TOGGLE_PAUSE:
                self.paused = not self.paused

            elif event == GameEvent.RESTART:
                self.reset_game()

            elif event == GameEvent.SHOOT:
                if not self.game_over and not self.paused:
                    self._handle_shot()

            elif event == GameEvent.SENSITIVITY_UP:
                self.sensitivity.multiplier = min(
                    10.0,
                    round(self.sensitivity.multiplier + 0.1, 1),
                )

            elif event == GameEvent.SENSITIVITY_DOWN:
                self.sensitivity.multiplier = max(
                    0.1,
                    round(self.sensitivity.multiplier - 0.1, 1),
                )

            elif event == GameEvent.TARGET_SIZE_UP:
                self.current_target_radius = min(
                    self.config.target_max_radius,
                    self.current_target_radius + 5,
                )

            elif event == GameEvent.TARGET_SIZE_DOWN:
                self.current_target_radius = max(
                    self.config.target_min_radius,
                    self.current_target_radius - 5,
                )

            elif event == GameEvent.TOGGLE_MODE:
                self._toggle_mode()

            elif event == GameEvent.FULLSCREEN:
                self._toggle_fullscreen()

    def _handle_shot(self) -> None:
        self.stats.register_shot()
        hit_something = False

        for target in self.targets:
            if target.is_clickable and inside_circle(
                (self.crosshair_x, self.crosshair_y),
                target.position,
                target.radius,
            ):
                hit_something = True
                spawn_time = self._spawn_times.get(id(target), 0)
                reaction_time = pygame.time.get_ticks() - spawn_time
                self.stats.register_hit(reaction_time)
                target.hit()

                if self.current_mode == "flicking":
                    break

        if (
            not self.config.game_mode_infinite
            and self.current_mode == "flicking"
            and self.stats.total_targets_hit >= self.targets_remaining
        ):
            self.game_over = True

    def _update_targets(self, dt_ms: float) -> None:
        for target in self.targets:
            target.update(dt_ms)

    def _cleanup_targets(self) -> None:
        for target in list(self.targets):
            if target.is_removable:
                if target.state.value == 4:
                    self.stats.register_miss()
                self.targets.remove(target)

    def _update_spawner(self, dt_ms: float) -> None:
        self._spawn_timer += dt_ms

        if self._spawn_timer >= self.config.target_spawn_delay_ms:
            current_count = sum(1 for t in self.targets if t.is_alive)
            if current_count < self.config.target_max_targets:
                self._spawn_target()
            self._spawn_timer = 0.0

    def _spawn_target(self) -> None:
        margin = self.current_target_radius + 20
        w = self.config.window_width
        h = self.config.window_height

        x = random.randint(margin, w - margin)
        y = random.randint(margin, h - margin)

        target = Target(
            x=float(x),
            y=float(y),
            radius=self.current_target_radius,
            color=tuple(self.config.target_color),
            hit_color=tuple(self.config.target_hit_color),
            lifetime_ms=self.config.target_lifetime_ms,
        )

        self.targets.append(target)
        self._spawn_times[id(target)] = pygame.time.get_ticks()
        self.stats.register_target_spawned()

    def reset_game(self) -> None:
        self.targets.clear()
        self._spawn_times.clear()
        self._spawn_timer = 0.0
        self.stats.reset()
        self.game_over = False
        self.paused = False
        self.targets_remaining = self.config.game_mode_total_targets
        self.current_target_radius = self.config.target_radius

        self.crosshair_x = self.config.window_width / 2
        self.crosshair_y = self.config.window_height / 2
        if self.screen:
            pygame.mouse.set_pos((int(self.crosshair_x), int(self.crosshair_y)))

    def _toggle_mode(self) -> None:
        if self.current_mode == "flicking":
            self.current_mode = "tracking"
        else:
            self.current_mode = "flicking"
        self.reset_game()

    def _toggle_fullscreen(self) -> None:
        if self.screen:
            is_full = bool(self.screen.get_flags() & pygame.FULLSCREEN)
            flags = 0 if is_full else (pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
            if not is_full:
                self.screen = pygame.display.set_mode((0, 0), flags)
            else:
                self.screen = pygame.display.set_mode(
                    (self.config.window_width, self.config.window_height),
                    pygame.HWSURFACE | pygame.DOUBLEBUF,
                )

    def _render(self) -> None:
        if self.screen is None:
            return

        self.screen.fill((20, 20, 30))

        for target in self.targets:
            target.draw(self.screen)

        self.crosshair.draw(
            self.screen,
            int(self.crosshair_x),
            int(self.crosshair_y),
        )

        self._render_ui()

        if self.paused:
            self.text_renderer.render_with_background(
                self.screen,
                "PAUSED - Press ESC/P to resume",
                self.config.window_width // 2 - 130,
                self.config.window_height // 2 - 10,
                (255, 255, 0),
            )

        if self.game_over:
            self.text_renderer.render_with_background(
                self.screen,
                f"GAME OVER! Score: {self.stats.score} - Press R to restart",
                self.config.window_width // 2 - 200,
                self.config.window_height // 2 - 10,
                (255, 200, 0),
            )

        pygame.display.flip()

    def _render_ui(self) -> None:
        if self.screen is None:
            return

        lines = self.stats.get_summary_lines()

        lines.insert(0, f"Sens: {self.sensitivity.multiplier:.1f}  "
                     f"TargetSize: {self.current_target_radius}  "
                     f"FPS: {self.fps_manager.current_fps:.0f}")
        lines.insert(0, f"Mode: {self.current_mode.upper()}  "
                     f"({self.targets_remaining - self.stats.total_targets_hit} remaining)")

        self.text_renderer.render_lines(self.screen, lines, 10, 10)

    def shutdown(self) -> None:
        pygame.mouse.set_visible(True)
        pygame.quit()