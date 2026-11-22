"""Renders the game instructions and control guidelines screen."""

from typing import Tuple

from pygame import font
from pygame.surface import Surface

from ...d1_helpers import Rgb
from ...d1_helpers import INSTRUCTIONS
from .. import Printer


class InstructionsPage:
    """
        Handles rendering instructions text and navigation options.

        Attributes:
            screen (Surface): Pygame display surface.
            title_font (font.Font): Font for the title.
            content_font (font.Font): Font for instructions content.
            width (int): Screen width.
            height (int): Screen height.
            p (Printer): Printer utility instance.
            pos (int): Current selected navigation option.
    """
    def __init__(
                    self,
                    screen: Surface,
                    title_font: font.Font,
                    content_font: font.Font,
                    p: Printer,
                    resolution: Tuple[int, int] = (1920, 1080)
                ) -> None:
        """
            Initializes instructions page layout.

            Args:
                screen (Surface): Target display surface.
                title_font (font.Font): Title font object.
                content_font (font.Font): Content font object.
                resolution (Tuple[int, int]): Screen resolution.
        """
        # ------------------- init params -------------------
        self.screen = screen
        self.title_font: font.Font = title_font
        self.content_font: font.Font = content_font
        self.p: Printer = p
        self.width, self.height = resolution
        # ---------------------------------------------------
        self.pos: int = 0

    # =========================================================================
    def print_instruction_page(self) -> None:
        """Renders formatted instruction guidelines and previous button."""
        # -------------- fill the screen first before printing ----------------
        self.screen.fill(Rgb.BLACK)
        # ---------------------------------------------------------------------
        self.p.print_title("Instructions", Rgb.RED, Rgb.BLACK)
        # ---------------------------------------------------------------------
        x: int | float = self.width * 0.05
        y: int | float = self.height * 0.15
        # ---------------------------------------------------------------------
        for i in INSTRUCTIONS:
            if i.startswith(("1", "2", "3", "4", "5")):
                y += self.height * 0.06
            elif i.startswith((" -", "-")):
                y += self.height * 0.03
            else:
                y += self.height * 0.0128
            self.p.print_text(i, (x, y), Rgb.WHITE, Rgb.BLACK, False)

        # ------------------ print the 'previous' boutton ---------------------
        color: Tuple[int, int, int] = Rgb.GREEN if self.pos == 1 else Rgb.WHITE
        # ---------------------------------------------------------------------
        self.p.print_text(
                            "previous",
                            (self.width * 0.8, self.height * 0.8),
                            color,
                            Rgb.BLACK, False
                         )
