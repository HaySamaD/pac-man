from src.m2_config_parser import Parser

from typing import List, Dict

import sys

RED = "\033[31m"
GREEN = "\033[32m"
WHITE = "\033[37m"


# --------------------------------------------------------------------------------

def main():

    # ---------------------------------------------------------------------------

    if len(sys.argv) != 2:
        raise Exception(
            f"\n{RED}❌ Usage: python3 pac-man.py <config_file>.json\n{WHITE}\n"
                       )

    if not sys.argv[1].endswith('.json'):
        raise Exception(
            f"{RED}❌ JSON format: '{sys.argv[1]}' must be a json file{WHITE}\n"
                       )

    # ---------------------------------------------------------------------------

    p = Parser(sys.argv[1])

    conf_obj: List[Dict] = p.conf_obj


# --------------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
