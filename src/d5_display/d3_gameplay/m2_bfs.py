"""Breadth-First Search pathfinding algorithm for maze navigation."""

from collections import deque
from typing import Deque, Dict, Tuple

from ...d2_classes import Direction
from .m1_maze_board import MazeBoard


class Bfs:
    """Provides shortest-path distance maps across maze corridors."""

    def __init__(self) -> None:
        """Initialize BFS helper with cardinal search order."""
        self.dirs: Tuple[str, str, str, str] = (
            Direction.UP,
            Direction.LEFT,
            Direction.DOWN,
            Direction.RIGHT,
        )

    def get_distance_map(
        self,
        board: MazeBoard,
        target_x: int,
        target_y: int,
    ) -> Dict[Tuple[int, int], int]:
        """Compute shortest corridor step distance from all cells to target."""
        tx, ty = board.find_nearest_open(target_x, target_y)
        queue: Deque[Tuple[int, int]] = deque([(tx, ty)])
        dist: Dict[Tuple[int, int], int] = {(tx, ty): 0}

        while queue:
            cx, cy = queue.popleft()
            next_dist = dist[(cx, cy)] + 1
            for d in self.dirs:
                dx, dy = Direction.VECTORS[d]
                nx, ny = cx + dx, cy + dy
                if (
                    board.is_in_bounds(nx, ny)
                    and (nx, ny) not in dist
                    and board.can_move(nx, ny, Direction.OPPOSITES[d])
                ):
                    dist[(nx, ny)] = next_dist
                    queue.append((nx, ny))
        return dist
