"""Player controller module managing user input and collectible consumption."""

from typing import Optional
import pygame
from src.d1_classes.m1_dataclasses import Direction, GameState, Player
from src.maze_board import MazeBoard, TileType
from src.movement import MovementController


class PlayerController(MovementController):
    """Controller for the playable Pac-Man character."""

    def __init__(
        self,
        player_data: Player,
        tile_size: int = 40,
        speed: int = 4,
        points_per_pacgum: int = 10,
        points_per_super_pacgum: int = 50,
    ) -> None:
        """Initialize the player entity, speed, and scoring parameters."""
        super().__init__(
            position=player_data.position,
            direction=player_data.direction,
            tile_size=tile_size,
            speed=speed,
        )
        self.data: Player = player_data
        self.points_per_pacgum: int = points_per_pacgum
        self.points_per_super_pacgum: int = points_per_super_pacgum

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Read keyboard states and register requested movement direction."""
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.next_direction = Direction.UP
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.next_direction = Direction.DOWN
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.next_direction = Direction.LEFT
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.next_direction = Direction.RIGHT

    def respawn(self, spawn_x: int, spawn_y: int) -> None:
        """Reset player coordinates and heading to designated spawn cell."""
        self.position.x = spawn_x
        self.position.y = spawn_y
        self.pixel_x = float(spawn_x * self.tile_size)
        self.pixel_y = float(spawn_y * self.tile_size)
        self.current_direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.data.direction = Direction.RIGHT

    def update(
        self,
        board: MazeBoard,
        game_state: Optional[GameState] = None,
    ) -> Optional[TileType]:
        """Advance player position and consume items at current location."""
        if not self.data.is_alive:
            return None

        self.advance_pixel_position(board)
        self.data.direction = self.current_direction
        return self._consume_items(board, game_state)

    def _consume_items(
        self,
        board: MazeBoard,
        game_state: Optional[GameState],
    ) -> Optional[TileType]:
        """Consume collectible dot from board and increment player score."""
        eaten: Optional[TileType] = board.consume_tile(
            self.position.x, self.position.y
        )
        if eaten is None:
            return None

        if game_state is not None:
            if eaten == TileType.PACGUM:
                game_state.score += self.points_per_pacgum
            elif eaten == TileType.SUPER_PACGUM:
                game_state.score += self.points_per_super_pacgum

        return eaten
