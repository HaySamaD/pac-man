"""Base movement controller for grid-aligned entities."""

from typing import Tuple

from ..d1_classes.m1_dataclasses import Direction, Position
from .m1_maze_board import MazeBoard


class MovementController:
    """Manages pixel coordinates, corridor turning, and wall collisions."""

    def __init__(
        self,
        position: Position,
        direction: str,
        tile_size: int = 40,
        speed: int = 2,
    ) -> None:
        """Initialize movement state and pixel positions."""
        self.position: Position = position
        self.current_direction: str = direction
        self.next_direction: str = direction
        self.tile_size: int = tile_size
        self.speed: int = speed
        self.pixel_x: float = float(position.x * tile_size)
        self.pixel_y: float = float(position.y * tile_size)
        self.anim_frame: int = 0
        self.anim_counter: int = 0

    def get_grid_coords(self) -> Tuple[int, int]:
        """Return rounded grid coordinates from current pixel position."""
        gx: int = int(round(self.pixel_x / self.tile_size))
        gy: int = int(round(self.pixel_y / self.tile_size))
        return gx, gy

    def distance_sq(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Compute squared Euclidean distance between two points."""
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def advance_position(self, board: MazeBoard) -> None:
        """Move entity along corridors and align on intersections."""
        ts: int = self.tile_size
        gx, gy = self.get_grid_coords()
        target_px: float = float(gx * ts)
        target_py: float = float(gy * ts)
        dist_x: float = abs(self.pixel_x - target_px)
        dist_y: float = abs(self.pixel_y - target_py)

        opp: str = Direction.OPPOSITES[self.current_direction]
        if self.next_direction == opp and self.next_direction != Direction.NONE:
            self.current_direction = self.next_direction
        elif (
            self.next_direction != self.current_direction
            and dist_x <= self.speed
            and dist_y <= self.speed
        ):
            if board.can_move(gx, gy, self.next_direction):
                self.pixel_x = target_px
                self.pixel_y = target_py
                self.current_direction = self.next_direction

        dx, dy = Direction.VECTORS[self.current_direction]
        past_center: bool = (
            (dx > 0 and self.pixel_x >= target_px)
            or (dx < 0 and self.pixel_x <= target_px)
            or (dy > 0 and self.pixel_y >= target_py)
            or (dy < 0 and self.pixel_y <= target_py)
        )
        can_go: bool = not past_center or board.can_move(
            gx, gy, self.current_direction
        )

        if can_go and self.current_direction != Direction.NONE:
            self.pixel_x += dx * self.speed
            self.pixel_y += dy * self.speed
            self.anim_counter += 1
            if self.anim_counter % 6 == 0:
                self.anim_frame = (self.anim_frame + 1) % 4
        else:
            self.pixel_x = target_px
            self.pixel_y = target_py
            self.current_direction = Direction.NONE

        self.position.x = int(round(self.pixel_x / ts))
        self.position.y = int(round(self.pixel_y / ts))
