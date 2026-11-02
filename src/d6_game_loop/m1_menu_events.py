"""
    Handles keyboard event management and navigation logic for the main menu
                                                                        screen.
"""

import pygame

from pygame.event import Event

from ..d1_classes.m1_dataclasses import GameState
from ..d4_display.m1_main_page import MainPage


class MenuEvent:
    """
        Manages menu option selection and state transitions from keyboard
                                                                        input.

        Attributes:
            main_obj (MainPage): Main page display instance.
            game_state (GameState): Active game state instance.
    """
    def __init__(
                    self,
                    main_obj: MainPage,
                    game_state: GameState,
                ) -> None:
        """
            Initializes menu event handler with main page and game state
                                                                references.

            Args:
                main_obj (MainPage): Main page instance.
                game_state (GameState): Game state instance.
        """
        # ------------ init params -------------
        self.main_obj: MainPage = main_obj
        self.game_state: GameState = game_state

    # =======================================================
    def run_event(self, event: Event, running: bool) -> bool:
        """
            Processes keyboard events to navigate menu items and update game
                                                                        status.

            Args:
                event (Event): Pygame event object.
                running (bool): Current application running state flag.

            Returns:
                bool: Updated application running state flag.
        """
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
