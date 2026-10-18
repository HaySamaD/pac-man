"""Terminal ANSI and RGB color definitions for game rendering."""

from typing import Tuple


class Color:
    """Terminal ANSI escape color strings for text formatting."""

    RED = "\033[31m"
    YELLOW = "\033[93m"
    GREEN = "\033[32m"
    WHITE = "\033[37m"


class Rgb:
    """RGB integer tuples for Pygame screen and sprite drawing."""

    WHITE: Tuple[int, int, int] = (255, 255, 255)
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    YELLOW: Tuple[int, int, int] = (255, 255, 0)
    PINK: Tuple[int, int, int] = (255, 192, 203)
    BLACK: Tuple[int, int, int] = (12, 12, 16)
    RED: Tuple[int, int, int] = (255, 0, 0)
    ORANGE: Tuple[int, int, int] = (255, 165, 0)
    WALL_BLUE: Tuple[int, int, int] = (40, 65, 135)
    BLOCK_BLUE: Tuple[int, int, int] = (30, 48, 102)
