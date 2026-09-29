from src.parsing_config_file.m2_config_parser import Parser

from src.parsing_config_file.m1_pydantic_objs import GameConfig

from typing import Dict

from src.m2_highscores_system import HighScoreSys

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

    # ---------------------------------
    hs: HighScoreSys = HighScoreSys(conf_obj.highscore_filename)
    print(hs.highscores_obj)

# --------------------------------------------------------------------------------

if __name__ == "__main__":
    # try:
    main()
    # except Exception as e:
    #     print(e)
