"""Base movement controller module for movable grid entities."""

from typing import Tuple
from src.d1_classes.m1_dataclasses import Direction, Position
from src.maze_board import MazeBoard


class MovementController:
    """Base class managing grid-aligned pixel movement and wall collisions."""

    def __init__(
        self,
        position: Position,
        direction: Direction,
        tile_size: int = 40,
        speed: int = 4,
    ) -> None:
        """Initialize entity coordinates, movement vectors, and timers."""
        self.position: Position = position
        self.current_direction: Direction = direction
        self.next_direction: Direction = direction
        self.tile_size: int = tile_size
        self.speed: int = speed
        self.pixel_x: float = float(position.x * tile_size)
        self.pixel_y: float = float(position.y * tile_size)
        self.anim_frame: int = 0
        self.anim_counter: int = 0

    @staticmethod
    def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
        """Compute Manhattan grid distance between two points."""
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def euclidean_distance_sq(
        x1: float, y1: float, x2: float, y2: float
    ) -> float:
        """Calculate squared Euclidean distance between two points."""
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def can_move(
        self,
        board: MazeBoard,
        direction: Direction,
        grid_x: int,
        grid_y: int,
    ) -> bool:
        """Check whether target direction is open in the maze corridors."""
        if direction == Direction.NONE:
            return True
        if not board.is_in_bounds(grid_x, grid_y):
            return False

        if board.has_wall_bit(grid_x, grid_y, direction.wall_bit):
            return False

        delta_x, delta_y = direction.vector
        target_x: int = grid_x + delta_x
        target_y: int = grid_y + delta_y

        return not board.is_wall(target_x, target_y)

    def get_current_grid_coords(self) -> Tuple[int, int]:
        """Compute nearest rounded grid tile indices from continuous pixels."""
        gx: int = int(round(self.pixel_x / self.tile_size))
        gy: int = int(round(self.pixel_y / self.tile_size))
        return gx, gy

    def advance_pixel_position(self, board: MazeBoard) -> None:
        """Advance coordinates, align on turns, and detect collisions."""
        tile_sz: int = self.tile_size
        cur_gx, cur_gy = self.get_current_grid_coords()
        target_px: float = float(cur_gx * tile_sz)
        target_py: float = float(cur_gy * tile_sz)
        dist_x: float = abs(self.pixel_x - target_px)
        dist_y: float = abs(self.pixel_y - target_py)

        if (
            self.next_direction == self.current_direction.opposite
            and self.next_direction != Direction.NONE
        ):
            self.current_direction = self.next_direction

        elif (
            self.next_direction != self.current_direction
            and dist_x <= self.speed
            and dist_y <= self.speed
        ):
            if self.can_move(board, self.next_direction, cur_gx, cur_gy):
                self.pixel_x = target_px
                self.pixel_y = target_py
                self.current_direction = self.next_direction

        dx, dy = self.current_direction.vector
        can_continue: bool = True
        if dx > 0 and self.pixel_x >= target_px:
            can_continue = self.can_move(
                board, self.current_direction, cur_gx, cur_gy
            )
        elif dx < 0 and self.pixel_x <= target_px:
            can_continue = self.can_move(
                board, self.current_direction, cur_gx, cur_gy
            )
        if dy > 0 and self.pixel_y >= target_py:
            can_continue = self.can_move(
                board, self.current_direction, cur_gx, cur_gy
            )
        elif dy < 0 and self.pixel_y <= target_py:
            can_continue = self.can_move(
                board, self.current_direction, cur_gx, cur_gy
            )

        if can_continue and self.current_direction != Direction.NONE:
            self.pixel_x += dx * self.speed
            self.pixel_y += dy * self.speed
            self.anim_counter += 1
            if self.anim_counter % 6 == 0:
                self.anim_frame = (self.anim_frame + 1) % 4
        else:
            self.pixel_x = target_px
            self.pixel_y = target_py
            self.current_direction = Direction.NONE

        self.position.x = int(round(self.pixel_x / tile_sz))
        self.position.y = int(round(self.pixel_y / tile_sz))
