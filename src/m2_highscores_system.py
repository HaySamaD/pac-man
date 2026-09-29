from .m0_helpers import Helper

from pydantic import BaseModel, Field, model_validator

from src.m0_helpers import Color

from typing import List, Dict


class NameScore(BaseModel):
    name: str
    score: int

    @model_validator(mode="before")
    @classmethod
    def validate(cls, dic):

        if not isinstance(dic, dict):
            print(
                    f"{Color().YELLOW}{dic} not a dict."
                    f"{Color().GREEN}{dic}\nswitch to default value"
                    f"{Color().WHITE}{dic}"
                 )
            return {"name": "player", "score": 0}

        return dic



class HighScoreSys:

    def __init__(self, highscores_path: str):

        # ---------------- get the content of highscores file ----------------
        self.highscores_meta: List[Dict] = (
                            Helper().read_highscore_json_file(highscores_path)
                                           )

        self.highscores_obj: NameScore = [
                                            NameScore.model_validate(i)
                                            for i in self.highscores_meta
                                         ]
