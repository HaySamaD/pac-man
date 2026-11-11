"""Maze board representation and grid state management."""

from collections import deque
from dataclasses import dataclass
from enum import IntEnum
import random
from typing import Deque, List, Optional, Set, Tuple


class TileType(IntEnum):
    """Numerical identification of contents located within a grid tile."""

    EMPTY = 0
    WALL = 1
    PACGUM = 2
    SUPER_PACGUM = 3


@dataclass
class MazeBoard:
    """Store grid cell data, raw bitmask layout, and collectibles."""

    width: int
    height: int
    grid: List[List[int]]
    raw_maze: List[List[int]]
    remaining_pacgums: int = 0
    total_pacgums: int = 0

    @classmethod
    def from_raw_maze(
        cls,
        raw_maze: List[List[int]],
        max_pacgums: Optional[int] = None,
    ) -> "MazeBoard":
        """Build and populate a MazeBoard instance from generator data."""
        if not raw_maze or not raw_maze[0]:
            raise ValueError("Raw maze data cannot be empty.")

        height: int = len(raw_maze)
        width: int = len(raw_maze[0])

        if any(len(row) != width for row in raw_maze):
            raise ValueError("Raw maze matrix contains uneven row lengths.")

        grid: List[List[int]] = [
            [int(TileType.EMPTY) for _ in range(width)]
            for _ in range(height)
        ]
        valid_paths: List[Tuple[int, int]] = []

        for y in range(height):
            for x in range(width):
                if raw_maze[y][x] == 15:
                    grid[y][x] = int(TileType.WALL)
                else:
                    valid_paths.append((x, y))

        corners: List[Tuple[int, int]] = [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1),
        ]
        corner_set: Set[Tuple[int, int]] = set(corners)

        regular_paths: List[Tuple[int, int]] = [
            pos for pos in valid_paths if pos not in corner_set
        ]

        target_count: int = len(regular_paths)
        if max_pacgums is not None and 0 < max_pacgums <= target_count:
            target_count = max_pacgums

        selected_paths: List[Tuple[int, int]] = random.sample(
            regular_paths, target_count
        )

        gums_count: int = 0
        for x, y in selected_paths:
            grid[y][x] = int(TileType.PACGUM)
            gums_count += 1

        for cx, cy in corners:
            if 0 <= cy < height and 0 <= cx < width:
                if grid[cy][cx] != int(TileType.WALL):
                    grid[cy][cx] = int(TileType.SUPER_PACGUM)
                    gums_count += 1

        return cls(
            width=width,
            height=height,
            grid=grid,
            raw_maze=raw_maze,
            remaining_pacgums=gums_count,
            total_pacgums=gums_count,
        )

    def is_in_bounds(self, x: int, y: int) -> bool:
        """Check whether a given coordinate falls inside board limits."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_wall(self, x: int, y: int) -> bool:
        """Determine whether a given coordinate holds a solid obstacle wall."""
        if not self.is_in_bounds(x, y):
            return True
        return self.grid[y][x] == int(TileType.WALL)

    def has_wall_bit(self, x: int, y: int, wall_bit: int) -> bool:
        """Inspect whether a cell's bitmask blocks a directional border."""
        if not self.is_in_bounds(x, y):
            return True
        return bool(self.raw_maze[y][x] & wall_bit)

    def get_tile(self, x: int, y: int) -> TileType:
        """Retrieve the tile type value at the specified coordinate."""
        if not self.is_in_bounds(x, y):
            return TileType.WALL
        return TileType(self.grid[y][x])

    def consume_tile(self, x: int, y: int) -> Optional[TileType]:
        """Eat collectible item at (x, y), clearing cell and updating count."""
        if not self.is_in_bounds(x, y):
            return None

        tile_val: int = self.grid[y][x]
        if tile_val in (int(TileType.PACGUM), int(TileType.SUPER_PACGUM)):
            self.grid[y][x] = int(TileType.EMPTY)
            self.remaining_pacgums -= 1
            return TileType(tile_val)

        return None

    def _find_nearest_walkable(
        self, start_x: int, start_y: int
    ) -> Tuple[int, int]:
        """Find nearest walkable corridor tile to origin via BFS."""
        if not self.is_wall(start_x, start_y):
            return start_x, start_y

        queue: Deque[Tuple[int, int]] = deque([(start_x, start_y)])
        visited: Set[Tuple[int, int]] = {(start_x, start_y)}

        while queue:
            curr_x, curr_y = queue.popleft()
            if not self.is_wall(curr_x, curr_y):
                return curr_x, curr_y

            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                nx, ny = curr_x + dx, curr_y + dy
                if self.is_in_bounds(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

        return start_x, start_y

    def find_spawn_position(self) -> Tuple[int, int]:
        """Find nearest walkable corridor cell to the maze center via BFS."""
        return self._find_nearest_walkable(self.width // 2, self.height // 2)

    def find_corner_spawn(self, corner_index: int) -> Tuple[int, int]:
        """Find safe walkable corridor cell at or near a designated corner."""
        corners: List[Tuple[int, int]] = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]
        cx, cy = corners[corner_index % 4]
        return self._find_nearest_walkable(cx, cy)

    def walkable_tiles(self) -> List[Tuple[int, int]]:
        """Return sorted list of all non-wall tile coordinates."""
        return [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if not self.is_wall(x, y)
        ]
