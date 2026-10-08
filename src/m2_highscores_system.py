from .m0_helpers import Helper

from pydantic import BaseModel, model_validator

from src.m0_helpers import Color

from typing import List, Dict

import json


class NameScore(BaseModel):
    name: str
    score: int

    @model_validator(mode="before")
    @classmethod
    def validate(cls, dic):

        # ------------- Verify first that we have a dict -------------
        if not isinstance(dic, dict):
            print(
                    f"{Color().YELLOW}{dic} not a dict."
                    f"{Color().GREEN}\nswitch to default value"
                    f"{Color().WHITE}"
                 )
            return {"name": "player", "score": 0}

        # ---- get the content of dict ----
        name: str = dic.get("name", None)
        score: int = dic.get("score", None)

        # ------ verify name (len <= 10 + each char isalnum or isspace) ------

        if not isinstance(name, str):
            print(
                    f"\n{Color().YELLOW}One of players data han not 'name'\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['name'] = 'Player'
            name = 'Player'

        elif len(name) > 10:
            print(
                    f"\n{Color().YELLOW}the len of '{name}' if > 10\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['name'] = 'Player'
            name = 'Player'

        elif not all(c.isalnum() or c.isspace() for c in name):
            print(
                    f"\n{Color().YELLOW}One of chars of '{name}' not a alnum"
                    f" or space\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['name'] = 'Player'
            name = 'Player'

        # --------------------- verefy score is a integer -------------------
        if not isinstance(score, int):
            print(
                    f"\n{Color().YELLOW}'{score}' is not a integer\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['score'] = 0

        # ---------
        return dic


# =================================================================================

class HighScoreSys:

    def __init__(self, highscores_path: str):

        # ------------- init params ---------------
        self.highscores_path: str = highscores_path

        # ------------------- get the highscores metadata --------------------
        self.highscores_meta: List[Dict] = (
                            Helper().read_highscore_json_file(highscores_path)
                                           )

        # -------- get the highscores_obj after parsing the metadata ---------
        self.highscores_obj: List[NameScore] = [
                                                NameScore.model_validate(i)
                                                for i in self.highscores_meta
                                               ]

        # ----------- get top 10 scores ------------
        self.top_10_scores_obj = sorted(
                                            self.highscores_obj,
                                            key=lambda x: x.score,
                                            reverse=True
                                       )[:10]

    # -------- add a new score and rebuild top 10 high scores --------
    def add_new_score(self, dict_meta: Dict[str, str | int]) -> None:

        name_score_obj: NameScore = NameScore(**dict_meta)

        self.highscores_obj.append(name_score_obj)

        self.top_10_scores_obj = sorted(
                                            self.highscores_obj,
                                            key=lambda x: x.score,
                                            reverse=True
                                       )[:10]

    # ---override the content of highscore file by new top 10 scores ---
    def save_top_10_scores(self):

        # transforme the top_10_scores_obj to list of dict for save it to json
        lst_top_10_scores_lst_dict: List[Dict] = [
                                                i.model_dump()
                                                for i in self.top_10_scores_obj
                                                 ]

        # read and overrite the highscore JSON file
        with open(self.highscores_path, 'w') as f:
            json.dump(lst_top_10_scores_lst_dict, f, indent=2)

        return lst_top_10_scores_lst_dict
