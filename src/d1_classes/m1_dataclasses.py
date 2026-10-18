"""Shared dataclasses and enumerations for game state, entities, and tiles."""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class Direction(str, Enum):
    """
    Movement directions combining string representation and coordinate vectors.

    Inheriting from (str, Enum) ensures string compatibility while providing
    type-safe direction management and mathematical delta vectors.
    """

    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    NONE = "NONE"

    @property
    def vector(self) -> Tuple[int, int]:
        """Return the (dx, dy) movement offset on the grid."""
        vectors = {
            Direction.UP: (0, -1),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0),
            Direction.NONE: (0, 0),
        }
        return vectors[self]

    @property
    def wall_bit(self) -> int:
        """Return the bitmask wall value (1=North, 2=East, 4=South, 8=West)."""
        bits = {
            Direction.UP: 1,
            Direction.RIGHT: 2,
            Direction.DOWN: 4,
            Direction.LEFT: 8,
            Direction.NONE: 0,
        }
        return bits[self]

    @property
    def opposite(self) -> "Direction":
        """Return the exact reverse direction."""
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
            Direction.NONE: Direction.NONE,
        }
        return opposites[self]


class GhostType(str, Enum):
    """The four classic ghost personalities."""

    BLINKY = "blinky"
    PINKY = "pinky"
    INKY = "inky"
    CLYDE = "clyde"


class GameStatus(str, Enum):
    """Game loop progression states."""

    MENU = "MENU"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"
    VICTORY = "VICTORY"


# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class Position:
    """Object position (x, y) on the grid board."""

    x: int
    y: int


@dataclass
class GameState:
    """State of the game progression and metrics."""

    score: int = 0
    lives: int = 3
    level: int = 1
    time_left: int = 90
    status: GameStatus = GameStatus.MENU


@dataclass
class Player:
    """Player runtime entity data."""

    position: Position
    direction: Direction = Direction.RIGHT
    is_alive: bool = True


@dataclass
class Ghost:
    """Ghost runtime entity data."""

    position: Position
    ghost_type: GhostType
    is_edible: bool = False
    direction: Direction = Direction.UP
