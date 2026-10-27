import sys

from src.d1_classes import GameConfig, NameScore, GameState

from src.d2_parsing_config_file import Parser

from src.d3_parsing_highscores import HighScoreSys

from src.d4_display import MainMenuPage, HighscoresPage, InstructionsPage
from src.d4_display import HUD, PauseMenuPage, GameOverPage, WinPage
from src.d5_game_loop import GameLoop

from typing import List


RED = "\033[31m"
GREEN = "\033[32m"
WHITE = "\033[37m"


# --------------------------------------------------------------------------------

def main() -> None:

    # ------------ if we have more than one arg || not a json file ------------
    if len(sys.argv) != 2:
        raise Exception(
            f"\n{RED}❌ Usage: python3 pac-man.py <config_file>.json\n{WHITE}\n"
                       )
    if not sys.argv[1].endswith('.json'):
        raise Exception(
            f"{RED}❌ JSON format: '{sys.argv[1]}' must be a json file{WHITE}\n"
                       )
    # ------ config validated ------
    p: Parser = Parser(sys.argv[1])
    config: GameConfig = p.conf_obj
    # ----------------- highscore object -----------------
    higher_score_path: int = config.highscore_filename
    highscores_obj: HighScoreSys = HighScoreSys(higher_score_path)
    # -------------------------------------
    game_state_obj: GameState = GameState()
    game_state_obj.status = "LOSS"
    # ----------------------------------------------------
    final_level: int = len(config.levels_data)
    g: GameLoop = GameLoop(
                            highscores_obj,
                            game_state_obj,
                            final_level,
                            resolution=(1920, 1080)
                          )
    g.game_loop()


if __name__ == "__main__":
    # try:
    main()
    # except Exception as e:
    #     print(e)
