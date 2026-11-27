"""Maze board generation and grid state management."""

from collections import deque
import random
from typing import Deque, List, Optional, Set, Tuple

from mazegenerator import MazeGenerator

from ...d2_classes import Direction, TileType

CARDINAL: Tuple[str, str, str, str] = (
    Direction.UP,
    Direction.LEFT,
    Direction.DOWN,
    Direction.RIGHT,
)


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
            [TileType.EMPTY] * width for _ in range(height)
        ]
        self.remaining_pacgums: int = 0
        self.populate_collectibles(max_pacgums)

    def generate_raw_maze(
        self, width: int, height: int, seed: int
    ) -> List[List[int]]:
        """Invoke external MazeGenerator safely with fallback grid."""
        gen = MazeGenerator(
            size=(width, height), seed=seed, perfect=False
        )
        raw: List[List[int]] = gen.maze
        return raw

    def populate_collectibles(self, max_pacgums: int) -> None:
        """Place pacgums in corridors and super-pacgums in the 4 corners."""
        paths: List[Tuple[int, int]] = []
        for y in range(self.height):
            for x in range(self.width):
                if self.raw_maze[y][x] == 15:
                    self.grid[y][x] = TileType.WALL
                else:
                    paths.append((x, y))

        corners = {self.find_corner_spawn(i) for i in range(4)}
        regular = [pos for pos in paths if pos not in corners]
        count = min(max_pacgums, len(regular))

        for x, y in random.sample(regular, count):
            self.grid[y][x] = TileType.PACGUM
            self.remaining_pacgums += 1

        for cx, cy in corners:
            if not self.is_wall(cx, cy):
                self.grid[cy][cx] = TileType.SUPER_PACGUM
                self.remaining_pacgums += 1

    def is_in_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates are inside board boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_wall(self, x: int, y: int) -> bool:
        """Return True if cell is out of bounds or a solid block wall."""
        return not self.is_in_bounds(x, y) or self.grid[y][x] == TileType.WALL

    def can_move(self, x: int, y: int, direction: str) -> bool:
        """Check if movement from (x, y) in direction is unobstructed."""
        if direction == Direction.NONE:
            return True
        if (
            not self.is_in_bounds(x, y)
            or self.raw_maze[y][x] & Direction.WALL_BITS[direction]
        ):
            return False
        dx, dy = Direction.VECTORS[direction]
        return not self.is_wall(x + dx, y + dy)

    def consume_tile(self, x: int, y: int) -> Optional[int]:
        """Consume pacgum at (x, y) and decrement remaining count."""
        if not self.is_in_bounds(x, y):
            return None
        val = self.grid[y][x]
        if val in (TileType.PACGUM, TileType.SUPER_PACGUM):
            self.grid[y][x] = TileType.EMPTY
            self.remaining_pacgums -= 1
            return val
        return None

    def find_nearest_open(self, start_x: int, start_y: int) -> Tuple[int, int]:
        """Find closest walkable cell starting from given coordinates."""
        sx = max(0, min(self.width - 1, start_x))
        sy = max(0, min(self.height - 1, start_y))
        queue: Deque[Tuple[int, int]] = deque([(sx, sy)])
        visited: Set[Tuple[int, int]] = {(sx, sy)}

        while queue:
            cx, cy = queue.popleft()
            if not self.is_wall(cx, cy):
                return cx, cy
            for d in CARDINAL:
                dx, dy = Direction.VECTORS[d]
                nx, ny = cx + dx, cy + dy
                if self.is_in_bounds(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return sx, sy

    def find_spawn_position(self) -> Tuple[int, int]:
        """Return center walkable cell and clear any pacgum on it."""
        x, y = self.find_nearest_open(self.width // 2, self.height // 2)
        self.consume_tile(x, y)
        return x, y

    def find_corner_spawn(self, corner_index: int) -> Tuple[int, int]:
        """Return walkable cell nearest to one of the 4 corners."""
        corners = (
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        )
        return self.find_nearest_open(*corners[corner_index])
