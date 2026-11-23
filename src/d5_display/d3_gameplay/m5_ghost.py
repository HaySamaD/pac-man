"""Ghost AI controller implementing classic arcade targeting and states."""

from typing import Dict, List, Set, Tuple

from ...d2_classes import Direction, Ghost
from .m1_maze_board import MazeBoard
from .m2_bfs import Bfs
from .m3_movement import MovementController


class GhostController(MovementController):
    """Controls autonomous behavior for Blinky, Pinky, Inky, and Clyde."""

    PRIORITIES: Dict[str, List[str]] = {
        "blinky": [
            Direction.UP,
            Direction.LEFT,
            Direction.DOWN,
            Direction.RIGHT,
        ],
        "pinky": [
            Direction.LEFT,
            Direction.UP,
            Direction.RIGHT,
            Direction.DOWN,
        ],
        "inky": [
            Direction.DOWN,
            Direction.RIGHT,
            Direction.UP,
            Direction.LEFT,
        ],
        "clyde": [
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT,
            Direction.UP,
        ],
    }

    def __init__(
        self,
        ghost_data: Ghost,
        spawn_corner: Tuple[int, int],
        bfs: Bfs,
        tile_size: int = 40,
        normal_speed: int = 2,
    ) -> None:
        """Initialize ghost state, home corner, and BFS pathfinder."""
        super().__init__(
            ghost_data.position, ghost_data.direction, tile_size, normal_speed
        )
        self.data: Ghost = ghost_data
        self.spawn_x: int = spawn_corner[0]
        self.spawn_y: int = spawn_corner[1]
        self.bfs: Bfs = bfs
        self.normal_speed: int = normal_speed
        self.frightened_speed: int = max(1, normal_speed // 2)
        self.is_eaten: bool = False
        self.frightened_timer: int = 0
        self.respawn_timer: int = 0
        self.last_heading: str = self.current_direction

    def set_frightened(self, duration_frames: int = 420) -> None:
        """Activate frightened state and reverse current heading."""
        if not self.is_eaten:
            self.data.is_edible = True
            self.frightened_timer = duration_frames
            self.speed = self.frightened_speed
            self.next_direction = Direction.OPPOSITES[self.current_direction]

    def make_eaten(self) -> None:
        """Mark ghost as eaten so eyes return to spawn point."""
        self.is_eaten = True
        self.data.is_edible = False
        self.frightened_timer = 0
        self.respawn_timer = 0
        self.speed = self.normal_speed

    def reset_to_spawn(self) -> None:
        """Return ghost immediately to its starting corner."""
        self.set_grid_pos(self.spawn_x, self.spawn_y)
        self.current_direction = Direction.UP
        self.next_direction = Direction.UP
        self.last_heading = Direction.UP
        self.is_eaten = False
        self.data.is_edible = False
        self.frightened_timer = 0
        self.respawn_timer = 0
        self.speed = self.normal_speed

    def get_target_tile(
        self,
        player_x: int,
        player_y: int,
        player_dir: str,
        blinky_pos: Tuple[int, int],
    ) -> Tuple[int, int]:
        """Calculate target cell according to active state and type."""
        if self.is_eaten:
            return self.spawn_x, self.spawn_y

        dx, dy = Direction.VECTORS[player_dir]
        if self.data.ghost_type == "pinky":
            return player_x + 4 * dx, player_y + 4 * dy
        if self.data.ghost_type == "inky":
            px: int = player_x + 2 * dx
            py: int = player_y + 2 * dy
            return 2 * px - blinky_pos[0], 2 * py - blinky_pos[1]
        return player_x, player_y

    def choose_next_direction(
        self,
        board: MazeBoard,
        gx: int,
        gy: int,
        player_x: int,
        player_y: int,
        player_dir: str,
        target: Tuple[int, int],
        occupied: Set[Tuple[int, int]],
    ) -> None:
        """Select optimal valid corridor direction without reversing."""
        heading: str = (
            self.current_direction
            if self.current_direction != Direction.NONE
            else self.last_heading
        )
        forbidden: str = Direction.OPPOSITES[heading]
        order: List[str] = self.PRIORITIES.get(
            self.data.ghost_type, self.PRIORITIES["blinky"]
        )
        valid: List[str] = [
            d for d in order if d != forbidden and board.can_move(gx, gy, d)
        ]
        if not valid and board.can_move(gx, gy, forbidden):
            valid = [forbidden]
        if not valid:
            return

        fleeing: bool = self.data.is_edible and not self.is_eaten
        tx, ty = (player_x, player_y) if fleeing else target
        dist_map: Dict[Tuple[int, int], int] = self.bfs.get_distance_map(
            board, tx, ty
        )
        opp_player: str = Direction.OPPOSITES[player_dir]

        best_dir: str = valid[0]
        best_cost: int = 999999
        for d in valid:
            dx, dy = Direction.VECTORS[d]
            npos: Tuple[int, int] = (gx + dx, gy + dy)
            if fleeing:
                cost: int = -dist_map.get(npos, 0) * 10
                if d == opp_player:
                    cost -= 5
                if npos in occupied:
                    cost += 40
            else:
                cost = dist_map.get(npos, 999999)
                if not self.is_eaten and npos in occupied:
                    cost += 4
            if cost < best_cost:
                best_cost = cost
                best_dir = d
        self.next_direction = best_dir

    def update(
        self,
        board: MazeBoard,
        player_x: int,
        player_y: int,
        player_dir: str,
        blinky_pos: Tuple[int, int],
        occupied: Set[Tuple[int, int]],
    ) -> None:
        """Update timers, compute AI decision at center, and move."""
        if self.data.is_edible:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.data.is_edible = False
                self.speed = self.normal_speed

        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            if self.respawn_timer == 0:
                self.reset_to_spawn()
            return

        gx, gy = self.get_grid_coords()
        if self.is_near_center():
            if self.is_eaten and (gx, gy) == (self.spawn_x, self.spawn_y):
                self.set_grid_pos(self.spawn_x, self.spawn_y)
                self.current_direction = Direction.NONE
                self.next_direction = Direction.NONE
                self.respawn_timer = 360
                return
            target: Tuple[int, int] = self.get_target_tile(
                player_x, player_y, player_dir, blinky_pos
            )
            self.choose_next_direction(
                board,
                gx,
                gy,
                player_x,
                player_y,
                player_dir,
                target,
                occupied,
            )

        if self.current_direction != Direction.NONE:
            self.last_heading = self.current_direction
        self.advance_position(board)
        self.data.direction = self.current_direction
