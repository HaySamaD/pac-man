import pygame
from pygame.event import Event

from ..d1_classes import GameState

from ..d4_display import PauseMenuPage


class PauseEvent:
    def __init__(
                    self, pause_obj: PauseMenuPage, game_state: GameState
                ) -> None:
        # ----------------------------------------
        self.pause_obj: PauseMenuPage = pause_obj
        self.game_state: GameState = game_state

    def run_event(self, event: Event):
        # ---------------------------------------
        if event.key == pygame.K_DOWN:
            self.pause_obj.pos += 1
            if self.pause_obj.pos > 1:
                self.pause_obj.pos = 0
        elif event.key == pygame.K_UP:
            self.pause_obj.pos -= 1
            if self.pause_obj.pos < 0:
                self.pause_obj.pos = 1
        elif event.key == pygame.K_RETURN:
            if self.pause_obj.pos == 0:
                self.game_state.status = "PLAY"
            elif self.pause_obj.pos == 1:
                self.game_state.status = "MENU"
        # ----------
        return None
