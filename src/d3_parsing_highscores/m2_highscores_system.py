
from typing import List, Dict, Any

import json

from ..d0_helpers import Helper
from ..d1_classes import NameScore


class HighScoreSys:

    def __init__(self, highscores_path: str):
        # ------------- init params ---------------
        self.highscores_path: str = highscores_path
        # ------------------- get the highscores metadata --------------------
        self.highscores_meta: List[Dict] = (
                            Helper().read_highscore_file(highscores_path)
                                           )
        # -------- get the highscores_obj after parsing the metadata ---------
        self.highscores_obj: List[NameScore] = [
                                                NameScore.model_validate(i)
                                                for i in self.highscores_meta
                                               ]
        # ------------------- get top 10 scores -------------------
        self.top_10_scores_obj = sorted(
                                            self.highscores_obj,
                                            key=lambda x: x.score,
                                            reverse=True
                                       )[:10]

    # -------- add a new score and rebuild top 10 high scores ---------
    def add_new_score(self, dict_meta: Dict[str, Any]) -> None:
        # -------------------------------------------------------------
        name_score_obj: NameScore = NameScore.model_validate(dict_meta)
        self.highscores_obj.append(name_score_obj)
        # ---------------------------------------------------------
        self.top_10_scores_obj = sorted(
                                            self.highscores_obj,
                                            key=lambda x: x.score,
                                            reverse=True
                                       )[:10]
        # ----------
        return None

    # ------ override the content of highscore file by new top 10 scores ------
    def save_top_10_scores(self) -> List[Dict[str, int]]:
        # transforme the top_10_scores_obj to list of dict for save it to json
        lst_top_10_scores_lst_dict: List[Dict[str, int]] = [
                                                i.model_dump()
                                                for i in self.top_10_scores_obj
                                                            ]
        # ---- read and overrite the highscore JSON file -----
        with open(self.highscores_path, 'w') as f:
            json.dump(lst_top_10_scores_lst_dict, f, indent=2)
        # -------------------------------
        return lst_top_10_scores_lst_dict
