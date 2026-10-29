from typing import Tuple

import pygame
from pygame.event import Event

from ..d0_helpers import Rgb

from ..d1_classes import GameState

from ..d3_parsing_highscores import HighScoreSys

from ..d4_display import Printer


class WinLossEvent:
    def __init__(self, highscores_obj: HighScoreSys, p: Printer, game_status: GameState, height: int):
        # -------------------------------------------------
        self.highscores_obj: HighScoreSys = highscores_obj
        self.p: Printer = p
        self.game_status: GameState = game_status
        self.height: int = height
        self.player_name: str = ""

    def run_event(self, event: Event) -> None:
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
        # ----------------------
        return self.player_name
