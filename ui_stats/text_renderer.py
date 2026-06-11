from typing import List, Optional, Tuple

import pygame


class TextRenderer:

    def __init__(
        self,
        font_name: Optional[str] = None,
        font_size: int = 18,
        text_color: Tuple[int, int, int] = (255, 255, 255),
        background_alpha: int = 128,
    ) -> None:
        self.font_name = font_name
        self.font_size = font_size
        self.text_color = text_color
        self.background_alpha = background_alpha
        self._font: Optional[pygame.font.Font] = None

    def _ensure_font(self) -> None:
        if self._font is not None:
            return
        try:
            if self.font_name:
                self._font = pygame.font.Font(self.font_name, self.font_size)
            else:
                self._font = pygame.font.Font(None, self.font_size)
        except Exception:
            self._font = pygame.font.Font(None, self.font_size)

    def set_font_size(self, size: int) -> None:
        self.font_size = size
        self._font = None

    def render_line(
        self,
        screen: pygame.Surface,
        text: str,
        x: int,
        y: int,
        color: Optional[Tuple[int, int, int]] = None,
    ) -> None:
        self._ensure_font()
        if self._font is None:
            return
        c = color if color else self.text_color
        surface = self._font.render(text, True, c)
        screen.blit(surface, (x, y))

    def render_lines(
        self,
        screen: pygame.Surface,
        lines: List[str],
        x: int,
        y: int,
        line_spacing: int = 22,
        color: Optional[Tuple[int, int, int]] = None,
    ) -> None:
        for i, line in enumerate(lines):
            self.render_line(screen, line, x, y + i * line_spacing, color)

    def render_with_background(
        self,
        screen: pygame.Surface,
        text: str,
        x: int,
        y: int,
        color: Optional[Tuple[int, int, int]] = None,
        bg_color: Tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        self._ensure_font()
        if self._font is None:
            return
        c = color if color else self.text_color
        text_surface = self._font.render(text, True, c)
        bg = pygame.Surface(
            (text_surface.get_width() + 10, text_surface.get_height() + 6),
            pygame.SRCALPHA,
        )
        bg.fill((*bg_color, self.background_alpha))
        screen.blit(bg, (x - 5, y - 3))
        screen.blit(text_surface, (x, y))