"""
    Handles reading configuration files, stripping comments, parsing JSON,
                                                                and validation.
"""

from typing import List, Dict, Any

import json

from ..d1_helpers import Color
from ..d1_helpers import Helper
from ..d1_helpers import DEFAULT_CONFIG
from ..d2_classes import Config


class Parser:
    """
        Parses and validates game configuration files into structured
                                                        configuration objects.

        Attributes:
            config_txt (str): Raw text read from the configuration file.
            net_txt (str): Cleaned configuration text with comments removed.
            conf_dic (Dict[str, Any]): Parsed configuration dictionary.
            conf_obj (Config): Validated configuration Pydantic object.
    """

    def __init__(self, config_path: str) -> None:
        """
        Initializes parser, reads config file, skips comments, parses dict,
                                                        and validates object.

        Args:
            config_path (str): Path to the configuration JSON file.
        """
        # -----------------------------------------------------------
        self.config_txt: str = Helper().read_config_file(config_path)
        self.net_txt: str = self.skip_comments()
        self.conf_dic: Dict[str, Any] = self.str_to_dict()
        self.conf_obj: Config = self.create_config_obj()

    # =========================================================================
    def skip_comments(self) -> str:
        """
            Removes lines starting with '#' comments from the raw
                                                            configuration text.

            Returns:
                str: Cleaned configuration text without comment lines.
        """
        # ---------------------------------------------
        lines: List[str] = self.config_txt.splitlines()
        # ---------------------------------------------
        res: List[str] = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            res.append(line)
        # ---------------------------------------------
        return "".join(res)

    # =========================================================================
    def str_to_dict(self) -> Dict[str, Any]:
        """
            Parses cleaned configuration text into a Python dictionary with
                                                            default fallback.

            Returns:
                Dict[str, Any]: Configuration dictionary loaded from JSON or
                                                    default config on error.
        """
        # ------------------------------------------------------------------
        try:
            conf_dic: Dict[str, Any] = json.loads(self.net_txt)
        except json.decoder.JSONDecodeError:
            print(
                f"{Color().RED}\n❌ JSON syntax: the syntax not conforme\n"
                f"{Color().GREEN}switching to default config data ...\n"
                f"{Color().WHITE}"
                 )
            conf_dic = DEFAULT_CONFIG
        # ------------------------------------------------------------------
        return conf_dic

    # =========================================================================
    def create_config_obj(self) -> Config:
        """
            Validates configuration dictionary data and instantiates a Config
                                                            Pydantic object.

            Returns:
                Config: Validated Config object.
        """
        # --- because the .load(): load the objet but not guaranteed
        #                                  if is it is a dict (maybe a list ---
        if not isinstance(self.conf_dic, dict):
            print(
                    f"\n{Color().YELLOW}the config is not a dictionary. \n"
                    f"{Color().GREEN}default config is added{Color().WHITE}\n"
                 )
            self.conf_dic = DEFAULT_CONFIG
        # ---------------------------------------------------------------------
        config_obj: Config = Config.model_validate(self.conf_dic)
        # ---------------------------------------------------------------------
        return config_obj
