from typing import List, Dict, Tuple

import json


class Color:
    RED = "\033[31m"
    YELLOW = '\033[93m'
    GREEN = "\033[32m"
    WHITE = "\033[37m"


class Rgb:
    WHITE: Tuple[int] = (255, 255, 255)
    GREEN: Tuple[int] = (0, 255, 0)
    YELLOW: Tuple[int] = (255, 255, 0)
    PINK: Tuple[int] = (255, 192, 203)
    BLACK: Tuple[int] = (0, 0, 0)


# ============================ Helper methodes ================================

class Helper:

    # --------- read json file and return he content (str format) ---------

    def read_txt_file(self, file_path: str) -> str:

        try:

            with open(file_path, 'r') as f:
                content: str = f.read()
            return content

        except OSError:
            raise Exception(
                            f"{Color().RED}❌ Error: {file_path} not exist or "
                            f"access denied{Color().WHITE}"
                           )

    # --------------------------------------------------------------------------

    def read_highscore_json_file(self, file_path: str) -> List[Dict]:

        try:

            with open(file_path, 'r') as f:
                content: List[Dict] = json.load(f)
                if not isinstance(content, list):
                    return []
                return content

        except OSError:
            print(
                    f"{Color().YELLOW}❌ Error: {file_path} not exist or "
                    "access denied"
                    f"{Color().GREEN}n\add default value [] and switch to "
                    f"'highscores.json'{Color().WHITE}"
                 )
            return []

        except json.JSONDecodeError:
            print(
                    f"{Color().YELLOW}❌ Error: {file_path}: wrong syntax"
                    f"{Color().GREEN}\nadd default value [] and switch to "
                    f"'data/highscores.json'{Color().WHITE}"
                 )
            return []

# =============================================================================
