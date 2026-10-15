from typing import List, Dict, Any

import json

from d0_helpers.m0_colors_RGB import Color
from d0_helpers.m1_helpers_read import Helper
from d0_helpers.m2_static_data import DEFAULT_CONFIG_FILE
from d1_classes.m0_pydantic_classes import GameConfig


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

            conf_dic = DEFAULT_CONFIG_FILE

        return conf_dic

    # --------------------------------------------------------

    def create_gameconf_obj(self) -> GameConfig:

        if not isinstance(self.conf_dic, dict):
            print(
                    f"\n{Color().YELLOW}the config is not a dictionary. \n"
                    f"{Color().GREEN}default config is added{Color().WHITE}\n"
                 )
            self.conf_dic = DEFAULT_CONFIG_FILE

        config_obj: GameConfig = GameConfig(**self.conf_dic)

        return config_obj
