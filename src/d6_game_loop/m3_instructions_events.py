"""
    Handles keyboard event management and navigation for the instructions
                                                                        screen.
"""

import pygame
from pygame.event import Event

from ..d2_classes import GameState

from ..d5_display import InstructionsPage


class InstructionsEvents:
    """
        Manages navigation inputs on the instructions screen.

        Attributes:
            instruction_obj (InstructionsPage): Instructions page display
                                                                    instance.
            game_state (GameState): Active game state instance.
    """
    def __init__(
            self, instruction_obj: InstructionsPage, game_state: GameState
                ):
        """
            Initializes instructions event handler.

            Args:
                instruction_obj (InstructionsPage): Instructions page instance.
                game_state (GameState): Game state instance.
        """
        # -------------------------------------------------------
        self.instruction_obj: InstructionsPage = instruction_obj
        self.game_state: GameState = game_state

    def run_events(self, event: Event) -> None:
        """
            Processes keyboard events to return to the main menu.

            Args:
                event (Event): Pygame event object.
        """
        # ------------------------------------
        if event.key == pygame.K_DOWN:
            self.instruction_obj.pos += 1
            if self.instruction_obj.pos > 1:
                self.instruction_obj.pos = 0
        elif event.key == pygame.K_UP:
            self.instruction_obj.pos -= 1
            if self.instruction_obj.pos < 0:
                self.instruction_obj.pos = 1
        elif event.key == pygame.K_RETURN:
            if self.instruction_obj.pos == 1:
                self.game_state.status = "MENU"
