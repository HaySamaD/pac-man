from dataclasses import dataclass
from pydantic import BaseModel, Field, model_validator
from typing import List, Any
from src.m0_helpers import Color
from src.m0_helpers import Default_conf


@dataclass
class Position:
    """ object prosition (x, y) on maze. """
    x: int
    y: int


# ========================= the config file parser ============================

class Levels(BaseModel):

    width: int = Field(ge=9)
    height: int = Field(ge=7)
    pacgum: int = Field(ge=1)

    @model_validator(mode="before")
    @classmethod
    def validate_raw_dic(cls, dic: Any) -> Any:

        # ------------------ check the type of the input --------------------
        if not isinstance(dic, dict):
            print(
                    f"\n{Color().YELLOW}one of levels metadata not a dict. \n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            return {"width": 42, "height": 42, "pacgum": 42}

        # ----------- get the elements ------------
        val_width: Any = dic.get("width", None)
        val_height: Any = dic.get("height", None)
        val_pacgum: Any = dic.get("pacgum", None)

        # ----------------- handel width value -------------------------

        if val_width is None:
            print(
                    f"\n{Color().YELLOW}'width' not exist.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['width'] = 42

        elif not isinstance(val_width, int) or val_width < 9:
            print(
                    f"\n{Color().YELLOW}'width' not a integer or < 9.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}"
                 )
            dic['width'] = 42

        # ----------------- handel height value -------------------------

        if val_height is None:
            print(
                    f"\n{Color().YELLOW}'height' not exist."
                    f"default value is added{Color().WHITE}\n"
                 )
            dic['height'] = 42

        elif (not isinstance(val_height, int) or val_height < 7):
            print(
                    f"\n{Color().YELLOW}'height' not a integer or < 7."
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['height'] = 42

        # ----------------- handel pacgums value -------------------------

        if val_pacgum is None:
            print(
                    f"\n{Color().YELLOW}'pacgum' not exist."
                    f"default value is added{Color().WHITE}\n"
                 )
            dic['pacgum'] = 42

        elif not isinstance(val_pacgum, int) or val_pacgum < 1:
            print(
                    f"\n{Color().YELLOW}'pacgum' not a integer or < 1.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['pacgum'] = 42

        if val_pacgum > (val_width * val_height) - 19:
            print(
                f"\n{Color().YELLOW}'nbr of pacgums more than map capacity\n"
                f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['pacgum'] = 42

        # ----------------------------------------------------------------

        return dic


# ----------------------------

class GameConfig(BaseModel):

    highscore_filename: str
    levels_data: List[Levels]
    lives: int = Field(gt=0)
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    seed: int
    level_max_time: int

    @model_validator(mode="before")
    @classmethod
    def validate_raw_dic(cls, dic: Any) -> Any:

        highscore_filename: Any = dic.get("highscore_filename", None)
        levels_data: Any = dic.get("levels_data", None)
        lives: Any = dic.get("lives", None)
        points_per_pacgum: Any = dic.get("points_per_pacgum", None)
        points_per_super_pacgum: Any = dic.get("points_per_super_pacgum", None)
        points_per_ghost: Any = dic.get("points_per_ghost", None)
        seed: Any = dic.get("seed", None)
        level_max_time: Any = dic.get("level_max_time", None)

        # ---------------------------------------------------------------------

        if highscore_filename is None:
            print(
                    f"\n{Color().YELLOW}'highscore_filename' not exist."
                    f"default value is added{Color().WHITE}\n"
                 )
            dic['highscore_filename'] = "top_10_scores.json"

        if (
            not isinstance(highscore_filename, str)
            or not highscore_filename.endswith('.json')
           ):
            print(
                f"\n{Color().YELLOW}'highscore_filename' not valid "
                "(not str or not end with '.json').\n"
                f"{Color().GREEN}default value is added{Color().WHITE}\n"
                 )
            dic['highscore_filename'] = 'top_10_scores.json'

        # ---------------------------------------------------------------------

        if not isinstance(levels_data, list):
            print(
                    f"\n{Color().YELLOW}'levels_data' not a list.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            dic['levels_data'] = [
                                    {"width": 42, "height": 42, "pacgum": 42}
                                    for _ in range(10)
                                 ]

        elif len(levels_data) < 10:
            print(
                    f"\n{Color().YELLOW}'levels_data' less than 10.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            for _ in range(10 - len(levels_data)):
                dic['levels_data'].append(
                                        Levels(width=42, height=42, pacgum=42)
                                         )

        # ---------------------------------------------------------------------

        if lives is None:
            print(
                    f"\n{Color().YELLOW}'lives' not exist."
                    f"default value is added{Color().WHITE}\n"
                 )
            dic['lives'] = 3

        if not isinstance(lives, int) or lives < 1:
            print(
                    f"\n{Color().YELLOW}'lives' not a number or less than 1.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            dic['lives'] = 3

        # ---------------------------------------------------------------------

        if points_per_pacgum is None:
            print(
                    f"\n{Color().YELLOW}'points_per_pacgum' not exist."
                    f"default value is added{Color().WHITE}\n"
                 )
            dic['points_per_pacgum'] = 10

        if not isinstance(points_per_pacgum, int) or points_per_pacgum < 1:
            print(
                    f"\n{Color().YELLOW}'points_per_pacgum' not a number or"
                    " less than 1.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            dic['points_per_pacgum'] = 10

        # ---------------------------------------------------------------------

        if points_per_super_pacgum is None:
            print(
                    f"\n{Color().YELLOW}'points_per_super_pacgum' not exist."
                    f"default value is added{Color().WHITE}\n"
                 )
            dic['points_per_super_pacgum'] = 20

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

        # ---------------------------------------------------------------------

        if points_per_ghost is None:
            print(
                    f"\n{Color().YELLOW}'points_per_ghost' not exist."
                    f"default value is added{Color().WHITE}\n"
                 )
            dic['points_per_ghost'] = 40

        if not isinstance(points_per_ghost, int) or points_per_ghost < 1:
            print(
                    f"\n{Color().YELLOW}'ghost_points' not a number or"
                    "less than 1.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            dic['ghost_points'] = 40

        # ---------------------------------------------------------------------

        if seed is None:
            print(
                    f"\n{Color().YELLOW}'seed' not exist."
                    f"default value is added{Color().WHITE}\n"
                 )
            dic['seed'] = 42

        if not isinstance(seed, int) or seed < 1:
            print(
                    f"\n{Color().YELLOW}'seed' not a number or"
                    "less than 1.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            dic['seed'] = 42

        # ---------------------------------------------------------------------

        if level_max_time is None:
            print(
                    f"\n{Color().YELLOW}'level_max_time' not exist."
                    f"default value is added{Color().WHITE}\n"
                 )
            dic['level_max_time'] = 300

        if not isinstance(level_max_time, int) or level_max_time < 1:
            print(
                    f"\n{Color().YELLOW}'level_max_time' not a number or"
                    "less than 1.\n"
                    f"{Color().GREEN}add a default level data{Color().WHITE}\n"
                 )
            dic['level_max_time'] = 300

        return dic


# ========================================

@dataclass
class GameState:
    """ state of the game per status. """
    score: int = 0
    lives: int = 3
    level: int = 1
    time_left: int = 90
    status: str = "MENU"  # MENU, PLAYING, PAUSED, GAME_OVER, VICTORY


# =============================

@dataclass
class Player:
    """ player metadata. """
    position: Position
    direction: str = "RIGHT"
    is_alive: bool = True


# =============================

@dataclass
class Ghost:
    """ ghost metadata """
    position: Position
    ghost_type: str  # blinky, pinky, inky, clyde
    is_edible: bool = False
    direction: str = "UP"
