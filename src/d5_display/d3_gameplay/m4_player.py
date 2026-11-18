"""Player controller handling keyboard events and item consumption."""

from typing import Optional

import pygame

from ...d2_classes import Direction, GameState, Player, TileType
from .m1_maze_board import MazeBoard
from .m3_movement import MovementController


class PlayerController(MovementController):
    """Controls playable Pac-Man movement and score updates."""

    def __init__(
        self,
        player_data: Player,
        tile_size: int = 40,
        speed: int = 2,
        points_pacgum: int = 10,
        points_super: int = 50,
    ) -> None:
        """Initialize player controller and point values."""
        super().__init__(
            player_data.position, player_data.direction, tile_size, speed
        )
        self.data: Player = player_data
        self.points_pacgum: int = points_pacgum
        self.points_super: int = points_super

    def handle_key(self, key: int) -> None:
        """Update next movement direction from KEYDOWN event."""
        if key in (pygame.K_UP, pygame.K_w):
            self.next_direction = Direction.UP
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.next_direction = Direction.DOWN
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.next_direction = Direction.LEFT
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.next_direction = Direction.RIGHT

    def respawn(self, spawn_x: int, spawn_y: int) -> None:
        """Reset player position and direction to spawn coordinates."""
        self.position.x = spawn_x
        self.position.y = spawn_y
        self.pixel_x = float(spawn_x * self.tile_size)
        self.pixel_y = float(spawn_y * self.tile_size)
        self.current_direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.data.direction = Direction.RIGHT

    def update(
        self, board: MazeBoard, game_state: GameState
    ) -> Optional[int]:
        """Advance player and consume any pacgum on the current tile."""
        if not self.data.is_alive:
            return None
        self.advance_position(board)
        self.data.direction = self.current_direction
        eaten: Optional[int] = board.consume_tile(
            self.position.x, self.position.y
        )
        if eaten == TileType.PACGUM:
            game_state.score += self.points_pacgum
        elif eaten == TileType.SUPER_PACGUM:
            game_state.score += self.points_super
        return eaten
