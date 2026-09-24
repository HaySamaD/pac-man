
class Color:
    RED = "\033[31m"
    YELLOW = '\033[93m'
    GREEN = "\033[32m"
    WHITE = "\033[37m"


# ==================== Default config if missing any data ====================

class Default_conf:

    DICT = {
                "highscore_file": "highscore.json",

                "levels_data": [
                                    {"width": 42, "height": 42, "pacgum": 42}
                                    for _ in range(10)
                                ],

                "lives": 3,

                "pacgum_points": 10,

                "super_pacgum_points": 20,

                "ghost_points": 40,

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
