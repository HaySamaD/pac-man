"""Renders the main menu interface with navigation options."""

from typing import Any, Tuple

from pygame import font

from ...d1_helpers import Rgb
from ...d1_helpers import MENU
from .. import Printer


class MainPage:
    """
        Handles rendering and navigation state of the main menu.

        Attributes:
            screen (Any): Pygame display surface.
            title_font (font.Font): Font for the main title.
            content_font (font.Font): Font for menu items.
            width (int): Screen width.
            height (int): Screen height.
            p (Printer): Printer utility instance.
            pos (int): Current selected menu option index.
    """

    def __init__(
                    self,
                    screen: Any,
                    title_font: font.Font,
                    content_font: font.Font,
                    resolution: Tuple[int, int]
                ) -> None:
        """
            Initializes main page layout and printer utility.

            Args:
                screen (Any): Target display surface.
                title_font (font.Font): Title font object.
                content_font (font.Font): Content font object.
                resolution (Tuple[int, int]): Screen dimensions.
        """

        # ------------------- init params -------------------
        self.screen = screen
        self.title_font: font.Font = title_font
        self.content_font: font.Font = content_font
        self.width, self.height = resolution
        # ---------------- the printer class ----------------
        self.p: Printer = Printer(
                                    self.screen,
                                    self.title_font,
                                    self.content_font,
                                    (self.width, self.height)
                                 )
        # ----- the selected option now is 'Start Game' -----
        self.pos: int = 0

    # ========================================================================
    def print_main_menu(self) -> None:
        """
            Clears screen and renders the main menu options with selection
                                                                    highlights.
        """
        # -------------- fill the screen first before printing ---------------
        self.screen.fill(Rgb.BLACK)
        # --------------------------------------------------------------------
        self.p.print_title("Pac-man", Rgb.YELLOW, Rgb.BLACK)
        # --------------------------------------------------------------------
        x: int | float = -99
        y: int | float = self.height * 0.25
        # --------------------------------------------------------------------
        for pos, option_content in enumerate(MENU):
            color: Tuple = Rgb.GREEN if pos == self.pos else Rgb.WHITE
            self.p.print_text(
                                option_content, (x, y), color, Rgb.BLACK, True
                             )
            y += self.height * 0.1
        # --------------------------------------------------------------------
        return None
