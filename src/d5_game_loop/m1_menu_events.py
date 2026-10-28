import pygame

from pygame.event import Event

from ..d1_classes.m1_dataclasses import GameState
from ..d4_display.m1_main_menu import MainMenuPage


class MenuEvent:
    def __init__(
                    self,
                    menu_obj: MainMenuPage,
                    game_state: GameState,
                ) -> None:
        # ------------ init params -------------
        self.menu_obj: MainMenuPage = menu_obj
        self.game_state: GameState = game_state

    def run_event(self, event: Event, running: bool) -> bool:
        if event.key == pygame.K_DOWN:
            self.menu_obj.pos += 1
            if self.menu_obj.pos > 3:
                self.menu_obj.pos = 0
        elif event.key == pygame.K_UP:
            self.menu_obj.pos -= 1
            if self.menu_obj.pos < 0:
                self.menu_obj.pos = 3
        elif event.key == pygame.K_RETURN:
            if self.menu_obj.pos == 0:
                self.game_state.status = "PLAY"
            elif self.menu_obj.pos == 1:
                self.game_state.status = "HIGHSCORES"
            elif self.menu_obj.pos == 2:
                self.game_state.status = "INSTRUCTIONS"
            elif self.menu_obj.pos == 3:
                running = False

        return running
