from typing import List, Dict, Any
import json
from ..m0_helpers import Helper, Color
from .m1_pydantic_objs import GameConfig


DEF_CONFIG = {

                "highscore_filename": "data/highscores.json",

                "levels_data": [
                                    {"width": 42, "height": 42, "pacgum": 42}
                                    for _ in range(10)
                               ],

                "lives": 3,

                "points_per_pacgum": 10,

                "points_per_super_pacgum": 20,

                "points_per_ghost": 40,

                "seed": 42,

                "level_max_time": 300

            }


# ==============================================================================

class Parser:

    def __init__(self, config_path: str) -> None:

        # ---------------- Raw text config ------------------------
        self.config_txt: str = Helper().read_txt_file(config_path)

        # ------ text after remove comments -----
        self.net_txt: str = self.skip_comments()

        # ---------- transf the text to dict object ----------
        self.conf_dic: Dict[str, Any] = self.get_config_dict()

        # ------------- the finale parsed config object -------
        self.conf_obj: GameConfig = self.create_gameconf_obj()

    # -------------------------------------------------------

    def skip_comments(self) -> str:

        lines: List[str] = self.config_txt.splitlines()

        res: List[str] = []
        for line in lines:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            res.append(line)

        return "".join(res)

    # --------------------------------------------------------

    def get_config_dict(self) -> Dict[str, Any]:

        try:

            conf_dic: Dict[str, Any] = json.loads(self.net_txt)

        except json.decoder.JSONDecodeError:

            print(
                f"{Color().RED}\n❌ JSON syntax: the syntax not conforme\n"
                f"{Color().GREEN}switching to default config data ...\n"
                f"{Color().WHITE}"
                 )

            conf_dic = DEF_CONFIG

        return conf_dic

    # --------------------------------------------------------

    def create_gameconf_obj(self) -> GameConfig:

        if not isinstance(self.conf_dic, dict):
            print(
                    f"\n{Color().YELLOW}the config is not a dictionary. \n"
                    f"{Color().GREEN}default config is added{Color().WHITE}\n"
                 )
            self.conf_dic = DEF_CONFIG

        config_obj: GameConfig = GameConfig(**self.conf_dic)

        return config_obj
