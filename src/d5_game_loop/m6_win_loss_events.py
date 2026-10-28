import pygame
from pygame.event import Event

from ..d1_classes import GameState

from ..d3_parsing_highscores import HighScoreSys

from ..d4_display import Printer


class WinLossEvent:
    def __init__(self, highscores_obj: HighScoreSys, p: Printer, game_status: GameState):
        # -------------------------------------------------
        self.highscores_obj: HighScoreSys = highscores_obj
        self.p: Printer = p
        self.game_status: GameState = game_status

    def run_event(self, event: Event, player_name: str):
        # ---------------------------
        while True:
            char: str = event.unicode
            if player_name.strip():
                if (
                        (char.isalpha() or char.isspace())
                        and len(player_name) < 10
                   ):
                    player_name += char
                if event.key == pygame.K_RETURN:
                    name: str = player_name
                    score: int = self.game_status.score
                    self.highscores_obj.add_new_score({"name": name, "score": score})