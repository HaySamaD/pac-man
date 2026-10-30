
from typing import List, Dict, Any

import json

from ..d0_helpers import Helper
from ..d1_classes import NameScore


class HigherScore:

    def __init__(self, highscores_path: str):
        # --------------------------- init params ----------------------------
        self.highscores_path: str = highscores_path
        # ------------------- get the highscores metadata --------------------
        self.meta: List[Dict] = (
                            Helper().read_highscore_file(highscores_path)
                                )
        # -------- get the highscores_obj after parsing the metadata ---------
        self.highscores: List[NameScore] = [
                                            NameScore.model_validate(i)
                                            for i in self.meta
                                           ]
        # ------------------------ get top 10 scores -------------------------
        self.top_10_scores = sorted(
                                    self.highscores,
                                    key=lambda x: x.score,
                                    reverse=True
                                   )[:10]

    # =========================================================================
    def add_new_score(self, dict_meta: Dict[str, Any]) -> None:
        # ----------------------------------------------------------
        name_score: NameScore = NameScore.model_validate(dict_meta)
        self.highscores.append(name_score)
        # ----------------------------------------------------------
        self.top_10_scores = sorted(
                                    self.highscores,
                                    key=lambda x: x.score,
                                    reverse=True
                                   )[:10]
        # ----------------------------------------------------------
        return None

    # =========================================================================
    def save_top_10_scores(self) -> None:
        # transforme the top_10_scores_obj to list of dict for save it to json
        top_10_scores_dicts: List[Dict[str, int]] = [
                                                    i.model_dump()
                                                    for i in self.top_10_scores
                                                    ]
        # ------------ read and overrite the highscore JSON file --------------
        with open(self.highscores_path, 'w') as f:
            json.dump(top_10_scores_dicts, f, indent=2)
        # ---------------------------------------------------------------------
        return None
