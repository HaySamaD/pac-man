import pygame
from pygame.event import Event

from ..d4_display import HighscoresPage

from ..d1_classes import GameState


class HighScoresEvent:
    def __init__(self, game_status: GameState, h_score_obj: HighscoresPage):
        # ------------- init params -------------
        self.game_status: GameState = game_status
        self.h_score_obj: HighscoresPage = h_score_obj

    def run_events(self, event: Event) -> None:
        # ---------------------------------------
        if event.key == pygame.K_DOWN:
            self.h_score_obj.pos += 1
            if self.h_score_obj.pos > 1:
                self.h_score_obj.pos = 0
        elif event.key == pygame.K_UP:
            self.h_score_obj.pos -= 1
            if self.h_score_obj.pos < 0:
                self.h_score_obj.pos = 1
        elif event.key == pygame.K_RETURN:
            if self.h_score_obj.pos == 1:
                self.game_status.status = "MENU"
        # ---------
        return None
