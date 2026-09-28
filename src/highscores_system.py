from .parsing_config_file.m0_helpers import Helper

from typing import List, Dict

from .parsing_config_file.m0_helpers import Color


class HighScoreSys:

    def __init__(self, highscores_path: str):

        # ---------------- get the content of highscores file ----------------
        self.highscores_meta: List[Dict] = (
                                    Helper().read_json_file(highscores_path)
                                           )

    def clean_highscores(self) -> List[Dict[str, int]]:

        for i in self.highscores_meta:

            pass
