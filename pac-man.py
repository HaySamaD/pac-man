from parsing_config_file.m1_config_parser import Parser

from src.parsing_config_file.m1_pydantic_objs import GameConfig

from d3_highscores_parser.m2_highscores_system import HighScoreSys, NameScore

from d5_display.m7_win_page import MainMenuPage

import sys

from typing import List

from d5_display.m7_win_page import MainMenuPage, HighscoresPage, InstructionsPage, HUD, PauseMenuPage, GameOverPage, WinPage

from d1_classes.m1_dataclasses import GameState


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
    # pause: PauseMenu = PauseMenu((1920, 1080))
    # pause.run()

    # --------- display game over page -------------
    # game_over: GameOver = GameOver((1920, 1080))
    # game_over.run()

    # --------- display win page -------------
    win: WinPage = WinPage((1920, 1080))
    win.run()
# --------------------------------------------------------------------------------

if __name__ == "__main__":
    # try:
    main()
    # except Exception as e:
    #     print(e)
