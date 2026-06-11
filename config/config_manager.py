import json
import os
from typing import Any, Dict


class ConfigManager:

    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls) -> "ConfigManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self, filepath: str = "resources/config.json") -> None:
        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"No se encontró el archivo de configuración: {filepath}"
            )
        with open(filepath, "r", encoding="utf-8") as f:
            self.__class__._config = json.load(f)

    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.split(".")
        value: Any = self.__class__._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    @property
    def window_width(self) -> int:
        return self.get("window.width", 800)

    @property
    def window_height(self) -> int:
        return self.get("window.height", 600)

    @property
    def window_title(self) -> str:
        return self.get("window.title", "Aim Trainer")

    @property
    def window_fullscreen(self) -> bool:
        return self.get("window.fullscreen", False)

    @property
    def fps_limit(self) -> int:
        return self.get("window.fps", 240)

    @property
    def sensitivity_multiplier(self) -> float:
        return self.get("sensitivity.multiplier", 1.0)

    @property
    def sensitivity_invert_y(self) -> bool:
        return self.get("sensitivity.invert_y", False)

    @property
    def sensitivity_raw_input(self) -> bool:
        return self.get("sensitivity.raw_input", True)

    @property
    def target_radius(self) -> int:
        return self.get("target.radius", 30)

    @property
    def target_min_radius(self) -> int:
        return self.get("target.min_radius", 15)

    @property
    def target_max_radius(self) -> int:
        return self.get("target.max_radius", 50)

    @property
    def target_color(self) -> list:
        return self.get("target.color", [255, 50, 50])

    @property
    def target_hit_color(self) -> list:
        return self.get("target.hit_color", [50, 255, 50])

    @property
    def target_lifetime_ms(self) -> int:
        return self.get("target.lifetime_ms", 2000)

    @property
    def target_spawn_delay_ms(self) -> int:
        return self.get("target.spawn_delay_ms", 500)

    @property
    def target_max_targets(self) -> int:
        return self.get("target.max_targets", 1)

    @property
    def crosshair_size(self) -> int:
        return self.get("crosshair.size", 20)

    @property
    def crosshair_thickness(self) -> int:
        return self.get("crosshair.thickness", 2)

    @property
    def crosshair_color(self) -> list:
        return self.get("crosshair.color", [0, 255, 0])

    @property
    def crosshair_gap(self) -> int:
        return self.get("crosshair.gap", 4)

    @property
    def crosshair_dot_radius(self) -> int:
        return self.get("crosshair.dot_radius", 2)

    @property
    def game_mode_mode(self) -> str:
        return self.get("game_mode.mode", "flicking")

    @property
    def game_mode_total_targets(self) -> int:
        return self.get("game_mode.total_targets", 30)

    @property
    def game_mode_infinite(self) -> bool:
        return self.get("game_mode.infinite", False)

    @property
    def ui_font_name(self) -> str | None:
        return self.get("ui.font_name", None)

    @property
    def ui_font_size(self) -> int:
        return self.get("ui.font_size", 18)

    @property
    def ui_text_color(self) -> list:
        return self.get("ui.text_color", [255, 255, 255])

    @property
    def ui_background_alpha(self) -> int:
        return self.get("ui.background_alpha", 128)