from dataclasses import dataclass


@dataclass
class Position:
    """ object prosition (x, y) on maze. """
    x: int
    y: int


# ========================================

@dataclass
class GameState:
    """ state of the game per status. """
    score: int = 0
    lives: int = 3
    level: int = 1
    time_left: int = 90
    status: str = "MENU"
    # MENU, PLAYING, PAUSED, GAME_OVER, VICTORY, HIGHSCORES, INSTRUCTIONS


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


@dataclass
class Flags:
    menu: bool = False
    start_game: bool = False
    highscores: bool = False
    INSTRUCTIONS: bool = False
