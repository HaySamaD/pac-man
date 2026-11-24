"""Unified gameplay facade connecting Core UI with Maze, Entities, AI."""

import random
from typing import List, Optional, Set, Tuple

import pygame
from pygame.event import Event

from ...d2_classes import (
    Config,
    Direction,
    GameState,
    Ghost,
    Player,
    Position,
    TileType,
)
from .m1_maze_board import MazeBoard
from .m2_bfs import Bfs
from .m4_player import PlayerController
from .m5_ghost import GhostController
from .m6_renderer import Renderer
from .m7_cheat_mode import CheatController


class Gameplay:
    """Single facade class for Person 1 to run and render active gameplay."""

    def __init__(
        self,
        screen: pygame.Surface,
        config: Config,
        game_state: GameState,
    ) -> None:
        """Initialize gameplay subsystems and load initial level."""
        self.screen: pygame.Surface = screen
        self.config: Config = config
        self.game_state: GameState = game_state
        self.tile_size: int = 40
        self.speed: int = 2
        self.frame_counter: int = 0
        self.session_active: bool = False

        self.bfs: Bfs = Bfs()
        self.cheat: CheatController = CheatController()
        self.board: MazeBoard = self.make_board(1)
        self.renderer: Renderer = Renderer(
            self.screen, self.board, self.tile_size
        )
        self.spawn_pos: Tuple[int, int] = self.board.find_spawn_position()
        p_data: Player = Player(
            Position(self.spawn_pos[0], self.spawn_pos[1]),
            Direction.RIGHT,
            True,
        )
        self.player: PlayerController = PlayerController(
            p_data,
            self.tile_size,
            self.speed,
            self.config.points_per_pacgum,
            self.config.points_per_super_pacgum,
        )
        self.ghosts: List[GhostController] = self.create_ghosts()

    def make_board(self, level_num: int) -> MazeBoard:
        """Build a MazeBoard for the given 1-based level number."""
        max_idx: int = len(self.config.levels_data) - 1
        lvl = self.config.levels_data[max(0, min(max_idx, level_num - 1))]
        seed: int = (
            self.config.seed
            if level_num == 1
            else random.randint(1000, 999999)
        )
        return MazeBoard(lvl.width, lvl.height, seed, lvl.pacgum)

    def create_ghosts(self) -> List[GhostController]:
        """Instantiate the 4 arcade ghosts in their respective corners."""
        names: Tuple[str, ...] = ("blinky", "pinky", "inky", "clyde")
        result: List[GhostController] = []
        for idx, name in enumerate(names):
            cx, cy = self.board.find_corner_spawn(idx)
            g_data: Ghost = Ghost(Position(cx, cy), name, False, Direction.UP)
            result.append(
                GhostController(
                    g_data, (cx, cy), self.bfs, self.tile_size, self.speed
                )
            )
        return result

    def start_new_game(self) -> None:
        """Reset game state metrics and build Level 1 with fixed seed."""
        self.game_state.score = 0
        self.game_state.lives = self.config.lives
        self.game_state.level = 1
        self.game_state.time_left = self.config.level_max_time
        self.player.data.is_alive = True
        self.session_active = True
        self.load_level(1)

    def load_level(self, level_num: int) -> None:
        """Build maze for specified level index and reset positions."""
        self.board = self.make_board(level_num)
        self.renderer.set_board(self.board)
        self.spawn_pos = self.board.find_spawn_position()
        self.ghosts = self.create_ghosts()
        self.reset_positions()
        self.game_state.time_left = self.config.level_max_time
        self.frame_counter = 0

    def reset_positions(self) -> None:
        """Respawn player at center and ghosts at their home corners."""
        self.player.respawn(self.spawn_pos[0], self.spawn_pos[1])
        for ghost in self.ghosts:
            ghost.reset_to_spawn()

    def lose_life(self) -> bool:
        """Decrement lives unless invincible; return True on game loss."""
        if self.cheat.invinc_mode:
            return False
        self.game_state.lives -= 1
        if self.game_state.lives <= 0:
            self.player.data.is_alive = False
            self.game_state.status = "LOSS"
            self.session_active = False
            return True
        return False

    def advance_level(self) -> None:
        """Move to next level or trigger WIN status if all completed."""
        if self.game_state.level < len(self.config.levels_data):
            self.game_state.level += 1
            self.load_level(self.game_state.level)
        else:
            self.game_state.status = "WIN"
            self.session_active = False

    def handle_event(self, event: Event) -> None:
        """Process player movement and cheat keys during PLAY state."""
        if event.type != pygame.KEYDOWN:
            return
        self.player.handle_key(event.key)
        if self.cheat.handle_key(event.key):
            self.advance_level()
        self.player.speed = self.speed * self.cheat.speed_mult

    def check_collisions(self) -> None:
        """Handle overlaps between player and ghosts."""
        thresh_sq: float = (self.tile_size * 0.7) ** 2
        px, py = self.player.position.x, self.player.position.y
        for ghost in self.ghosts:
            if ghost.is_eaten:
                continue
            dist_sq: float = self.player.distance_sq(
                self.player.pixel_x,
                self.player.pixel_y,
                ghost.pixel_x,
                ghost.pixel_y,
            )
            same_tile: bool = (
                ghost.position.x == px and ghost.position.y == py
            )
            if dist_sq <= thresh_sq or same_tile:
                if ghost.data.is_edible:
                    ghost.make_eaten()
                    self.game_state.score += self.config.points_per_ghost
                else:
                    if not self.cheat.invinc_mode and not self.lose_life():
                        self.reset_positions()
                    break

    def update_and_render(self) -> None:
        """Update timers, entities, collisions, and draw frame."""
        if not self.session_active:
            self.start_new_game()

        self.frame_counter += 1
        if self.frame_counter % 60 == 0:
            self.game_state.time_left -= 1
            if self.game_state.time_left <= 0:
                if self.lose_life():
                    return
                self.game_state.time_left = self.config.level_max_time
                self.reset_positions()

        eaten: Optional[int] = self.player.update(
            self.board, self.game_state
        )
        if eaten == TileType.SUPER_PACGUM:
            for ghost in self.ghosts:
                ghost.set_frightened(420)

        blinky_pos: Tuple[int, int] = (
            self.ghosts[0].position.x,
            self.ghosts[0].position.y,
        )
        for ghost in self.ghosts:
            occupied: Set[Tuple[int, int]] = {
                (g.position.x, g.position.y)
                for g in self.ghosts
                if g is not ghost and not g.is_eaten
            }
            occupied.discard(
                (self.player.position.x, self.player.position.y)
            )
            ghost.update(
                self.board,
                self.player.position.x,
                self.player.position.y,
                self.player.current_direction,
                blinky_pos,
                occupied
            )

        self.check_collisions()
        if self.board.remaining_pacgums <= 0:
            self.advance_level()

        self.renderer.render_all(self.player, self.ghosts)
