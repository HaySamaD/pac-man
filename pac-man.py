from src.parsing_config_file.m2_config_parser import Parser

from src.parsing_config_file.m1_pydantic_obj import GameConfig

from typing import List, Dict

from src.highscores_system import HighScoreSys

import sys

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

    # ---------------------------------------------------------------------------

    highscore_obj: HighScoreSys = HighScoreSys(conf_obj.highscore_filename)

    highscore_dict: Dict[str, int] = highscore_obj.highscores_meta

    print(highscore_dict)


# --------------------------------------------------------------------------------

if __name__ == "__main__":
    # try:
    main()
    # except Exception as e:
    #     print(e)
