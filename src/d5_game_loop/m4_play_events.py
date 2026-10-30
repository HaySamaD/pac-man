import pygame
from pygame.event import Event

from ..d1_classes import GameState


class PlayEvent:
    def __init__(self, game_state: GameState, nbr_levels: int):
        # --------------------------------------
        self.game_state: GameState = game_state
        self.nbr_levels: int = nbr_levels

    def run_event(self, event: Event):
        # ----------------------------------------------------------------
        if event.key == pygame.K_ESCAPE:
            self.game_state.status = "PAUSE"
        elif self.game_state.lives <= 0 or self.game_state.time_left <= 0:
            self.game_state.status = "LOSS"
        elif self.game_state.level > self.nbr_levels:
            self.game_state.status = "WIN"
        # ----------
        return None
