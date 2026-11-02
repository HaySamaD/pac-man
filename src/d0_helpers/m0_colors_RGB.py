"""Defines terminal color codes and Pygame RGB color tuples."""

from typing import Tuple


# change terminal color
class Color:
    """ Terminal text coloring"""
    RED = "\033[31m"
    YELLOW = '\033[93m'
    GREEN = "\033[32m"
    WHITE = "\033[37m"


# change pygame text color
class Rgb:
    """ RGB colors for pygame"""
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    YELLOW: Tuple[int, int, int] = (255, 255, 0)
    PINK: Tuple[int, int, int] = (255, 192, 203)
    BLACK: Tuple[int, int, int] = (12, 12, 16)
    RED: Tuple[int, int, int] = (255, 0, 0)
    ORANGE: Tuple[int, int, int] = (255, 165, 0)
