"""Unified gameplay facade connecting Core UI with Maze, Entities, and AI."""

import random
from typing import List, Optional, Set, Tuple

import pygame
from pygame.event import Event

from ...d2_classes import Config, GameState, Ghost, Player, Position
from ...d2_classes import Direction, TileType
from .m2_bfs import Bfs
from .m7_cheat_mode import CheatController
from .m5_ghost import GhostController
from .m1_maze_board import MazeBoard
from .m4_player import PlayerController
from .m6_renderer import Renderer


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
        self.wave_timer: int = 0
        self.session_active: bool = False

        self.bfs: Bfs = Bfs()
        self.cheat: CheatController = CheatController()

        lvl_cfg = self.config.levels_data[0]
        self.board: MazeBoard = MazeBoard(
            min(lvl_cfg.width, 46),
            min(lvl_cfg.height, 24),
            self.config.seed,
            lvl_cfg.pacgum,
        )
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

    def create_ghosts(self) -> List[GhostController]:
        """Instantiate the 4 arcade ghosts in their respective corners."""
        names: List[str] = ["blinky", "pinky", "inky", "clyde"]
        result: List[GhostController] = []
        for idx, name in enumerate(names):
            cx, cy = self.board.find_corner_spawn(idx)
            g_data: Ghost = Ghost(
                Position(cx, cy), name, False, Direction.UP
            )
            result.append(
                GhostController(
                    g_data,
                    (cx, cy),
                    self.bfs,
                    self.tile_size,
                    self.speed,
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
        idx: int = max(
            0, min(len(self.config.levels_data) - 1, level_num - 1)
        )
        lvl_cfg = self.config.levels_data[idx]
        seed: int = (
            self.config.seed
            if level_num == 1
            else random.randint(1000, 999999)
        )
        self.board = MazeBoard(
            min(lvl_cfg.width, 46),
            min(lvl_cfg.height, 24),
            seed,
            lvl_cfg.pacgum,
        )
        self.renderer.set_board(self.board)
        self.spawn_pos = self.board.find_spawn_position()
        self.ghosts = self.create_ghosts()
        self.reset_positions()
        self.game_state.time_left = self.config.level_max_time
        self.frame_counter = 0
        self.wave_timer = 0

    def reset_positions(self) -> None:
        """Respawn player at center and ghosts at their home corners."""
        self.player.respawn(self.spawn_pos[0], self.spawn_pos[1])
        for ghost in self.ghosts:
            ghost.reset_to_spawn()

    def advance_level(self) -> None:
        """Move to next level or trigger WIN status if all completed."""
        total_levels: int = len(self.config.levels_data)
        if self.game_state.level < total_levels:
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

    def check_collisions(self) -> None:
        """Handle overlaps between player and ghosts."""
        thresh_sq: float = (self.tile_size * 0.7) ** 2
        for ghost in self.ghosts:
            dist_sq: float = self.player.distance_sq(
                self.player.pixel_x,
                self.player.pixel_y,
                ghost.pixel_x,
                ghost.pixel_y,
            )
            same_tile: bool = (
                ghost.position.x == self.player.position.x
                and ghost.position.y == self.player.position.y
            )
            if dist_sq <= thresh_sq or same_tile:
                if ghost.data.is_edible and not ghost.is_eaten:
                    ghost.make_eaten()
                    self.game_state.score += self.config.points_per_ghost
                elif not ghost.data.is_edible and not ghost.is_eaten:
                    if not self.cheat.god_mode:
                        self.game_state.lives -= 1
                        if self.game_state.lives <= 0:
                            self.player.data.is_alive = False
                            self.game_state.status = "LOSS"
                            self.session_active = False
                        else:
                            self.reset_positions()
                    break

    def update_and_render(self) -> None:
        """Update timers, entities, collisions, and draw frame."""
        if not self.session_active:
            self.start_new_game()

        self.frame_counter += 1
        self.wave_timer = (self.wave_timer + 1) % 1620
        is_scatter: bool = self.wave_timer < 420

        if self.frame_counter % 60 == 0:
            self.game_state.time_left -= 1
            if self.game_state.time_left <= 0:
                if not self.cheat.god_mode:
                    self.game_state.lives -= 1
                    if self.game_state.lives <= 0:
                        self.game_state.status = "LOSS"
                        self.session_active = False
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
                if g is not ghost
            }
            ghost.update(
                self.board,
                self.player.position.x,
                self.player.position.y,
                self.player.current_direction,
                blinky_pos,
                occupied,
                is_scatter,
            )

        self.check_collisions()
        if self.board.remaining_pacgums <= 0:
            self.advance_level()

        self.renderer.render_all(self.player, self.ghosts)
