from src.parsing_config_file.m2_config_parser import Parser

from src.parsing_config_file.m1_pydantic_objs import GameConfig

from src.m2_highscores_system import HighScoreSys, NameScore

from src.m4_display import MainMenuPage

import sys

from typing import List

from src.m4_display import MainMenuPage, HighscoresPage, InstructionsPage, HUD, PauseMenu

from src.m1_our_dataclasses import GameState


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

    # ----- config object parsed -----
    p = Parser(sys.argv[1])
    conf_obj: GameConfig = p.conf_obj

    # ---------------------- higher scores ----------------------
    hs: HighScoreSys = HighScoreSys(conf_obj.highscore_filename)
    higher_scores_obj: List[NameScore] = hs.top_10_scores_obj

    # ------------- display menu page ---------------
    # menu: MainMenuPage = MainMenuPage((1920, 1080))
    # menu.run()

    # ------------- display highscores page ---------------
    # hs_page: HighscoresPage = HighscoresPage(higher_scores_obj, (1920, 1080))
    # hs_page.run()

    # ------------- display instructions page ---------------
    # instr_page: InstructionsPage = InstructionsPage((1920, 1080))
    # instr_page.run()

    # --------- display HUD -------------
    # game_state: GameState = GameState(score=42, lives=3, level=1, time_left=90, status="PLAYING")
    # uud: HUD = HUD(game_state, (1920, 1080))
    # uud.run()

    # --------- display PAUSE page -------------
    pause: PauseMenu = PauseMenu((1920, 1080))
    pause.run()
# --------------------------------------------------------------------------------

if __name__ == "__main__":
    # try:
    main()
    # except Exception as e:
    #     print(e)
