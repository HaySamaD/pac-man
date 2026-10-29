from typing import List, Dict, Any

import json

from ..d0_helpers import Color
from ..d0_helpers import Helper
from ..d0_helpers import DEFAULT_CONFIG_FILE
from ..d1_classes import Config


class Parser:

    def __init__(self, config_path: str) -> None:
        # -----------------------------------------------------------
        self.config_txt: str = Helper().read_config_file(config_path)
        self.net_txt: str = self.skip_comments()
        self.conf_dic: Dict[str, Any] = self.str_to_dict()
        self.conf_obj: Config = self.create_game_conf_obj()

    # ==================================================
    def skip_comments(self) -> str:
        # ---------------------------------------------
        lines: List[str] = self.config_txt.splitlines()
        # ---------------------------------------------
        res: List[str] = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            res.append(line)
        # -----------------
        return "".join(res)

    # ======================================================================
    def str_to_dict(self) -> Dict[str, Any]:
        # ------------------------------------------------------------------
        try:
            conf_dic: Dict[str, Any] = json.loads(self.net_txt)
        except json.decoder.JSONDecodeError:
            print(
                f"{Color().RED}\n❌ JSON syntax: the syntax not conforme\n"
                f"{Color().GREEN}switching to default config data ...\n"
                f"{Color().WHITE}"
                 )
            conf_dic = DEFAULT_CONFIG_FILE
        # ------------------------------------------------------------------
        return conf_dic

    # =========================================================================
    def create_game_conf_obj(self) -> Config:
        # --- because the .load(): load the objet but not guaranteed
        #                                  if is it is a dict (maybe a list ---
        if not isinstance(self.conf_dic, dict):
            print(
                    f"\n{Color().YELLOW}the config is not a dictionary. \n"
                    f"{Color().GREEN}default config is added{Color().WHITE}\n"
                 )
            self.conf_dic = DEFAULT_CONFIG_FILE
        # ---------------------------------------------------------------------
        config_obj: Config = Config.model_validate(self.conf_dic)
        # ---------------------------------------------------------------------
        return config_obj
