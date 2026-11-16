"""
    Defines Pydantic models for validating game configuration,
                                                        levels, and highscores.
"""

from pydantic import BaseModel, model_validator

from typing import List, Dict, Any

from ..d0_helpers import Color


# =============== The subclass of the gameconfig class (bellow) ===============

class Level(BaseModel):
    """
        Validates individual level parameters (dimensions and pacgum count).

        Attributes:
            width (int): Width of the maze grid.
            height (int): Height of the maze grid.
            pacgum (int): Number of pacgums in the level.
    """

    width: int
    height: int
    pacgum: int

    # ------------- parce the dict before impaking (mode=before) --------------
    @model_validator(mode="before")
    @classmethod
    def validate_raw_dic(cls, dic: Any) -> Dict[str, Any]:
        """
            Validates and return raw level dictionary data before model
                                                                    creation.

            Args:
                dic (Any): Raw input data to validate.

            Returns:
                Dict[str, Any]: Validated dictionary with safe defaults if
                                                                    invalid.
        """
        # ----------- check the type of the input (if dict or not) ------------
        if not isinstance(dic, dict):
            print(
                    f"\n{Color().YELLOW}One of levels metadata not a dict. \n"
                    f"{Color().GREEN}Default value is added{Color().WHITE}\n"
                 )
            return {"width": 42, "height": 42, "pacgum": 42}
        # ----------------------- get the dic elements ------------------------
        val_width: Any = dic.get("width", None)
        val_height: Any = dic.get("height", None)
        val_pacgum: Any = dic.get("pacgum", None)
        # ------------------------ handel width value -------------------------
        if val_width is None:
            print(
                    f"\n{Color().YELLOW}'width' not exist.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['width'] = 42
            val_width = 42
        # the maze must be >= 14 (to display the 42 pattern)
        # and <= 48 (to display the full maze in screen)
        elif not isinstance(val_width, int) or not (14 <= val_width <= 48):
            print(
                f"\n{Color().YELLOW}'width' not a integer or out of [14, 48]."
                f"\n{Color().GREEN}default value is added{Color().WHITE}"
                 )
            dic['width'] = 42
        # ------------------------ handel height value ------------------------
        if val_height is None:
            print(
                    f"\n{Color().YELLOW}'height' not exist."
                    f"\n{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['height'] = 42
            val_height = 42
        # the maze must be >= 10 (to display the 42 pattern)
        # and <= 24 (to less space for HUD + display the full maze in screen)
        elif not isinstance(val_height, int) or not (10 <= val_height <= 24):
            print(
                    f"\n{Color().YELLOW}'height' not a int or out of [10, 24]."
                    f"\n{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['height'] = 42
        # ------------------------ handel pacgums value -----------------------
        if val_pacgum is None:
            print(
                    f"\n{Color().YELLOW}'pacgum' not exist.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['pacgum'] = 42
            val_pacgum = 42
        elif not isinstance(val_pacgum, int) or val_pacgum < 1:
            print(
                    f"\n{Color().YELLOW}'pacgum' not a integer or < 1.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['pacgum'] = 42
            val_pacgum = 42
        elif val_pacgum > (dic['width'] * dic['height']) - 23:
            print(
                f"\n{Color().YELLOW}'nbr of pacgums more than map capacity "
                f"must be btwn 1 and {(dic['width'] * dic['height']) - 23}"
                f"\n{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['pacgum'] = 42
            val_pacgum = 42
        # ---------------------------------------------------------------------
        return dic


# ===============================================================================

class Config(BaseModel):
    """
        Validates overall game configuration settings loaded from JSON.

        Attributes:
            highscore_filename (str): File path for highscore data storage.
            levels_data (List[Level]): List of level configurations.
            lives (int): Initial player lives count.
            points_per_pacgum (int): Points awarded per regular pacgum.
            points_per_super_pacgum (int): Points awarded per super pacgum.
            points_per_ghost (int): Points awarded per eaten ghost.
            seed (int): Random seed for level generation.
            level_max_time (int): Maximum time limit per level in seconds.
    """

    highscore_filename: str
    levels_data: List[Level]
    lives: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    seed: int
    level_max_time: int

    # ------------- parce the dict before impaking (mode=before) --------------
    @model_validator(mode="before")
    @classmethod
    def validate_raw_dic(cls, dic: Any) -> Any:
        """
            Validates raw configuration dictionary data.

            Args:
                dic (Any): Raw configuration input data.

            Returns:
                Any: Validated configuration dictionary with fallback defaults.
        """
        # ----------------------- get the dic elements ------------------------
        highscore_filename: Any = dic.get("highscore_filename", None)
        levels_data: Any = dic.get("levels_data", None)
        lives: Any = dic.get("lives", None)
        points_per_pacgum: Any = dic.get("points_per_pacgum", None)
        points_per_super_pacgum: Any = dic.get("points_per_super_pacgum", None)
        points_per_ghost: Any = dic.get("points_per_ghost", None)
        seed: Any = dic.get("seed", None)
        level_max_time: Any = dic.get("level_max_time", None)
        # --------------------- handel highscore_filename ---------------------
        if highscore_filename is None:
            print(
                    f"\n{Color().YELLOW}'highscore_filename' not exist.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['highscore_filename'] = "highscores.json"
            highscore_filename = dic['highscore_filename']
        if (
            not isinstance(highscore_filename, str)
            or not highscore_filename.endswith('.json')
           ):
            print(
                f"\n{Color().YELLOW}'highscore_filename' not valid "
                "(not str or not a JSON file).\n"
                f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['highscore_filename'] = "highscores.json"
            highscore_filename = dic['highscore_filename']
        # ------------------------ handel levels_data -------------------------
        if not isinstance(levels_data, list):
            print(
                    f"\n{Color().YELLOW}'levels_data' not a list.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            dic['levels_data'] = [
                                {"width": 42, "height": 42, "pacgum": 42}
                                for _ in range(10)
                                 ]
            levels_data = dic['levels_data']
        elif len(levels_data) < 10:
            print(
                    f"\n{Color().YELLOW}'levels_data' less than 10.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            for _ in range(0, 10 - len(levels_data)):
                dic['levels_data'].append(
                                    {"width": 42, "height": 42, "pacgum": 42}
                                         )
                levels_data = dic['levels_data']
        # ---------------------- handel lives List[Dict] ----------------------
        if lives is None:
            print(
                    f"\n{Color().YELLOW}'lives' not exist.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['lives'] = 3
            lives = 3
        if not isinstance(lives, int) or lives < 1:
            print(
                    f"\n{Color().YELLOW}'lives' not a number or less than 1.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            dic['lives'] = 3
            lives = 3
        # --------------------- handel points_per_pacgum ----------------------
        if points_per_pacgum is None:
            print(
                    f"\n{Color().YELLOW}'points_per_pacgum' not exist.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['points_per_pacgum'] = 10
            points_per_pacgum = 10
        if not isinstance(points_per_pacgum, int) or points_per_pacgum < 1:
            print(
                    f"\n{Color().YELLOW}'points_per_pacgum' not a number or"
                    " less than 1.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            dic['points_per_pacgum'] = 10
            points_per_pacgum = 10
        # ------------------- handel points_per_super_pacgum ------------------
        if points_per_super_pacgum is None:
            print(
                    f"\n{Color().YELLOW}'points_per_super_pacgum' not exist.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['points_per_super_pacgum'] = 20
            points_per_super_pacgum = 20
        if (
                not isinstance(points_per_super_pacgum, int)
                or points_per_super_pacgum < 1
           ):
            print(
                    f"\n{Color().YELLOW}'points_per_super_pacgum' not a number"
                    " or less than 1.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            dic['points_per_super_pacgum'] = 20
            points_per_super_pacgum = 20
        # -------------------- handel points_per_ghost -----------------------
        if points_per_ghost is None:
            print(
                    f"\n{Color().YELLOW}'points_per_ghost' not exist.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['points_per_ghost'] = 40
            points_per_ghost = 40
        elif not isinstance(points_per_ghost, int) or points_per_ghost < 1:
            print(
                    f"\n{Color().YELLOW}'points_per_ghost' not a number or"
                    " less than 1.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            dic['points_per_ghost'] = 40
            points_per_ghost = 40
        # -------------------------- handel seed ------------------------------
        if seed is None:
            print(
                    f"\n{Color().YELLOW}'seed' not exist.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['seed'] = 42
            seed = 42
        elif not isinstance(seed, int) or seed < 1:
            print(
                    f"\n{Color().YELLOW}'seed' not a number or "
                    "less than 1.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            dic['seed'] = 42
            seed = 42
        # --------------------- handel level_max_time -------------------------
        if level_max_time is None:
            print(
                    f"\n{Color().YELLOW}'level_max_time' not exist.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['level_max_time'] = 300
            level_max_time = 300
        if not isinstance(level_max_time, int) or level_max_time < 1:
            print(
                    f"\n{Color().YELLOW}'level_max_time' not a number or"
                    "less than 1.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            dic['level_max_time'] = 300
            level_max_time = 300
        # ---------------------------------------------------------------------
        return dic


# =============== this class for validate the highscores file ===============

class NameScore(BaseModel):
    """
        Validates player name and score leaderboard entries.

        Attributes:
            name (str): Player name (alphanumeric and spaces, max 10 chars).
            score (int): Non-negative player score.
    """
    name: str
    score: int

    @model_validator(mode="before")
    @classmethod
    def valide(cls, dic: Dict[str, str | int]) -> Dict[str, str | int]:
        """
            Validates and normalizes player name and score entry.

            Args:
                dic (Dict[str, str | int]): Raw name-score dictionary.

            Returns:
                Dict[str, str | int]: Validated name-score dictionary.
        """
        # ------------- Verify first that we have a dict -------------
        if not isinstance(dic, dict):
            print(
                    f"{Color().YELLOW}{dic} not a dict."
                    f"{Color().GREEN}\nswitch to default value"
                    f"{Color().WHITE}"
                 )
            return {"name": "player", "score": 0}
        # ---- get the content of dict ----
        name: Any = dic.get("name", None)
        score: Any = dic.get("score", None)
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
        if not isinstance(score, int) or score < 0:
            print(
                    f"\n{Color().YELLOW}'{score}' is not a integer or negative"
                    f"\n{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['score'] = 0
        # -------------------------------------------------------------------
        return dic

# ==========================================================================
# Remarques:

#     - bnisba l width and height (lines 41 and 57):
#                                             a revoir l explication dialha

#     - bnisba l handllage dial nbr of pacgums (line 78):
#                                             a revoir l explication dialha
# ==========================================================================
