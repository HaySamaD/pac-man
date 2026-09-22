from src.dataclasses import GameConfig
from typing import List, Dict
import json


RED = "\033[31m"
GREEN = "\033[32m"
WHITE = "\033[37m"


DEFAULT_DICT = {
                    "highscore_file": "test.json",

                    "levels_data": [
                                    {"width": 20, "height": 20, "pacgum": 42},
                                    {"width": 20, "height": 20, "pacgum": 42},
                                    {"width": 20, "height": 20, "pacgum": 42},
                                    {"width": 20, "height": 20, "pacgum": 42},
                                    {"width": 20, "height": 20, "pacgum": 42},
                                    {"width": 20, "height": 20, "pacgum": 42},
                                    {"width": 20, "height": 20, "pacgum": 42},
                                    {"width": 20, "height": 20, "pacgum": 42},
                                    {"width": 20, "height": 20, "pacgum": 42},
                                    {"width": 20, "height": 20, "pacgum": 42}
                                   ],

                    "lives": 3,

                    "pacgum_points": 10,

                    "super_pacgum_points": 50,

                    "ghost_points": 200,

                    "seed": 42,

                    "level_max_time": 90
                }


class Helper:

    def read_json_file(self, json_path: str) -> str | GameConfig:
        try:
            with open(json_path, 'r') as f:
                content: str = f.read()
            return content
        except (FileNotFoundError, OSError):
            raise Exception(
                f"{RED}❌ Error: {json_path} not exist or access denied{WHITE}"
                           )


class Parser:

    def __init__(self, config_path) -> None:

        # ----------------------------------------------------------
        self.config_txt: str = Helper().read_json_file(config_path)

        # ----------------------------------------------------------
        self.net_txt: str = self.skip_comments_and_filter_text()

        # ---------------------------------------------------------
        self.conf_obj = self.build_config_object()

    # -------------------------------------------------------

    def skip_comments_and_filter_text(self) -> str:

        lines: List[str] = self.config_txt.splitlines()

        res: List[str] = []
        for line in lines:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "#" in line:
                line = line.split("#")[0].strip()

            res.append(line)

        return "".join(res)

    # --------------------------------------------------------

    def build_config_object(self):

        try:

            conf_obj = json.loads(self.net_txt)

        except json.decoder.JSONDecodeError:

            print(
                f"{RED}\n❌ JSON syntax: the syntax not conforme\n{GREEN}"
                F"switching to default config data ...\n{WHITE}"
                 )

            conf_obj = DEFAULT_DICT

        return conf_obj

    # --------------------------------------------------------
