from typing import Tuple

import pygame
from pygame import font

from ..d0_helpers import Rgb
from ..d4_display import Printer


class WinPage:

    def __init__(
                    self,
                    screen,
                    title_font,
                    content_font,
                    resolution: Tuple[int, int]
                ) -> None:

        # -------------- init params ---------------
        self.screen = screen
        self.title_font: font.Font = title_font
        self.content_font: font.Font = content_font
        self.width, self.height = resolution
        # ----------------------------------------------------
        self.p: Printer = Printer(
                                    self.screen,
                                    self.title_font,
                                    self.content_font,
                                    (self.width, self.height)
                                 )

    # ----------------------------------------------------------------------
    def print_win_page(self) -> None:
        # ------------------------------------------------------------------
        self.p.print_title("Congratulations: You Win", Rgb.GREEN, Rgb.BLACK)
        # ----------------------------------
        x: int | float = -99
        y: int | float = self.height * 0.17
        # --------------------------------------------------------------
        self.p.print_text(
                            "Enter your name bellow to save your score",
                            (x, y),
                            Rgb.WHITE,
                            Rgb.BLACK,
                            center_text=True
                         )
        # ----------
        return None
