"""
    Provides file reading methodes including:
    - read the cinfig file
    - read the highscores file
"""

from .m1_colors_RGB import Color

from typing import List, Dict

import json


class Helper:
    """
        Handles safe reading of JSON configuration and highscore files.

        Methods:
            read_config_file: Reads configuration file content as a string.
            read_highscore_file: Loads highscore records from JSON file safely.
    """

    # =========== Read json file and return he content (str format) ===========
    def read_config_file(self, file_path: str) -> str:
        """
            Reads configuration file and returns its content as a string.

            Args:
                file_path (str): Path to the configuration file.

            Returns:
                str: Raw text content of the configuration file.

            Raises:
                Exception: If file does not exist or access is denied.
        """
        # ---------------------------------------------------------------------
        try:
            with open(file_path, 'r') as f:
                content: str = f.read()
            return content
        except OSError:
            raise Exception(
                            f"{Color().RED}❌Error: '{file_path}' not exist or "
                            f"access denied{Color().WHITE}"
                           )
        # ---------------------------------------------------------------------

    # ==========================================================================
    def read_highscore_file(self, file_path: str) -> List[Dict]:
        """
            Loads highscore JSON file and returns data as list of dictionaries.

            Args:
                file_path (str): Path to the highscore JSON file.

            Returns:
                List[Dict]: List of highscore dictionaries,
                                                        or empty list on error.
        """
        # ----------------------------------------------------------------------
        try:
            with open(file_path, 'r') as f:
                content: List[Dict] = json.load(f)
                if not isinstance(content, list):
                    return []
                return content
        except OSError:
            print(
                    f"\n{Color().YELLOW}❌Error: '{file_path}' not exist or "
                    "access denied\n"
                    f"{Color().GREEN}add default value [] and switch to "
                    f"'highscores.json'{Color().WHITE}"
                 )
            return []
        except json.JSONDecodeError:
            print(
                    f"\n{Color().YELLOW}❌Error: {file_path}: wrong JSON syntax"
                    f"\n{Color().GREEN}\nadd default value []"
                 )
            return []
        # ----------------------------------------------------------------------
