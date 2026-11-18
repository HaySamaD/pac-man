"""Handles keyboard event management and navigation for the game pause menu."""

import pygame
from pygame.event import Event

from ..d2_classes import GameState

from ..d5_display import PausePage


class PauseEvent:
    """
        Manages pause menu option selection and state transitions.

        Attributes:
            pause_obj (PausePage): Pause page display instance.
            game_state (GameState): Active game state instance.
    """
    def __init__(
                    self, pause_obj: PausePage, game_state: GameState
                ) -> None:
        """
            Initializes pause event handler.

            Args:
                pause_obj (PausePage): Pause page instance.
                game_state (GameState): Game state instance.
        """
        # ----------------------------------------
        self.pause_obj: PausePage = pause_obj
        self.game_state: GameState = game_state

    def run_event(self, event: Event) -> None:
        """
            Processes keyboard inputs to resume game or return to menu.

            Args:
                event (Event): Pygame event object.
        """
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
