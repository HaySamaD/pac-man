"""Player controller handling keyboard events and item consumption."""

from typing import Dict, Optional

import pygame

from ...d2_classes import Config, Direction, GameState, Player, TileType
from .m1_maze_board import MazeBoard
from .m3_movement import MovementController


class PlayerController(MovementController):
    """Controls playable Pac-Man movement and score updates."""

    KEY_MAP: Dict[int, str] = {
        pygame.K_UP: Direction.UP,
        pygame.K_w: Direction.UP,
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_s: Direction.DOWN,
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_a: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
        pygame.K_d: Direction.RIGHT,
    }

    def __init__(
        self,
        player_data: Player,
        config: Config,
        tile_size: int = 40,
        speed: int = 2,
    ) -> None:
        """Initialize player controller and point values from config."""
        super().__init__(
            player_data.position, player_data.direction, tile_size, speed
        )
        self.data: Player = player_data
        self.points: Dict[int, int] = {
            TileType.PACGUM: config.points_per_pacgum,
            TileType.SUPER_PACGUM: config.points_per_super_pacgum,
        }

    def handle_key(self, key: int) -> None:
        """Update next movement direction from KEYDOWN event."""
        if key in self.KEY_MAP:
            self.next_direction = self.KEY_MAP[key]

    def respawn(self, spawn_x: int, spawn_y: int) -> None:
        """Reset player position and direction to spawn coordinates."""
        self.set_grid_pos(spawn_x, spawn_y)
        self.current_direction = Direction.NONE
        self.next_direction = Direction.NONE
        self.data.direction = Direction.RIGHT

    def update(
        self, board: MazeBoard, game_state: GameState
    ) -> Optional[int]:
        """Advance player and consume any pacgum on the current tile."""
        self.advance_position(board)
        self.data.direction = self.current_direction
        eaten: Optional[int] = board.consume_tile(
            self.position.x, self.position.y
        )
        if eaten is not None:
            game_state.score += self.points[eaten]
        return eaten
