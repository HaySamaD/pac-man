import pygame
from pygame.event import Event

from ..d1_classes import GameState

from ..d4_display import InstructionsPage


class InstructionsEvents:
    def __init__(
            self, instruction_obj: InstructionsPage, game_state: GameState
                ):
        # -------------------------------------------------------
        self.instruction_obj: InstructionsPage = instruction_obj
        self.game_state: GameState = game_state

    def run_events(self, event: Event) -> None:
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
