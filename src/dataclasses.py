from dataclasses import dataclass
from pydantic import BaseModel, Field, model_validator
from typing import List, Dict


@dataclass
class Position:
    """ object prosition (x, y) on maze. """
    x: int
    y: int


# === the config file parser ===

class Levels(BaseModel):

    width: int = Field(ge=9)
    height: int = Field(ge=7)
    pacgum: int = Field(ge=1)

    @model_validator(mode="before")
    @classmethod
    def validate_raw_dic(cls, dic: Dict[str, int]) -> Dict[str, int]:

        # ----------------------------------------------------------------

        if dic.get("width", None) is None:
            print("width not exist. default value is added")
            dic["width"] = 20

        elif (
                not isinstance(dic.get("width", None), int) or
                dic.get("width", None) < 9
             ):
            print("width not a integer or < 9. default value is added")
            dic["width"] = 20

        # ----------------------------------------------------------------

        if dic.get("height", None) is None:
            print("height not exist. default value is added")
            dic["height"] = 20

        elif (
                not isinstance(dic.get("height", None), int) or
                dic.get("height", None) < 7
             ):
            print("height not a integer or < 7. default value is added")
            dic["height"] = 20

        # ----------------------------------------------------------------

        if dic.get("pacgum", None) is None:
            print("pacgum not exist. default value is added")
            dic["pacgum"] = 20

        elif (
                not isinstance(dic.get("pacgum", None), int) or
                dic.get("pacgum", None) < 1
             ):
            print("pacgum not a integer or < 1. default value is added")
            dic["pacgum"] = 20

        # ----------------------------------------------------------------

        return dic


# ----------------------------

class GameConfig(BaseModel):

    highscore_file: str
    levels_data: List[Levels]
    lives: int = Field(gt=0)
    pacgum_points: int
    super_pacgum_points: int
    ghost_points: int
    seed: int
    level_max_time: int


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
