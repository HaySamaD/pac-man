from dataclasses import dataclass
from pydantic import BaseModel, Field, model_validator
from typing import List, Any
from src.helpers import Color


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
    def validate_raw_dic(cls, dic: Any) -> Any:

        # ------------------ check the type of the input --------------------
        if not isinstance(dic, dict):
            print(
                    f"{Color().YELLOW}one of levels metadata not a dict. \n"
                    f"{Color().GREEN}default value is added{Color().WHITE}"
                 )
            return {"width": 20, "height": 20, "pacgum": 42}

        # ----------- get the elements ------------
        val_width: Any = dic.get("width", None)
        val_height: Any = dic.get("height", None)
        val_pacgum: Any = dic.get("pacgum", None)

        # ----------------- handel width value -------------------------

        if val_width is None:
            print(
                    f"{Color().YELLOW}width not exist.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}"
                 )
            dic["width"] = 20

        elif not isinstance(val_width, int) or val_width < 9:
            print(
                    f"{Color().YELLOW}width not a integer or < 9.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}"
                 )
            dic["width"] = 20

        # ----------------- handel height value -------------------------

        if val_height is None:
            print("height not exist. default value is added")
            dic["height"] = 20

        elif (not isinstance(val_height, int) or val_height < 7):
            print(
                    f"{Color().YELLOW}height not a integer or < 7."
                    f"{Color().GREEN}default value is added{Color().WHITE}"
                 )
            dic["height"] = 20

        # ----------------- handel pacgums value -------------------------

        if val_pacgum is None:
            print("pacgum not exist. default value is added")
            dic["pacgum"] = 20

        elif not isinstance(val_pacgum, int) or val_pacgum < 1:
            print(
                    f"{Color().YELLOW}pacgum not a integer or < 1.\n"
                    f"{Color().GREEN}default value is added{Color().WHITE}"
                 )
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
