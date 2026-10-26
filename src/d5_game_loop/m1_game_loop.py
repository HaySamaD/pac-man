from ..d4_display import (
                            Printer, m1_main_menu, m2_highscore_page,
                            m3_instruction_page, m4_hud, m5_pause_menu_page,
                            m6_game_over_page, m7_win_page
                         )
from ..d1_classes import m0_pydantic_classes, m1_dataclasses
from ..d0_helpers import m1_helpers_read

import pygame

from typing import Tuple


class GameLoop:
    def __init__(self, resolution: Tuple[int, int] = (1920, 1080)):
        # init params
        self.width, self.height = resolution

    # --------------------------
    def game_loop(self) -> None:
        # -----------
        pygame.init()
        # ------ display the window (width and height------
        pygame.display.set_mode((self.width, self.height))
        # -- display the name of the window --
        pygame.display.set_caption("PAC-MAN")
        # ------------------
        running: bool = True
        # ---------------------------------------
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
