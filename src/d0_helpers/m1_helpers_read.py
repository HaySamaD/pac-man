from .m0_colors_RGB import Color

from typing import List, Dict

import json


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
