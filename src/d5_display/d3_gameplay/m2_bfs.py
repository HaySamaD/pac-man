"""Breadth-First Search pathfinding algorithm for maze navigation."""

from collections import deque
from typing import Deque, Dict, Set, Tuple

from ...d2_classes import Direction
from .m1_maze_board import MazeBoard


class Bfs:
    """Provides grid pathfinding and walkable tile resolution via BFS."""

    def __init__(self) -> None:
        """Initialize BFS helper with cardinal search order."""
        self.dirs: Tuple[str, str, str, str] = (
            Direction.UP,
            Direction.LEFT,
            Direction.DOWN,
            Direction.RIGHT,
        )

    def find_nearest_walkable(
        self,
        board: MazeBoard,
        target_x: int,
        target_y: int,
    ) -> Tuple[int, int]:
        """Locate closest non-wall tile to given target coordinates."""
        cx: int = max(0, min(board.width - 1, target_x))
        cy: int = max(0, min(board.height - 1, target_y))
        if not board.is_wall(cx, cy):
            return cx, cy

        queue: Deque[Tuple[int, int]] = deque([(cx, cy)])
        visited: Set[Tuple[int, int]] = {(cx, cy)}
        while queue:
            x, y = queue.popleft()
            if not board.is_wall(x, y):
                return x, y
            for d in self.dirs:
                dx, dy = Direction.VECTORS[d]
                nx, ny = x + dx, y + dy
                if board.is_in_bounds(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return cx, cy

    def get_distance_map(
        self,
        board: MazeBoard,
        target_x: int,
        target_y: int,
    ) -> Dict[Tuple[int, int], int]:
        """Compute shortest corridor step distance from all cells to target."""
        tx, ty = self.find_nearest_walkable(board, target_x, target_y)
        queue: Deque[Tuple[int, int]] = deque([(tx, ty)])
        dist: Dict[Tuple[int, int], int] = {(tx, ty): 0}

        while queue:
            cx, cy = queue.popleft()
            cur_dist: int = dist[(cx, cy)]
            for d in self.dirs:
                dx, dy = Direction.VECTORS[d]
                nx, ny = cx + dx, cy + dy
                opp: str = Direction.OPPOSITES[d]
                if (
                    board.is_in_bounds(nx, ny)
                    and (nx, ny) not in dist
                    and board.can_move(nx, ny, opp)
                ):
                    dist[(nx, ny)] = cur_dist + 1
                    queue.append((nx, ny))
        return dist
