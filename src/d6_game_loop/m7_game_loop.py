"""
    Core game loop orchestrator managing Pygame initialization, screen updates,
                                                            and event routing.
"""

from typing import Tuple

from .m1_menu_events import MenuEvent
from .m2_highscores_events import HighScoresEvent
from .m3_instructions_events import InstructionsEvents
from .m4_play_events import PlayEvent
from .m5_pause_events import PauseEvent
from .m6_win_loss_events import WinLossEvent

from ..d1_helpers import Rgb
from ..d2_classes import Config, GameState
from ..d4_parsing_highscores import HigherScore
from ..d5_display import (
                            Printer, MainPage, HighscoresPage,
                            InstructionsPage, HUD, PausePage,
                            LossPage, WinPage, Gameplay
                         )

import pygame


class GameLoop:
    """
        Manages main application execution, display rendering, and state
                                                                    dispatching.

        Attributes:
            highscores_obj (HigherScore): Highscore management instance.
            game_state (GameState): Active game state instance.
            nbr_levels (int): Total number of game levels.
            width (int): Screen width resolution.
            height (int): Screen height resolution.
    """
    def __init__(
                    self,
                    config: Config,
                    highscores_obj: HigherScore,
                    game_state: GameState,
                    nbr_levels: int,
                    resolution: Tuple[int, int]
                ) -> None:
        """
            Initializes game loop controller with configuration and state
                                                                    objects.

            Args:
                highscores_obj (HigherScore): Highscore manager instance.
                game_state (GameState): Game state instance.
                nbr_levels (int): Number of levels.
                resolution (Tuple[int, int]): Window resolution width and
                                                                        height.
        """
        # ----------------------- init params --------------------------
        self.config: Config = config
        self.highscores_obj: HigherScore = highscores_obj
        self.game_state: GameState = game_state
        self.nbr_levels = nbr_levels
        self.width, self.height = resolution
        # ------------------------ init pygame -------------------------
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        # ------------------------- init font --------------------------
        self.title_font = pygame.font.Font(None, 135)
        self.content_font = pygame.font.Font(None, 35)
        # ----------- load the instructions image ------------
        self.image = pygame.image.load(
                                "assets/instructions/instructions.jpeg"
                                      )
        # --------------------- the printer object ---------------------
        self.p: Printer = Printer(
                                    self.screen,
                                    self.title_font,
                                    self.content_font,
                                    (self.width, self.height)
                                 )

    # =========================================================================
    def game_loop(self) -> None:
        """
            Runs the main application execution loop, handling events and
            rendering active pages at 60 FPS.
        """
        # ---------------------- the pages of each menu -----------------------
        main_page: MainPage = MainPage(
                                        self.screen,
                                        self.title_font,
                                        self.content_font,
                                        self.p,
                                        (self.width, self.height)
                                      )
        higher_score_page: HighscoresPage = HighscoresPage(
                                                    self.highscores_obj,
                                                    self.screen,
                                                    self.title_font,
                                                    self.content_font,
                                                    self.p,
                                                    (self.width, self.height)
                                                          )
        instruction_page: InstructionsPage = InstructionsPage(
                                                    self.screen,
                                                    self.title_font,
                                                    self.content_font,
                                                    self.p,
                                                    self.image,
                                                    (self.width, self.height)
                                                             )
        hud: HUD = HUD(
                        self.game_state,
                        self.screen,
                        self.title_font,
                        self.content_font,
                        self.p,
                        (self.width, self.height)
                      )
        pause_page: PausePage = PausePage(
                                            self.screen,
                                            self.title_font,
                                            self.content_font,
                                            self.p,
                                            (self.width, self.height)
                                         )
        loss_page: LossPage = LossPage(
                                        self.screen,
                                        self.title_font,
                                        self.content_font,
                                        self.game_state,
                                        self.p,
                                        (self.width, self.height)
                                      )
        win_page: WinPage = WinPage(
                                    self.screen,
                                    self.title_font,
                                    self.content_font,
                                    self.game_state,
                                    self.p,
                                    (self.width, self.height)
                                   )
        gameplay_page: Gameplay = Gameplay(
                                            self.screen,
                                            self.config,
                                            self.game_state
                                          )
        # ----------------- the events objects for each page ------------------
        menu_event_obj: MenuEvent = MenuEvent(main_page, self.game_state)
        highscore_event_obj: HighScoresEvent = HighScoresEvent(
                                                            self.game_state,
                                                            higher_score_page
                                                              )
        instruction_event_obj: InstructionsEvents = InstructionsEvents(
                                                            instruction_page,
                                                            self.game_state
                                                                      )
        play_event_obj: PlayEvent = PlayEvent(self.game_state, self.nbr_levels)
        pause_event_obj: PauseEvent = PauseEvent(pause_page, self.game_state)
        win_loss_event: WinLossEvent = WinLossEvent(
                                                    self.highscores_obj,
                                                    self.game_state,
                                                    self.height
                                                   )
        # ---------------------------------------------------------------------
        running: bool = True
        player_name: str = ""
        while running:
            self.screen.fill(Rgb.BLACK)
            # ------------------------ the events ------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.game_state.status == "MENU":
                        running = menu_event_obj.run_event(event, running)
                    elif self.game_state.status == "HIGHSCORES":
                        highscore_event_obj.run_events(event)
                    elif self.game_state.status == "INSTRUCTIONS":
                        instruction_event_obj.run_events(event)
                    elif self.game_state.status == "PLAY":
                        play_event_obj.run_event(event)
                        gameplay_page.handle_event(event)
                    elif self.game_state.status == "PAUSE":
                        pause_event_obj.run_event(event, gameplay_page)
                    elif self.game_state.status in ["LOSS", "WIN"]:
                        player_name = win_loss_event.run_event(event)
            # ------------------ print pages ------------------
            if self.game_state.status == "MENU":
                main_page.print_main_menu()
            elif self.game_state.status == "HIGHSCORES":
                higher_score_page.print_highscores_page()
            elif self.game_state.status == "INSTRUCTIONS":
                instruction_page.print_instruction_page()
            elif self.game_state.status == "PLAY":
                gameplay_page.update_and_render()
                hud.print_hud()
            elif self.game_state.status == "PAUSE":
                pause_page.print_pause_page()
            elif self.game_state.status == "LOSS":
                loss_page.print_loss_page()
                self.p.print_text(
                                    player_name,
                                    (-99, self.height * 0.35),
                                    Rgb.GREEN,
                                    Rgb.BLACK,
                                    center_text=True
                                 )
            elif self.game_state.status == "WIN":
                win_page.print_win_page()
                self.p.print_text(
                                    player_name,
                                    (-99, self.height * 0.35),
                                    Rgb.GREEN,
                                    Rgb.BLACK,
                                    center_text=True
                                 )
            # ---------------------
            self.clock.tick(60)
            pygame.display.update()
        # ------------------------------------------------------------------
        pygame.quit()
