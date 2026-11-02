"""
    Main entry point script for the Pac-Man application.

    Handles command-line argument validation, configuration loading, highscore
    initialization, and launching the core game loop.
"""

import sys

from src.d1_classes import Config, GameState
from src.d2_parsing_config_file import Parser
from src.d3_parsing_highscores import HigherScore
from src.d6_game_loop import GameLoop


RED = "\033[31m"
GREEN = "\033[32m"
WHITE = "\033[37m"


# ==============================================================================

def main() -> None:
    """
        Validates command-line arguments, initializes parser, highscores, and
                                                                    game loop.

        Verifies that exactly one JSON configuration file path is passed as an
        argument, loads configurations, sets up highscores and game state, then
        starts execution of the main game loop.

        Raises:
            Exception: If the argument count is not equal to 2 or the file
            does not end with '.json'.
    """

    # ------------ if we have more than one arg || not a json file ------------
    if len(sys.argv) != 2:
        raise Exception(
            f"\n{RED}❌ Usage: python3 pac-man.py <config_file>.json\n{WHITE}\n"
                       )
    if not sys.argv[1].endswith('.json'):
        raise Exception(
            f"{RED}❌ JSON format: '{sys.argv[1]}' must be a json file{WHITE}\n"
                       )
    # -------------------------------------------------------------------------
    p: Parser = Parser(sys.argv[1])
    config: Config = p.conf_obj
    # -------------------------------------------------------------------------
    higher_score_path: str = config.highscore_filename
    highscores_obj: HigherScore = HigherScore(higher_score_path)
    # -------------------------------------------------------------------------
    game_state_obj: GameState = GameState()
    game_state_obj.status = "LOSS"
    # -------------------------------------------------------------------------
    nbr_levels: int = len(config.levels_data)
    g: GameLoop = GameLoop(
                            highscores_obj,
                            game_state_obj,
                            nbr_levels,
                            resolution=(1920, 1080)
                          )
    g.game_loop()


# =============================================================================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
