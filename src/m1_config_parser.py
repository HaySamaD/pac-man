from typing import List, Dict
import json
from src.helpers import Helper, Default_conf, Color
from pydantic import BaseModel, Field
from src.dataclasses import GameConfig

# ==============================================================================


class Parser:

    def __init__(self, config_path) -> None:

        # ------------------ Raw text config -------------------------
        self.config_txt: str = Helper().read_config_file(config_path)

        # ---------------- Net text config -----------------------
        self.net_txt: str = self.skip_comments()

        # ---------- config object ----------------
        self.conf_obj: List[Dict] = self.build_config_object()

    # -------------------------------------------------------

    def skip_comments(self) -> str:

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
                f"{Color().RED}\n❌ JSON syntax: the syntax not conforme\n"
                f"{Color().GREEN}\nswitching to default config data ...\n"
                f"{Color().WHITE}"
                 )

            conf_obj = Default_conf().DICT

        return conf_obj

    # --------------------------------------------------------

    def parse_config_object(self):

        g_conf: GameConfig = GameConfig(**self.conf_obj)

        return g_conf
