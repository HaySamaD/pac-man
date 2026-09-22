from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import List


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
