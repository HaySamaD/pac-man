from typing import Tuple

import pygame
from pygame import font

from d0_helpers.m0_colors_RGB import Rgb
from d5_display.m0_printer import Printer


class WinPage:

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

        self.p: Printer = Printer(
                                    self.screen,
                                    self.title_font,
                                    self.content_font,
                                    (self.width, self.height)
                                 )

    def print_win_page(self):

        self.p.print_title("Congratulations: You Win", Rgb.GREEN, Rgb.BLACK)

        x: int = -99
        y: int = self.height * 0.17
        self.p.print_text(
                            "Enter your name bellow to save your score",
                            (x, y),
                            Rgb.WHITE,
                            Rgb.BLACK,
                            center_text=True
                         )
