from enum import IntEnum
from dataclasses import dataclass

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
    remaining_pacgums: int = 0

    @classmethod
    def from_raw_maze(cls, raw_maze: list[list[int]]) -> "MazeBoard":
        width = len(raw_maze)
        height = len(raw_maze)
        grid = [[int(TileType.EMPTY) for _ in range(width)] for _ in range(height)]
        gums_count = 0

        for y in range(height):
            for x in range(width):
                # kay3ni bli raha cell dyal 42
                if raw_maze[y][x] == 15:
                    grid[y][x] = TileType.WALL
                else:
                    grid[y][x] = TileType.PACGUM
                    gums_count += 1

        corners = [(1, 1), (width - 2, 1), (1, height - 2), (width - 2, height - 2)]
        for cx, cy in corners:
            if 0 <= cy < height and 0 <= cx < width and grid[cy][cx] == TileType.PACGUM:
                grid[cy][cx] = TileType.SUPER_PACGUM

        return cls(width=width, height=height, grid=grid, remaining_pacgums=gums_count)
