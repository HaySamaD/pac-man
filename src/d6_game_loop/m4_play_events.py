"""
    Manages active gameplay events, checking win/loss conditions and pause
                                                                    triggers.
"""

import pygame
from pygame.event import Event

from ..d2_classes import GameState


class PlayEvent:
    """
        Monitors gameplay conditions during active play.

        Attributes:
            game_state (GameState): Active game state instance.
            nbr_levels (int): Total number of game levels.
    """
    def __init__(self, game_state: GameState, nbr_levels: int):
        """
            Initializes play event handler.

            Args:
                game_state (GameState): Game state instance.
                nbr_levels (int): Number of levels.
        """
        # --------------------------------------------------------------------
        self.game_state: GameState = game_state
        self.nbr_levels: int = nbr_levels

    # ========================================================================
    def run_event(self, event: Event) -> None:
        """
            Checks pause triggers, player lives, time left, and level
                                                            completion status.

            Args:
                event (Event): Pygame event object.
        """
        # --------------------------------------------------------------------
        if event.key == pygame.K_ESCAPE:
            self.game_state.status = "PAUSE"
        if self.game_state.time_left <= 0:
            self.game_state.lives -= 1
        if self.game_state.lives <= 0:
            self.game_state.status = "LOSS"
        if self.game_state.level > self.nbr_levels:
            self.game_state.status = "WIN"
        # --------------------------------------------------------------------
        return None
