from typing import Tuple

import pygame
from pygame import font

from d0_helpers.m0_colors_RGB import Rgb
from d3_parsing_highscores.m2_highscores_system import HighScoreSys
from d5_display.m0_printer import Printer


class HighscoresPage:
    def __init__(
                    self,
                    highscores_obj: HighScoreSys,
                    resolution: Tuple[int, int] = (1920, 1080)
                ) -> None:

        # ----------- init params -----------
        self.highscores_obj: HighScoreSys = highscores_obj
        self.width, self.height = resolution

        # ------------------------ init pygame -------------------------
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # ---------------------- init fonts ----------------------
        self.title_font: font.Font = pygame.font.Font(None, 135)
        self.content_font: font.Font = pygame.font.Font(None, 50)

        # ----------------
        self.pos: int = 0

        # ------------------------------------------------------------------
        self.p: Printer = Printer(
                                    self.screen,
                                    self.title_font,
                                    self.content_font,
                                    (self.width, self.height)
                                 )

    # -----------------------------------------------------------------
    def print_highscores_page(self) -> None:

        self.screen.fill(Rgb.BLACK)

        self.p.print_title("Highscores", Rgb.PINK, Rgb.BLACK)

        x: int = -99
        y: int = self.height * 0.20
        for i in self.highscores_obj:

            name: str = i.name
            score: int = i.score

            self.p.print_text(
                                f"{name} ----> {score}",
                                (x, y),
                                Rgb.WHITE, Rgb.BLACK, center_text=True
                             )

            y += self.height * 0.05

        # ----------------- print the 'previous' boutton ------------------
        color: Tuple[int, int] = Rgb.GREEN if self.pos == 1 else Rgb.WHITE

        self.p.print_text(
                            "previous",
                            (self.width * 0.8, self.height * 0.8),
                            color,
                            Rgb.BLACK, False
                         )
