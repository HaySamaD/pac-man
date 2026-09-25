
class Color:
    RED = "\033[31m"
    YELLOW = '\033[93m'
    GREEN = "\033[32m"
    WHITE = "\033[37m"


# ==================== Default config if missing any data ====================

class Default_conf:

    DICT = {
                "highscore_filename": "top_10_scores.json",

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

    def read_config_file(self, json_path: str) -> str:
        try:
            with open(json_path, 'r') as f:
                content: str = f.read()
            return content
        except (FileNotFoundError, OSError):
            raise Exception(
                            f"{Color().RED}❌ Error: {json_path} not exist or "
                            f"access denied{Color().WHITE}"
                           )
