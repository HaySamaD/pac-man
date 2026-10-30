from .m6_win_loss_events import WinLossEvent

from .m5_pause_events import PauseEvent

from .m4_play_events import PlayEvent

from .m3_instructions_events import InstructionsEvents

from .m2_highscores_events import HighScoresEvent

from .m1_menu_events import MenuEvent

from ..d4_display import (
                            Printer, MainPage, HighscoresPage,
                            InstructionsPage, HUD, PausePage,
                            LossPage, WinPage
                         )
from ..d1_classes import GameState

from ..d3_parsing_highscores import HigherScore

import pygame

from typing import Tuple

from ..d0_helpers import Rgb


class GameLoop:
    def __init__(
                    self,
                    highscores_obj: HigherScore,
                    game_state: GameState,
                    nbr_levels: int,
                    resolution: Tuple[int, int] = (1920, 1080)
                ) -> None:
        # ----------------- init params -----------------
        self.highscores_obj: HigherScore = highscores_obj
        self.game_state: GameState = game_state
        self.nbr_levels = nbr_levels
        self.width, self.height = resolution

    # =========================================================================
    def game_loop(self) -> None:
        # ---------------------------- init pygame ----------------------------
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()
        # ---------------------------- init fonts -----------------------------
        title_font = pygame.font.Font(None, 135)
        content_font = pygame.font.Font(None, 50)
        # --------------------------- printer text ----------------------------
        p: Printer = Printer(
                                screen,
                                title_font,
                                content_font,
                                (self.width, self.height)
                            )
        # ----------------------------------------------------------------------
        main_page: MainPage = MainPage(
                    screen, title_font, content_font, (self.width, self.height)
                                      )
        higher_score_page: HighscoresPage = HighscoresPage(
                        self.highscores_obj, screen, title_font, content_font
                                                          )
        instruction_page: InstructionsPage = InstructionsPage(
                    screen, title_font, content_font, (self.width, self.height)
                                                            )
        hud: HUD = HUD(
                        self.game_state, screen, title_font, content_font,
                        (self.width, self.height)
                      )
        pause_page: PausePage = PausePage(
                    screen, title_font, content_font, (self.width, self.height)
                                         )
        loss_page: LossPage = LossPage(
                    screen, title_font, content_font, (self.width, self.height)
                                      )
        win_page: WinPage = WinPage(
                    screen, title_font, content_font, (self.width, self.height)
                                   )
        # ----------------------------------------------------------------------
        menu_event_obj: MenuEvent = MenuEvent(main_page, self.game_state)
        highscore_event_obj: HighScoresEvent = HighScoresEvent(
                                            self.game_state, higher_score_page
                                                              )
        instruction_event_obj: InstructionsEvents = InstructionsEvents(
                                            instruction_page, self.game_state
                                                                      )
        play_event_obj: PlayEvent = PlayEvent(self.game_state, self.nbr_levels)
        pause_event_obj: PauseEvent = PauseEvent(pause_page, self.game_state)
        win_loss_event: WinLossEvent = WinLossEvent(
                        self.highscores_obj, p, self.game_state, self.height
                                                   )
        # ----------------------------------------------------------------------
        running: bool = True
        player_name: str = ""
        while running:
            screen.fill(Rgb.BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_state.status == "MENU":
                        running = menu_event_obj.run_event(event, running)
                    elif self.game_state.status == "HIGHSCORES":
                        highscore_event_obj.run_events(event)
                    elif self.game_state.status == "INSTRUCTIONS":
                        instruction_event_obj.run_events(event)
                    elif self.game_state.status == "PLAY":
                        play_event_obj.run_event(event)
                    elif self.game_state.status == "PAUSE":
                        pause_event_obj.run_event(event)
                    elif self.game_state.status in ["LOSS", "WIN"]:
                        player_name = win_loss_event.run_event(event)
            if self.game_state.status == "MENU":
                main_page.print_main_menu()
            elif self.game_state.status == "HIGHSCORES":
                higher_score_page.print_highscores_page()
            elif self.game_state.status == "INSTRUCTIONS":
                instruction_page.print_instruction_page()
            elif self.game_state.status == "PLAY":
                hud.print_hud()
            elif self.game_state.status == "PAUSE":
                pause_page.print_pause_page()
            elif self.game_state.status == "LOSS":
                loss_page.print_game_over_page()
                p.print_text(
                                f"Your score is: {self.game_state.score}",
                                (-99, self.height * 0.25),
                                Rgb.WHITE,
                                Rgb.BLACK,
                                True
                            )
                p.print_text(
                                player_name,
                                (-99, self.height * 0.35),
                                Rgb.GREEN,
                                Rgb.BLACK,
                                True
                            )
            elif self.game_state.status == "WIN":
                win_page.print_win_page()
                p.print_text(
                                f"Your score is: {self.game_state.score}",
                                (-99, self.height * 0.25),
                                Rgb.WHITE,
                                Rgb.BLACK,
                                True
                            )
                p.print_text(
                                player_name,
                                (-99, self.height * 0.35),
                                Rgb.GREEN,
                                Rgb.BLACK,
                                True
                            )
            clock.tick(60)
            pygame.display.update()
        # ------------------------------------------------------------------
        pygame.quit()


"""
    links:
    - game loop: https://www.pygame.fr/en/bb-01-game-loop/
    - using Font for text: https://www.geeksforgeeks.org/python/python-display-text-to-pygame-window/
    - using clock for FPS: https://gamedevacademy.org/pygame-fps-tutorial/
    - print a text in pygame: https://gamedevacademy.org/display-text-pygame-tutorial-complete-guide/
"""
