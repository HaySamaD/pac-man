"""Base movement controller for grid-aligned entities."""

from typing import Tuple

from ...d2_classes import Direction, Position
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
        return (
            int(round(self.pixel_x / self.tile_size)),
            int(round(self.pixel_y / self.tile_size)),
        )

    def set_grid_pos(self, gx: int, gy: int) -> None:
        """Snap both grid and pixel coordinates to a specific tile."""
        self.position.x = gx
        self.position.y = gy
        self.pixel_x = float(gx * self.tile_size)
        self.pixel_y = float(gy * self.tile_size)

    def is_near_center(self) -> bool:
        """Return True when entity is aligned near its current tile center."""
        gx, gy = self.get_grid_coords()
        return (
            abs(self.pixel_x - gx * self.tile_size) <= self.speed
            and abs(self.pixel_y - gy * self.tile_size) <= self.speed
        )

    def distance_sq(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Compute squared Euclidean distance between two points."""
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def advance_position(self, board: MazeBoard) -> None:
        """Move entity along corridors and align on intersections."""
        gx, gy = self.get_grid_coords()
        tx: float = float(gx * self.tile_size)
        ty: float = float(gy * self.tile_size)
        opp: str = Direction.OPPOSITES[self.current_direction]

        if (
            self.next_direction != Direction.NONE
            and self.next_direction == opp
        ):
            self.current_direction = self.next_direction
        elif (
            self.next_direction != self.current_direction
            and self.is_near_center()
            and board.can_move(gx, gy, self.next_direction)
        ):
            self.pixel_x, self.pixel_y = tx, ty
            self.current_direction = self.next_direction

        dx, dy = Direction.VECTORS[self.current_direction]
        past_center: bool = (
            dx * (self.pixel_x - tx) + dy * (self.pixel_y - ty) >= 0
        )
        can_go: bool = (
            not past_center
            or board.can_move(gx, gy, self.current_direction)
        )
        if self.current_direction != Direction.NONE and can_go:
            self.pixel_x += dx * self.speed
            self.pixel_y += dy * self.speed
            self.anim_counter += 1
            if self.anim_counter % 6 == 0:
                self.anim_frame = (self.anim_frame + 1) % 4
        else:
            self.pixel_x, self.pixel_y = tx, ty
            self.current_direction = Direction.NONE

        self.position.x, self.position.y = self.get_grid_coords()
