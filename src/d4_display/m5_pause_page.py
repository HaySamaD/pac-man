"""Renders the pause menu interface."""

from typing import Tuple

from pygame import font
from pygame.surface import Surface

from ..d0_helpers import Rgb
from ..d0_helpers import PAUSE
from .m0_printer import Printer


class PausePage:
    """
        Handles rendering pause menu options and title.

        Attributes:
            screen (Surface): Pygame display surface.
            title_font (font.Font): Title font object.
            content_font (font.Font): Content font object.
            width (int): Screen width.
            height (int): Screen height.
            p (Printer): Printer utility instance.
            pos (int): Current selected pause option index.
    """
    def __init__(
                    self,
                    screen: Surface,
                    title_font: font.Font,
                    content_font: font.Font,
                    resolution: Tuple[int, int]
                ) -> None:
        """
            Initializes pause page layout.

            Args:
                screen (Surface): Target display surface.
                title_font (font.Font): Title font object.
                content_font (font.Font): Content font object.
                resolution (Tuple[int, int]): Screen resolution.
        """
        # ------------------- init params -------------------
        self.screen = screen
        self.title_font = title_font
        self.content_font: font.Font = content_font
        self.width, self.height = resolution
        # ---------------------------------------------------
        self.p: Printer = Printer(
                                    self.screen,
                                    self.title_font,
                                    self.content_font,
                                    (self.width, self.height)
                                 )
        # ---------------------------------------------------
        self.pos: int = 0

    # ==================================================================
    def print_pause_page(self) -> None:
        """Renders pause title and options with selection highlights."""
        # --------------------------------------------------------------
        self.p.print_title("Pause", Rgb.GREEN, Rgb.BLACK)
        # --------------------------------------------------------------
        x: int | float = -99
        y: int | float = self.height * 0.18
        # --------------------------------------------------------------
        for idx, option in enumerate(PAUSE):
            color: Tuple = Rgb.YELLOW if idx == self.pos else Rgb.WHITE
            self.p.print_text(option, (x, y), color, Rgb.BLACK, True)
            y += self.height * 0.08
        # --------------------------------------------------------------
        return None
