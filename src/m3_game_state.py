from .m1_our_dataclasses import GameState


# class GameState:
#     """ state of the game per status. """
#     score: int = 0
#     lives: int = 3
#     level: int = 1
#     time_left: int = 90
#     status: str = "MENU"  # MENU, PLAYING, PAUSED, GAME_OVER, VICTORY


class GameManager:
    def __init__(self, game_state: GameState, level_max_time: int) -> None:
        self.game_state: GameState = game_state
        self.level_max_time: int = level_max_time

    # --------------------------------------------
    def increment_score(self, count: int) -> None:
        self.game_state.score += count

    # -----------------------------------
    def decrement_lives(self) -> None:
        self.game_state.lives -= 1

    # ---------------------------------
    def increment_level(self) -> None:
        self.game_state.level += 1

    # -------------------------------------------------
    def reset_time(self) -> None:
        self.game_state.time_left = self.level_max_time

    # ------------------------------------------------
    def change_status_game(self, status: str) -> None:
        self.game_state.status = status

    # -----------------------------------------------
    def decrement_time(self) -> None:

        self.game_state.time_left -= 1

        if self.game_state.time_left <= 0:

            if self.game_state.lives <= 0:
                self.change_status_game("GAME_OVER")

            else:
                self.decrement_lives()
                self.reset_time()
