from src.dataclasses import GameConfig
from typing import List, Dict
import json

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

        self.net_txt: str = self.skip_comments_and_filter_text()

    def skip_comments_and_filter_text(self) -> str:

        splt_line: List[str] = self.config_txt.splitlines()

        res: List[str] = []

        for line in splt_line:

            line = line.strip()

            if line.startswith("#"):
                continue

            if "#" in line:
                line = line.split("#")[0].strip()

            res.append(line)

        return "".join(res)
