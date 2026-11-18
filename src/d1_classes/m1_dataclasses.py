"""Shared data structures and constants for game state and entities."""

from typing import Dict, Tuple


class Direction:
    """Movement direction constants and directional lookup tables."""

    UP: str = "UP"
    DOWN: str = "DOWN"
    LEFT: str = "LEFT"
    RIGHT: str = "RIGHT"
    NONE: str = "NONE"

    VECTORS: Dict[str, Tuple[int, int]] = {
        "UP": (0, -1),
        "DOWN": (0, 1),
        "LEFT": (-1, 0),
        "RIGHT": (1, 0),
        "NONE": (0, 0),
    }

    WALL_BITS: Dict[str, int] = {
        "UP": 1,
        "RIGHT": 2,
        "DOWN": 4,
        "LEFT": 8,
        "NONE": 0,
    }

    OPPOSITES: Dict[str, str] = {
        "UP": "DOWN",
        "DOWN": "UP",
        "LEFT": "RIGHT",
        "RIGHT": "LEFT",
        "NONE": "NONE",
    }


class TileType:
    """Numerical constants representing grid cell contents."""

    EMPTY: int = 0
    WALL: int = 1
    PACGUM: int = 2
    SUPER_PACGUM: int = 3


class Position:
    """Represents 2D grid coordinates (x, y) for entities."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize grid coordinates."""
        self.x: int = x
        self.y: int = y


class GameState:
    """Tracks active game state parameters and progression status."""

    def __init__(
        self,
        score: int = 0,
        lives: int = 3,
        level: int = 1,
        time_left: int = 90,
        status: str = "MENU",
    ) -> None:
        """Initialize game state metrics."""
        self.score: int = score
        self.lives: int = lives
        self.level: int = level
        self.time_left: int = time_left
        self.status: str = status


class Player:
    """Stores player position, movement direction, and status."""

    def __init__(
        self,
        position: Position,
        direction: str = "RIGHT",
        is_alive: bool = True,
    ) -> None:
        """Initialize player runtime data."""
        self.position: Position = position
        self.direction: str = direction
        self.is_alive: bool = is_alive


class Ghost:
    """Stores ghost position, entity type, edible state, and direction."""

    def __init__(
        self,
        position: Position,
        ghost_type: str,
        is_edible: bool = False,
        direction: str = "UP",
    ) -> None:
        """Initialize ghost runtime data."""
        self.position: Position = position
        self.ghost_type: str = ghost_type
        self.is_edible: bool = is_edible
        self.direction: str = direction
