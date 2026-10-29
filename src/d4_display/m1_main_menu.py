from typing import Any, Tuple

from pygame import font

from ..d0_helpers import Rgb
from ..d0_helpers import MENU
from ..d4_display import Printer


class MainMenuPage:

    def __init__(
                    self,
                    screen: Any,
                    title_font,
                    content_font,
                    resolution
                ) -> None:

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
        # -------------- fill the screen first before printing --------------
        # self.screen.fill(Rgb.BLACK)
        # -------------------------------------------------------------------
        self.p.print_title("Pac-man", Rgb.YELLOW, Rgb.BLACK)
        # -------------------------------------------------------------------
        x: int | float = -99
        y: int | float = self.height * 0.25
        # --------------------------------------------------------------------
        for pos, option_content in enumerate(MENU):
            color: Tuple = Rgb.GREEN if pos == self.pos else Rgb.WHITE
            self.p.print_text(
                                option_content, (x, y), color, Rgb.BLACK, True
                             )
            y += self.height * 0.1
        # -------------------------------------------------------------------
        return None
