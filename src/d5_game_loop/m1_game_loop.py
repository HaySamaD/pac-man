from ..d4_display import (
                            Printer, MainMenuPage, HighscoresPage,
                            InstructionsPage, HUD, PauseMenuPage,
                            GameOverPage, WinPage
                         )
from ..d1_classes import GameState

from ..d3_parsing_highscores import HighScoreSys

import pygame

from typing import Tuple


class GameLoop:
    def __init__(
                    self,
                    highscores_obj: HighScoreSys,
                    game_state: GameState,
                    resolution: Tuple[int, int] = (1920, 1080)
                ) -> None:
        # ----------- init params -------------------------
        self.highscores_obj: HighScoreSys = highscores_obj
        self.game_state: GameState = game_state
        self.width, self.height = resolution

    # --------------------------
    def game_loop(self) -> None:
        # ---------------------- init pygame ----------------------
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()
        # ------------- init fonts -------------
        title_font = pygame.font.Font(None, 135)
        content_font = pygame.font.Font(None, 50)
        # -------------------------------------------------------------------
        menu_obj: MainMenuPage = MainMenuPage(
                                                screen,
                                                title_font,
                                                content_font
                                                (self.width, self.height)
                                             )
        h_score_obj: HighscoresPage = HighscoresPage(
                                                        self.highscores_obj,
                                                        screen
                                                    )
        inst_obj: InstructionsPage = InstructionsPage(
                                                    screen,
                                                    title_font,
                                                    content_font,
                                                    (self.width, self.height)
                                                     )
        hud_obj: HUD = HUD(
                            self.game_state,
                            screen,
                            title_font,
                            content_font,
                            (self.width, self.height)
                          )
        pause_obj: PauseMenuPage = PauseMenuPage(
                                                    screen,
                                                    title_font,
                                                    content_font,
                                                    (self.width, self.height)
                                                )
        gm_ovr_obj: GameOverPage = GameOverPage(
                                        screen,
                                        title_font,
                                        content_font,
                                        (self.width, self.height)
                                    )
        win_obj: WinPage = WinPage(
                                    screen,
                                    title_font,
                                    content_font,
                                    (self.width, self.height)
                                  )
        # -------------------------------------------------
        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    pass
            clock.tick(60)


"""
    links:
    - using font for tetx: https://www.geeksforgeeks.org/python/python-display-text-to-pygame-window/
    - using clock for FPS: https://gamedevacademy.org/pygame-fps-tutorial/
"""
