"""Defines dataclasses for the game and him state management."""

from dataclasses import dataclass


# ===============================================================================

@dataclass
class Position:
    """
        Represents 2D grid coordinates (x, y) for entities.

        Attributes:
            x (int): Horizontal grid coordinate.
            y (int): Vertical grid coordinate.
    """
    x: int
    y: int


# ===============================================================================

@dataclass
class GameState:
    """
        Tracks active game state parameters and progression status.

        Attributes:
            score (int): Current player score.
            lives (int): Remaining player lives.
            level (int): Current game level index.
            time_left (int): Remaining time for the current level.
            status (str): Current game state status (MENU, PLAY, etc.).
    """
    score: int = 0
    lives: int = 3
    level: int = 1
    time_left: int = 90
    status: str = "MENU"
    # MENU, HIGHSCORES, INSTRUCTIONS, PLAY (Maze + HUD), PAUSE, LOSS,
    #                                                               WIN


# ===============================================================================

@dataclass
class Player:
    """
        Stores player position, movement direction, and status.

        Attributes:
            position (Position): Current grid position of the player.
            direction (str): Current movement direction (UP, DOWN, LEFT, RIGHT)
            is_alive (bool): Flag indicating if the player is alive.
    """
    position: Position
    direction: str = "RIGHT"
    is_alive: bool = True


# ===============================================================================

@dataclass
class Ghost:
    """
    Stores ghost position, entity type, edible state, and direction.

    Attributes:
        position (Position): Current grid position of the ghost.
        ghost_type (str): Type identifier of the ghost (blinky, pinky, etc.).
        is_edible (bool): Flag indicating if the ghost can be eaten.
        direction (str): Current movement direction of the ghost.
    """
    position: Position
    ghost_type: str  # blinky, pinky, inky, clyde
    is_edible: bool = False
    direction: str = "UP"
