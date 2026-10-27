from typing import Tuple

import pygame
from pygame import font

from ..d0_helpers import Rgb
from ..d0_helpers import PAUSE
from ..d4_display import Printer


class PauseMenuPage:
    def __init__(
                    self,
                    screen,
                    title_font,
                    content_font,
                    resolution: Tuple[int, int]
                ) -> None:
        # ------------------------- init params -------------------------
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
        # ----------------
        self.pos: int = 0

    # ----------------------------------------------------------------------------
    def print_pause_page(self) -> None:
        # -----------------------------------------------
        self.p.print_title("Pause", Rgb.GREEN, Rgb.BLACK)
        # ----------------------------------
        x: int | float = -99
        y: int | float = self.height * 0.18
        # --------------------------------------------------------------
        for idx, option in enumerate(PAUSE):
            color: Tuple = Rgb.YELLOW if idx == self.pos else Rgb.WHITE
            self.p.print_text(option, (x, y), color, Rgb.BLACK, True)
            y += self.height * 0.08
        # ----------
        return None
