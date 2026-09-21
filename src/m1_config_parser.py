from src.dataclasses import GameConfig


class Helper:

    def read_json_file(self, json_path: str) -> str | GameConfig:
        try:
            with open(json_path, 'r') as f:
                content: str = f.read()
            return content
        except (FileNotFoundError, OSError):
            raise Exception(f"❌ Error: {json_path} not exist or access denied")


class Parser:

    def __init__(self, config_path) -> None:

        self.config_txt: str = Helper().read_json_file(config_path)
