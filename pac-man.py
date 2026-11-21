"""
    Main entry point script for the Pac-Man application.

    Handles command-line argument validation, configuration loading, highscore
    initialization, and launching the core game loop.
"""

import sys

from src.d2_classes import Config, GameState
from src.d3_parsing_config_file import Parser
from src.d4_parsing_highscores import HigherScore
from src.d6_game_loop import GameLoop
from src.d1_helpers import Color


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
                        f"\n{Color.RED}❌ Usage: python3 pac-man.py "
                        f"<config_file>.json\n{Color.WHITE}\n"
                       )
    if not sys.argv[1].endswith('.json'):
        raise Exception(
                        f"{Color.RED}❌ JSON format: '{sys.argv[1]}' must be "
                        f"a json file{Color.WHITE}\n"
                       )
    # -------------------------------------------------------------------------
    config: Config = Parser(sys.argv[1]).conf_obj
    # -------------------------------------------------------------------------
    highscores_obj: HigherScore = HigherScore(config.highscore_filename)
    # -------------------------------------------------------------------------
    game_state_obj: GameState = GameState()
    # --------------------------- run the game loop ---------------------------
    nbr_levels: int = len(config.levels_data)
    g: GameLoop = GameLoop(
                            config,
                            highscores_obj,
                            game_state_obj,
                            nbr_levels
                          )
    g.game_loop()
    # -------------------------------------------------------------------------
    return None


# =============================================================================
if __name__ == "__main__":
    try:
        main()
    except (Exception, KeyboardInterrupt, ImportError) as e:
        print(e)
