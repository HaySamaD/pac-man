import pygame

from pygame.event import Event

from ..d1_classes.m1_dataclasses import GameState
from ..d4_display.m1_main_page import MainPage


class MenuEvent:
    def __init__(
                    self,
                    main_obj: MainPage,
                    game_state: GameState,
                ) -> None:
        # ------------ init params -------------
        self.main_obj: MainPage = main_obj
        self.game_state: GameState = game_state

    # =======================================================
    def run_event(self, event: Event, running: bool) -> bool:
        # ----------------------------------------------
        if event.key == pygame.K_DOWN:
            self.main_obj.pos += 1
            if self.main_obj.pos > 3:
                self.main_obj.pos = 0
        elif event.key == pygame.K_UP:
            self.main_obj.pos -= 1
            if self.main_obj.pos < 0:
                self.main_obj.pos = 3
        elif event.key == pygame.K_RETURN:
            if self.main_obj.pos == 0:
                self.game_state.status = "PLAY"
            elif self.main_obj.pos == 1:
                self.game_state.status = "HIGHSCORES"
            elif self.main_obj.pos == 2:
                self.game_state.status = "INSTRUCTIONS"
            elif self.main_obj.pos == 3:
                running = False
        # ----------------------------------------------
        return running
