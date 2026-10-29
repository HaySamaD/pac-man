from typing import Tuple

import pygame
from pygame import font

from ..d0_helpers import Rgb
from ..d3_parsing_highscores import HigherScore
from ..d4_display import Printer


class HighscoresPage:
    def __init__(
                    self,
                    highscores_obj: HigherScore,
                    screen,
                    title_font,
                    content_font,
                    resolution: Tuple[int, int] = (1920, 1080)
                ) -> None:
        # ------------------ init params ------------------
        self.highscores_obj: HigherScore = highscores_obj
        self.screen = screen
        self.title_font: font.Font = title_font
        self.content_font: font.Font = content_font
        self.width, self.height = resolution
        # ------------------------------------------------------------------
        self.p: Printer = Printer(
                                    self.screen,
                                    self.title_font,
                                    self.content_font,
                                    (self.width, self.height)
                                 )
        # ----------------
        self.pos: int = 0

    # -----------------------------------------------------------------
    def print_highscores_page(self) -> None:
        # -------------------------
        self.screen.fill(Rgb.BLACK)
        # ---------------------------------------------------
        self.p.print_title("Highscores", Rgb.PINK, Rgb.BLACK)
        # ---------------------------------
        x: int | float = -99
        y: int | float = self.height * 0.20
        # -------------------------------------------------------------
        for i in self.highscores_obj.top_10_scores:
            name: str = i.name
            score: int = i.score
            self.p.print_text(
                                f"{name} ----> {score}",
                                (x, y),
                                Rgb.WHITE, Rgb.BLACK, center_text=True
                             )
            y += self.height * 0.05
        # ------------------- print the 'previous' boutton --------------------
        color: Tuple[int, int, int] = Rgb.GREEN if self.pos == 1 else Rgb.WHITE
        # --------------------------------------------------------
        self.p.print_text(
                            "previous",
                            (self.width * 0.8, self.height * 0.8),
                            color,
                            Rgb.BLACK, False
                         )
