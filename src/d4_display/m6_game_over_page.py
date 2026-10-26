from typing import Tuple

import pygame
from pygame import font

from ..d0_helpers import Rgb
from ..d4_display import Printer


class GameOverPage:
    def __init__(self, resolution: Tuple[int, int]) -> None:
        # ----------- init params -----------
        self.width, self.height = resolution
        # ------------------------ init pygame -------------------------
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        # ---------------------- init fonts ----------------------
        self.title_font: font.Font = pygame.font.Font(None, 100)
        self.content_font: font.Font = pygame.font.Font(None, 40)
        # ----------------------------------------------------
        self.p: Printer = Printer(
                                    self.screen,
                                    self.title_font,
                                    self.content_font,
                                    (self.width, self.height)
                                 )

    # -------------------------------------------------------------------
    def print_game_over_page(self) -> None:
        # ---------------------------------------------------------------
        self.p.print_title("Game Over: Try again", Rgb.ORANGE, Rgb.BLACK)
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
        # ---------
        return None
