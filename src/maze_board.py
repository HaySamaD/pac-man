from enum import IntEnum
from dataclasses import dataclass
from typing import Optional
import random


class TileType(IntEnum):
    EMPTY = 0
    WALL = 1
    PACGUM = 2
    SUPER_PACGUM = 3


@dataclass
class MazeBoard:
    width: int
    height: int
    grid: list[list[int]]
    raw_maze: list[list[int]]
    remaining_pacgums: int = 0

    @classmethod
    def from_raw_maze(
                        cls,
                        raw_maze: list[list[int]],
                        max_pacgums: Optional[int] = None
                    ) -> "MazeBoard":

        height = len(raw_maze)
        width = len(raw_maze[0])
        grid = [[int(TileType.EMPTY) 
                 for _ in range(width)] for _ in range(height)]
        valid_paths: list[tuple[int, int]] = []

        for y in range(height):
            for x in range(width):
                if raw_maze[y][x] == 15:
                    grid[y][x] = TileType.WALL
                else:
                    valid_paths.append((x, y))

        corners = [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1),
        ]
        corner_set = set(corners)
        regular_paths = [pos for pos in valid_paths if pos not in corner_set]

        total_available = len(regular_paths)
        if max_pacgums is not None:
            if 0 < max_pacgums < total_available:
                target_count = max_pacgums
            else :
                print(
                    "[CONFIG WARNING] Invalid max_pacgums value "
                    f"({max_pacgums}).\n    Must be between 1 and "
                    f"{total_available}.\n    Falling back to default "
                    f"({total_available})."
                )
                target_count = total_available
        else:
            target_count = total_available

        selected_paths = random.sample(regular_paths, target_count)
        gums_count = 0
        for x, y in selected_paths:
            grid[y][x] = TileType.PACGUM
            gums_count += 1

        for cx, cy in corners:
            if 0 <= cy < height and 0 <= cx < width:
                if grid[cy][cx] != TileType.WALL:
                    grid[cy][cx] = TileType.SUPER_PACGUM
                    gums_count += 1

        return cls(
            width=width,
            height=height,
            grid=grid,
            raw_maze=raw_maze,
            remaining_pacgums=gums_count,
        )
