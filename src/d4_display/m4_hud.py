from typing import Tuple

import pygame
from pygame import font

from ..d0_helpers import Rgb
from ..d1_classes import GameState
from ..d4_display import Printer


class HUD:
    def __init__(
                    self, game_state: GameState, resolution: Tuple[int, int]
                ) -> None:

        # ------------- init params -------------
        self.game_state: GameState = game_state
        self.width, self.height = resolution
        # ------------------------ init pygame -------------------------
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        # ---------------------- init fonts ----------------------
        self.title_font: font.Font = pygame.font.Font(None, 100)
        self.content_font: font.Font = pygame.font.Font(None, 40)
        # ---------------------------------------------------
        self.p: Printer = Printer(
                                    self.screen,
                                    self.title_font,
                                    self.content_font,
                                    (self.width, self.height)
                                 )

    # -------------------------------------------------------------------
    def print_hud(self) -> None:
        # ----------------------------------------
        score: int = self.game_state.score
        lives: int = self.game_state.lives
        level: int = self.game_state.level
        time_left: int = self.game_state.time_left
        # -----------------------------------
        x: int | float = self.width * 0.20
        y: int | float = self.height * 0.025
        # --------------------------------------------------------------
        self.p.print_text(
                            (
                                f"Score: {score}                      "
                                f"Lives: {lives}                      "
                                f"Level: {level}                      "
                                f"Time left: {time_left}"
                            ),
                            (x, y),
                            Rgb.WHITE,
                            Rgb.BLACK,
                            False
                         )
        # ----------
        return None
