from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Position:
    """ object prosition (x, y) on maze. """
    x: int
    y: int


@dataclass
class GameConfig:
    """ JSON config data. """
    highscore_file: str = "highscores.json"
    levels_data: List[Dict] = [
                                {'width': 20, 'height': 20, "n_pacgum": 381}
                                for _ in range(10)
                              ]
    lives: int = 3
    pacgum_points: int = 10
    super_pacgum_points: int = 50
    ghost_points: int = 200
    seed: int = 42
    level_max_time: int = 90


@dataclass
class GameState:
    """ state of the game per status. """
    score: int = 0
    lives: int = 3
    level: int = 1
    time_left: int = 90
    status: str = "MENU"  # MENU, PLAYING, PAUSED, GAME_OVER, VICTORY


@dataclass
class Player:
    """ player metadata. """
    position: Position
    direction: str = "RIGHT"
    is_alive: bool = True


@dataclass
class Ghost:
    """ ghost metadata """
    position: Position
    ghost_type: str  # blinky, pinky, inky, clyde
    is_edible: bool = False
    direction: str = "UP"
