"""Manages player name input and highscore saving on win or loss screens."""

import pygame
from pygame.event import Event

from ..d2_classes import GameState

from ..d4_parsing_highscores import HigherScore


class WinLossEvent:
    """
        Handles character entry for player names and updates highscores.

        Attributes:
            highscores_obj (HigherScore): Highscore management instance.
            p (Printer): Printer utility instance.
            game_status (GameState): Active game state instance.
            height (int): Screen height resolution.
            player_name (str): Current input string for player name.
    """
    def __init__(
                    self,
                    highscores_obj: HigherScore,
                    game_status: GameState,
                    height: int
                ) -> None:
        """
            Initializes win/loss event handler.

            Args:
                highscores_obj (HigherScore): Highscore manager instance.
                p (Printer): Printer utility instance.
                game_status (GameState): Game state instance.
                height (int): Screen height.
        """
        # ------------------------------------------------
        self.highscores_obj: HigherScore = highscores_obj
        self.game_status: GameState = game_status
        self.height: int = height
        self.player_name: str = ""

    def run_event(self, event: Event) -> str:
        """
            Captures keyboard inputs for player name entry and saves score on
                                                                        enter.

            Args:
                event (Event): Pygame event object.

            Returns:
                str: Updated player name string.
        """
        # ---------------------------------------------------------------------
        if event.key == pygame.K_RETURN:
            if self.player_name.strip():
                name: str = self.player_name
                score: int = self.game_status.score
                self.highscores_obj.add_new_score(
                                                {"name": name, "score": score}
                                                 )
                self.highscores_obj.save_top_10_scores()
                self.game_status.status = "MENU"
                self.player_name = ""
        elif event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
        else:
            char: str = event.unicode
            if (
                (char.isalnum() or char.isspace())
                and len(self.player_name) < 10
               ):
                self.player_name += char
        # ---------------------------------------------------------------------
        return self.player_name
