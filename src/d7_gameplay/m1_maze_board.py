"""Maze board generation and grid state management."""

from collections import deque
import random
from typing import Deque, List, Optional, Set, Tuple

from mazegenerator import MazeGenerator

from ..d1_classes.m1_dataclasses import Direction, TileType


class MazeBoard:
    """Stores maze grid, wall bitmasks, and collectible items."""

    def __init__(
        self,
        width: int,
        height: int,
        seed: int,
        max_pacgums: int,
    ) -> None:
        """Generate maze from external package and place collectibles."""
        self.width: int = width
        self.height: int = height
        self.raw_maze: List[List[int]] = self.generate_raw_maze(
            width, height, seed
        )
        self.grid: List[List[int]] = [
            [TileType.EMPTY for _ in range(width)] for _ in range(height)
        ]
        self.remaining_pacgums: int = 0
        self.populate_collectibles(max_pacgums)

    def generate_raw_maze(
        self, width: int, height: int, seed: int
    ) -> List[List[int]]:
        """Invoke external MazeGenerator safely with fallback grid."""
        try:
            try:
                gen = MazeGenerator(
                    size=(width, height), seed=seed, perfect=False
                )
            except TypeError:
                gen = MazeGenerator(size=(width, height), seed=seed)
            raw: List[List[int]] = gen.maze
            if raw and len(raw) == height and len(raw[0]) == width:
                return raw
        except Exception:
            pass

        fallback: List[List[int]] = [[0] * width for _ in range(height)]
        for col in range(width):
            fallback[0][col] |= 1
            fallback[height - 1][col] |= 4
        for row in range(height):
            fallback[row][0] |= 8
            fallback[row][width - 1] |= 2
        return fallback

    def populate_collectibles(self, max_pacgums: int) -> None:
        """Place pacgums in corridors and super-pacgums in the 4 corners."""
        valid_paths: List[Tuple[int, int]] = []
        for y in range(self.height):
            for x in range(self.width):
                if self.raw_maze[y][x] == 15:
                    self.grid[y][x] = TileType.WALL
                else:
                    valid_paths.append((x, y))

        corners: List[Tuple[int, int]] = [
            self.find_corner_spawn(0),
            self.find_corner_spawn(1),
            self.find_corner_spawn(2),
            self.find_corner_spawn(3),
        ]
        corner_set: Set[Tuple[int, int]] = set(corners)
        regular_paths: List[Tuple[int, int]] = [
            pos for pos in valid_paths if pos not in corner_set
        ]

        count: int = len(regular_paths)
        if 0 < max_pacgums <= count:
            count = max_pacgums

        for x, y in random.sample(regular_paths, count):
            self.grid[y][x] = TileType.PACGUM
            self.remaining_pacgums += 1

        for cx, cy in corner_set:
            if not self.is_wall(cx, cy):
                self.grid[cy][cx] = TileType.SUPER_PACGUM
                self.remaining_pacgums += 1

    def is_in_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates are inside board boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_wall(self, x: int, y: int) -> bool:
        """Return True if cell is out of bounds or a solid block wall."""
        if not self.is_in_bounds(x, y):
            return True
        return self.grid[y][x] == TileType.WALL

    def can_move(self, x: int, y: int, direction: str) -> bool:
        """Check if movement from (x, y) in direction is unobstructed."""
        if direction == Direction.NONE:
            return True
        if not self.is_in_bounds(x, y):
            return False
        bit: int = Direction.WALL_BITS[direction]
        if bool(self.raw_maze[y][x] & bit):
            return False
        dx, dy = Direction.VECTORS[direction]
        return not self.is_wall(x + dx, y + dy)

    def consume_tile(self, x: int, y: int) -> Optional[int]:
        """Consume pacgum at (x, y) and decrement remaining count."""
        if not self.is_in_bounds(x, y):
            return None
        val: int = self.grid[y][x]
        if val in (TileType.PACGUM, TileType.SUPER_PACGUM):
            self.grid[y][x] = TileType.EMPTY
            self.remaining_pacgums -= 1
            return val
        return None

    def find_nearest_open(self, start_x: int, start_y: int) -> Tuple[int, int]:
        """Find closest walkable cell starting from given coordinates."""
        if not self.is_wall(start_x, start_y):
            return start_x, start_y
        queue: Deque[Tuple[int, int]] = deque([(start_x, start_y)])
        visited: Set[Tuple[int, int]] = {(start_x, start_y)}
        while queue:
            cx, cy = queue.popleft()
            if not self.is_wall(cx, cy):
                return cx, cy
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                nx, ny = cx + dx, cy + dy
                if self.is_in_bounds(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return start_x, start_y

    def find_spawn_position(self) -> Tuple[int, int]:
        """Return walkable cell nearest to the center of the maze."""
        return self.find_nearest_open(self.width // 2, self.height // 2)

    def find_corner_spawn(self, corner_index: int) -> Tuple[int, int]:
        """Return walkable cell nearest to one of the 4 corners."""
        corners: List[Tuple[int, int]] = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]
        cx, cy = corners[corner_index % 4]
        return self.find_nearest_open(cx, cy)
