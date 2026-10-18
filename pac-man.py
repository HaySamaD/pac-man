"""Main entry point and gameplay orchestrator for Pac-Man arcade."""

import json
import os
import random
import sys
from typing import Any, Dict, List, Optional, Tuple
from mazegenerator import MazeGenerator
import pygame
from src.cheat_mode import CheatController
from src.d1_classes.m1_dataclasses import (
    Direction,
    GameState,
    GameStatus,
    Ghost,
    GhostType,
    Player,
    Position,
)
from src.ghost import GhostController
from src.maze_board import MazeBoard, TileType
from src.movement import MovementController
from src.player import PlayerController
from src.renderer import Renderer

DEFAULT_CONFIG: Dict[str, Any] = {
    "highscore_filename": "data/highscores.json",
    "width": 15,
    "height": 10,
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90,
    "total_levels": 10,
}


def load_clean_config(filepath: Optional[str]) -> Dict[str, Any]:
    """Load configuration from JSON file ignoring comments and bad values."""
    config: Dict[str, Any] = dict(DEFAULT_CONFIG)
    if not filepath or not os.path.exists(filepath):
        return config

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            clean_lines: List[str] = []
            for line in file:
                stripped: str = line.strip()
                if not stripped.startswith("#") and not stripped.startswith(
                    "//"
                ):
                    clean_lines.append(line)
            parsed: Any = json.loads("".join(clean_lines))
            if isinstance(parsed, dict):
                for key, val in parsed.items():
                    if key in config and isinstance(val, (int, str)):
                        config[key] = val
    except Exception:
        return dict(DEFAULT_CONFIG)

    return config


def create_level_board(
    width: int,
    height: int,
    seed: int,
    max_pacgums: int,
) -> MazeBoard:
    """Generate and construct a MazeBoard instance from external generator."""
    raw_maze: List[List[int]]
    try:
        try:
            gen = MazeGenerator(
                size=(width, height), seed=seed, perfect=False
            )
        except TypeError:
            gen = MazeGenerator(size=(width, height), seed=seed)
        raw_maze = gen.maze
    except Exception:
        raw_maze = [[0 for _ in range(width)] for _ in range(height)]
        for col in range(width):
            raw_maze[0][col] |= 1
            raw_maze[height - 1][col] |= 4
        for row in range(height):
            raw_maze[row][0] |= 8
            raw_maze[row][width - 1] |= 2

    return MazeBoard.from_raw_maze(raw_maze, max_pacgums=max_pacgums)


def setup_ghosts(
    board: MazeBoard,
    tile_size: int,
    speed: int,
) -> List[GhostController]:
    """Spawn the 4 arcade ghosts in their respective home corners."""
    corner_configs: List[Tuple[int, GhostType]] = [
        (0, GhostType.BLINKY),
        (1, GhostType.PINKY),
        (2, GhostType.INKY),
        (3, GhostType.CLYDE),
    ]
    ghosts: List[GhostController] = []
    for corner_idx, g_type in corner_configs:
        cx, cy = board.find_corner_spawn(corner_idx)
        g_data = Ghost(
            position=Position(x=cx, y=cy),
            ghost_type=g_type,
            direction=Direction.UP,
        )
        ctrl = GhostController(
            ghost_data=g_data,
            spawn_corner=(cx, cy),
            tile_size=tile_size,
            normal_speed=speed,
            frightened_speed=max(1, speed // 2),
        )
        ghosts.append(ctrl)
    return ghosts


def reset_round_positions(
    player_ctrl: PlayerController,
    spawn_pos: Tuple[int, int],
    ghosts: List[GhostController],
) -> None:
    """Reset player and ghost coordinates back to safe starting points."""
    player_ctrl.respawn(spawn_pos[0], spawn_pos[1])
    for ghost in ghosts:
        ghost.reset_to_spawn()


def resolve_level_parameters(
    config: Any,
    level_number: int,
) -> Tuple[int, int, int, int]:
    """Extract width, height, pacgums, and seed with fallbacks."""
    def_w: int = 20
    def_h: int = 15
    def_pacgum: int = 42
    def_seed: int = getattr(config, "seed", 42)

    l1_w: int = def_w
    l1_h: int = def_h
    l1_pacgum: int = def_pacgum

    levels_list = getattr(config, "levels_data", [])
    if levels_list and len(levels_list) > 0:
        first_lvl = levels_list[0]
        l1_w = getattr(first_lvl, "width", def_w)
        l1_h = getattr(first_lvl, "height", def_h)
        l1_pacgum = getattr(first_lvl, "pacgum", def_pacgum)

    target_idx: int = level_number - 1
    cur_w: int = l1_w
    cur_h: int = l1_h
    cur_pacgum: int = l1_pacgum

    if 0 <= target_idx < len(levels_list):
        lvl_obj = levels_list[target_idx]
        cur_w = getattr(lvl_obj, "width", l1_w)
        cur_h = getattr(lvl_obj, "height", l1_h)
        cur_pacgum = getattr(lvl_obj, "pacgum", l1_pacgum)

    if level_number == 1:
        lvl_seed = def_seed
    else:
        lvl_seed = random.randint(10000, 999999)

    return cur_w, cur_h, cur_pacgum, lvl_seed


def main() -> None:
    """Run main gameplay loop coordinating levels, timers, and entities."""
    config_file: Optional[str] = None
    if len(sys.argv) == 2:
        config_file = sys.argv[1]
        if not config_file.endswith(".json"):
            sys.stderr.write(
                f"Error: Config file '{config_file}' must be a .json file.\n"
            )
            sys.exit(1)
        if not os.path.isfile(config_file):
            sys.stderr.write(
                f"Error: Config file '{config_file}' not found.\n"
            )
            sys.exit(1)
    elif len(sys.argv) > 2:
        sys.stderr.write(
            "Error: pac-man takes at most one argument: config.json\n"
        )
        sys.exit(1)

    config: Dict[str, Any] = load_clean_config(config_file)

    width: int = int(config.get("width", 15))
    height: int = int(config.get("height", 10))
    initial_seed: int = int(config.get("seed", 42))
    max_pacgums: int = int(config.get("pacgum", 42))
    points_pacgum: int = int(config.get("points_per_pacgum", 10))
    points_super: int = int(config.get("points_per_super_pacgum", 50))
    points_ghost: int = int(config.get("points_per_ghost", 200))
    level_max_time: int = int(config.get("level_max_time", 90))
    total_levels: int = int(config.get("total_levels", 10))
    start_lives: int = int(config.get("lives", 3))

    tile_size: int = 40
    entity_speed: int = 2

    board: MazeBoard = create_level_board(
        width, height, initial_seed, max_pacgums
    )
    renderer: Renderer = Renderer(board, tile_size=tile_size)

    spawn_pos: Tuple[int, int] = board.find_spawn_position()
    player_data: Player = Player(
        position=Position(x=spawn_pos[0], y=spawn_pos[1]),
        direction=Direction.RIGHT,
        is_alive=True,
    )
    game_state: GameState = GameState(
        score=0,
        lives=start_lives,
        level=1,
        time_left=level_max_time,
        status=GameStatus.PLAYING,
    )

    player_ctrl: PlayerController = PlayerController(
        player_data=player_data,
        tile_size=tile_size,
        speed=entity_speed,
        points_per_pacgum=points_pacgum,
        points_per_super_pacgum=points_super,
    )

    ghosts: List[GhostController] = setup_ghosts(
        board, tile_size, entity_speed
    )
    cheat_ctrl: CheatController = CheatController(is_enabled=True)

    running: bool = True
    is_paused: bool = False
    frame_counter: int = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    is_paused = not is_paused
                    game_state.status = (
                        GameStatus.PAUSED if is_paused else GameStatus.PLAYING
                    )
                elif event.key == pygame.K_c:
                    cheat_ctrl.set_enabled(not cheat_ctrl.is_enabled)
                else:
                    skip_req: bool = cheat_ctrl.handle_cheat_keys(
                        event, player_ctrl, game_state
                    )
                    if skip_req:
                        board.remaining_pacgums = 0

        if is_paused or game_state.status != GameStatus.PLAYING:
            renderer.render_map()
            renderer.render_player(player_ctrl)
            for ghost in ghosts:
                renderer.render_ghost(ghost)
            renderer.update_display()
            continue

        frame_counter += 1
        if frame_counter % 60 == 0:
            game_state.time_left -= 1
            if game_state.time_left <= 0:
                if not cheat_ctrl.god_mode:
                    game_state.lives -= 1
                    if game_state.lives <= 0:
                        player_data.is_alive = False
                        game_state.status = GameStatus.GAME_OVER
                game_state.time_left = level_max_time
                reset_round_positions(player_ctrl, spawn_pos, ghosts)

        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        player_ctrl.handle_input(keys)
        eaten_item: Optional[TileType] = player_ctrl.update(
            board, game_state
        )

        if eaten_item == TileType.SUPER_PACGUM:
            for ghost in ghosts:
                ghost.set_frightened(duration_frames=420)

        blinky_pos: Optional[Tuple[int, int]] = None
        for g in ghosts:
            if g.data.ghost_type == GhostType.BLINKY:
                blinky_pos = (g.position.x, g.position.y)
                break

        if not cheat_ctrl.ghosts_frozen:
            for ghost in ghosts:
                other_positions = [
                    (g.position.x, g.position.y)
                    for g in ghosts
                    if g is not ghost
                ]
                ghost.update(
                    board,
                    player_ctrl.position.x,
                    player_ctrl.position.y,
                    player_ctrl.current_direction,
                    blinky_pos=blinky_pos,
                    other_ghosts_pos=other_positions,
                )

        col_thresh_sq: float = (tile_size * 0.7) ** 2
        for ghost in ghosts:
            dist_sq: float = MovementController.euclidean_distance_sq(
                player_ctrl.pixel_x,
                player_ctrl.pixel_y,
                ghost.pixel_x,
                ghost.pixel_y,
            )
            is_collision: bool = (
                dist_sq <= col_thresh_sq
                or (
                    ghost.position.x == player_ctrl.position.x
                    and ghost.position.y == player_ctrl.position.y
                )
            )
            if is_collision:
                if ghost.data.is_edible and not ghost.is_eaten:
                    ghost.make_eaten()
                    game_state.score += points_ghost
                elif not ghost.data.is_edible and not ghost.is_eaten:
                    if not cheat_ctrl.god_mode:
                        game_state.lives -= 1
                        if game_state.lives <= 0:
                            player_data.is_alive = False
                            game_state.status = GameStatus.GAME_OVER
                        else:
                            reset_round_positions(
                                player_ctrl, spawn_pos, ghosts
                            )
                    break

        if board.remaining_pacgums <= 0:
            if game_state.level < total_levels:
                game_state.level += 1
                next_seed: int = random.randint(1000, 999999)
                board = create_level_board(
                    width, height, next_seed, max_pacgums
                )
                renderer.set_board(board)
                spawn_pos = board.find_spawn_position()
                reset_round_positions(player_ctrl, spawn_pos, ghosts)
                game_state.time_left = level_max_time
            else:
                game_state.status = GameStatus.VICTORY

        renderer.render_map()
        renderer.render_player(player_ctrl)
        for ghost in ghosts:
            renderer.render_ghost(ghost)
        renderer.update_display()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
