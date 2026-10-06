from typing import List, Dict

import json


class Color:
    RED = "\033[31m"
    YELLOW = '\033[93m'
    GREEN = "\033[32m"
    WHITE = "\033[37m"


# ==================== Default config if missing any data ====================

class Default_conf:

    DICT = {
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


# ============================ Helper methodes ================================

class Helper:
    pass

#     # --------- read json file and return he content (str format) ---------

#     def read_txt_file(self, file_path: str) -> str:

#         try:

#             with open(file_path, 'r') as f:
#                 content: str = f.read()
#             return content

#         except OSError:
#             raise Exception(
#                             f"{Color().RED}❌ Error: {file_path} not exist or "
#                             f"access denied{Color().WHITE}"
#                            )

#     # --------------------------------------------------------------------------

#     def read_highscore_json_file(self, file_path: str) -> List[Dict]:

#         try:

#             with open(file_path, 'r') as f:
#                 content: List[Dict] = json.load(f)
#                 return content

#         except OSError:
#             print(
#                     f"{Color().YELLOW}❌ Error: {file_path} not exist or "
#                     "access denied"
#                     f"{Color().GREEN}n\add default value [] and switch to "
#                     f"'highscores.json'{Color().WHITE}"
#                  )
#             return []

#         except json.JSONDecodeError:
#             print(
#                     f"{Color().YELLOW}❌ Error: {file_path}: wrong syntax"
#                     f"{Color().GREEN}\nadd default value [] and switch to "
#                     f"'data/highscores.json'{Color().WHITE}"
#                  )
#             return []

#         if not isinstance(content, list):
#             return []

#         return content
