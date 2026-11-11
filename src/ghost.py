"""Ghost controller module with AI pathfinding and crowding avoidance."""

from collections import deque
from typing import Deque, Dict, List, Optional, Set, Tuple
from src.d1_classes.m1_dataclasses import Direction, Ghost, GhostType
from src.maze_board import MazeBoard
from src.movement import MovementController

_CROWD_PENALTY_CHASE: int = 4
_CROWD_PENALTY_FLEE: int = 3
_CLYDE_CHASE_RADIUS: int = 8
_CLYDE_RETURN_RADIUS: int = 12

_PRIORITY_MAP: Dict[str, List[Direction]] = {
    "blinky": [
        Direction.UP,
        Direction.LEFT,
        Direction.DOWN,
        Direction.RIGHT,
    ],
    "pinky": [
        Direction.RIGHT,
        Direction.DOWN,
        Direction.LEFT,
        Direction.UP,
    ],
    "inky": [
        Direction.LEFT,
        Direction.UP,
        Direction.RIGHT,
        Direction.DOWN,
    ],
    "clyde": [
        Direction.DOWN,
        Direction.RIGHT,
        Direction.UP,
        Direction.LEFT,
    ],
}


class GhostController(MovementController):
    """Controls autonomous AI behavior and states for an individual ghost."""

    def __init__(
        self,
        ghost_data: Ghost,
        spawn_corner: Tuple[int, int],
        tile_size: int = 40,
        normal_speed: int = 4,
        frightened_speed: int = 2,
    ) -> None:
        """Initialize ghost entity with spawn points, speeds, and state."""
        super().__init__(
            position=ghost_data.position,
            direction=Direction(ghost_data.direction),
            tile_size=tile_size,
            speed=normal_speed,
        )
        self.data: Ghost = ghost_data
        self.spawn_x: int = spawn_corner[0]
        self.spawn_y: int = spawn_corner[1]
        self.normal_speed: int = normal_speed
        self.frightened_speed: int = frightened_speed
        self.is_eaten: bool = False
        self.frightened_timer: int = 0
        self.respawn_timer: int = 0
        self.last_heading: Direction = self.current_direction
        self._clyde_retreating: bool = False

    def set_frightened(self, duration_frames: int = 420) -> None:
        """Trigger frightened mode when player eats a super-pacgum."""
        if not self.is_eaten:
            self.data.is_edible = True
            self.frightened_timer = duration_frames
            self.speed = self.frightened_speed
            self.next_direction = self.current_direction.opposite

    def make_eaten(self) -> None:
        """Mark ghost as eaten by player and start respawn sequence."""
        self.is_eaten = True
        self.data.is_edible = False
        self.frightened_timer = 0
        self.respawn_timer = 300
        self.speed = self.normal_speed

    def reset_to_spawn(self) -> None:
        """Reset ghost state and snap back to its initial home corner."""
        self.position.x = self.spawn_x
        self.position.y = self.spawn_y
        self.pixel_x = float(self.spawn_x * self.tile_size)
        self.pixel_y = float(self.spawn_y * self.tile_size)
        self.current_direction = Direction.UP
        self.next_direction = Direction.UP
        self.last_heading = Direction.UP
        self.is_eaten = False
        self.data.is_edible = False
        self.frightened_timer = 0
        self.respawn_timer = 0
        self.speed = self.normal_speed
        self._clyde_retreating = False

    def _get_directional_priority(self) -> List[Direction]:
        """Return distinct directional tie-breaking priority per ghost."""
        raw_type = self.data.ghost_type
        g_name = str(
            raw_type.value if hasattr(raw_type, "value") else raw_type
        ).lower()
        return _PRIORITY_MAP.get(g_name, _PRIORITY_MAP["clyde"])

    def _get_nearest_walkable_tile(
        self,
        board: MazeBoard,
        target_x: int,
        target_y: int,
    ) -> Tuple[int, int]:
        """Find the closest walkable corridor tile to given coordinates."""
        clamped_x = max(0, min(board.width - 1, target_x))
        clamped_y = max(0, min(board.height - 1, target_y))

        if not board.is_wall(clamped_x, clamped_y):
            return clamped_x, clamped_y

        queue: Deque[Tuple[int, int]] = deque([(clamped_x, clamped_y)])
        visited: Set[Tuple[int, int]] = {(clamped_x, clamped_y)}

        while queue:
            cx, cy = queue.popleft()
            if not board.is_wall(cx, cy):
                return cx, cy

            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                nx, ny = cx + dx, cy + dy
                if (
                    0 <= nx < board.width
                    and 0 <= ny < board.height
                    and (nx, ny) not in visited
                ):
                    visited.add((nx, ny))
                    queue.append((nx, ny))

        return clamped_x, clamped_y

    def _bfs_distance_map(
        self,
        board: MazeBoard,
        target: Tuple[int, int],
    ) -> Dict[Tuple[int, int], int]:
        """Compute shortest maze path distance from all cells to target."""
        tx, ty = self._get_nearest_walkable_tile(board, target[0], target[1])
        queue: Deque[Tuple[int, int]] = deque([(tx, ty)])
        dist: Dict[Tuple[int, int], int] = {(tx, ty): 0}

        while queue:
            cx, cy = queue.popleft()
            cur_d = dist[(cx, cy)]

            for d in (
                Direction.UP,
                Direction.DOWN,
                Direction.LEFT,
                Direction.RIGHT,
            ):
                dx, dy = d.vector
                nx, ny = cx + dx, cy + dy

                if (
                    0 <= nx < board.width
                    and 0 <= ny < board.height
                    and (nx, ny) not in dist
                    and self.can_move(board, d.opposite, nx, ny)
                ):
                    dist[(nx, ny)] = cur_d + 1
                    queue.append((nx, ny))

        return dist

    def _bfs_farthest_corner(
        self,
        board: MazeBoard,
        dist_map: Dict[Tuple[int, int], int],
    ) -> Tuple[int, int]:
        """Return the walkable corner cell with maximum BFS distance."""
        corners: List[Tuple[int, int]] = [
            (0, 0),
            (board.width - 1, 0),
            (0, board.height - 1),
            (board.width - 1, board.height - 1),
        ]
        walkable_corners = [
            self._get_nearest_walkable_tile(board, cx, cy)
            for cx, cy in corners
        ]
        return max(walkable_corners, key=lambda c: dist_map.get(c, 0))

    def _choose_target(
        self,
        board: MazeBoard,
        player_x: int,
        player_y: int,
        player_dir: Direction,
        blinky_pos: Optional[Tuple[int, int]] = None,
    ) -> Tuple[int, int]:
        """Compute target tile based on ghost personality and state."""
        if self.is_eaten:
            return self.spawn_x, self.spawn_y

        raw_type = self.data.ghost_type
        g_type = str(
            raw_type.value if hasattr(raw_type, "value") else raw_type
        ).lower()
        p_dx, p_dy = player_dir.vector

        if g_type in ("blinky", GhostType.BLINKY.value):
            return player_x, player_y

        if g_type in ("pinky", GhostType.PINKY.value):
            if p_dx == 0 and p_dy == 0:
                return self._get_nearest_walkable_tile(
                    board, player_x + 2, player_y - 2
                )
            for step in (4, 3, 2, 1):
                tx = player_x + p_dx * step
                ty = player_y + p_dy * step
                if (
                    0 <= tx < board.width
                    and 0 <= ty < board.height
                    and not board.is_wall(tx, ty)
                ):
                    return tx, ty
            flank_x = player_x - p_dy * 3
            flank_y = player_y + p_dx * 3
            return self._get_nearest_walkable_tile(board, flank_x, flank_y)

        if g_type in ("inky", GhostType.INKY.value):
            pivot_x = player_x + p_dx * 2
            pivot_y = player_y + p_dy * 2
            if blinky_pos is not None:
                bx, by = blinky_pos
                target_x = 2 * pivot_x - bx
                target_y = 2 * pivot_y - by
            else:
                target_x, target_y = pivot_x, pivot_y
            return self._get_nearest_walkable_tile(board, target_x, target_y)

        # Clyde cowardice retreat with 8/12 hysteresis gap
        dist_map = self._bfs_distance_map(board, (player_x, player_y))
        dist_to_player = dist_map.get((self.position.x, self.position.y), 999)

        if (
            not self._clyde_retreating
            and dist_to_player <= _CLYDE_CHASE_RADIUS
        ):
            self._clyde_retreating = True

        if self._clyde_retreating and dist_to_player >= _CLYDE_RETURN_RADIUS:
            self._clyde_retreating = False

        if self._clyde_retreating:
            return self._bfs_farthest_corner(board, dist_map)

        return player_x, player_y

    def _decide_direction(
        self,
        board: MazeBoard,
        cur_gx: int,
        cur_gy: int,
        player_x: int,
        player_y: int,
        target_x: int,
        target_y: int,
        other_ghosts_pos: Optional[List[Tuple[int, int]]] = None,
    ) -> None:
        """Pick best corridor turn using BFS and prevent reverse loops."""
        priority_dirs = self._get_directional_priority()

        effective_heading = (
            self.current_direction
            if self.current_direction != Direction.NONE
            else self.last_heading
        )
        forbidden_dir = effective_heading.opposite

        valid_dirs: List[Direction] = [
            d
            for d in priority_dirs
            if d != forbidden_dir and self.can_move(board, d, cur_gx, cur_gy)
        ]

        if not valid_dirs:
            if self.can_move(board, forbidden_dir, cur_gx, cur_gy):
                valid_dirs.append(forbidden_dir)

        if not valid_dirs:
            return

        crowd_set = set(other_ghosts_pos) if other_ghosts_pos else set()

        if self.data.is_edible and not self.is_eaten:
            dist_map = self._bfs_distance_map(board, (player_x, player_y))

            def flee_score(d: Direction) -> int:
                dx, dy = d.vector
                cand_pos = (cur_gx + dx, cur_gy + dy)
                penalty = _CROWD_PENALTY_FLEE if cand_pos in crowd_set else 0
                return dist_map.get(cand_pos, -1) - penalty

            max_score = max(flee_score(d) for d in valid_dirs)
            best_dirs = [d for d in valid_dirs if flee_score(d) == max_score]
            self.next_direction = max(
                best_dirs,
                key=lambda d: self.euclidean_distance_sq(
                    float(cur_gx + d.vector[0]),
                    float(cur_gy + d.vector[1]),
                    float(player_x),
                    float(player_y),
                ),
            )
            return

        dist_map = self._bfs_distance_map(board, (target_x, target_y))

        def chase_cost(d: Direction) -> int:
            dx, dy = d.vector
            cand_pos = (cur_gx + dx, cur_gy + dy)
            penalty = _CROWD_PENALTY_CHASE if cand_pos in crowd_set else 0
            return dist_map.get(cand_pos, 999999) + penalty

        best_dir = min(valid_dirs, key=chase_cost)
        if chase_cost(best_dir) >= 999999:
            best_dir = min(
                valid_dirs,
                key=lambda d: self.euclidean_distance_sq(
                    float(cur_gx + d.vector[0]),
                    float(cur_gy + d.vector[1]),
                    float(target_x),
                    float(target_y),
                ),
            )

        self.next_direction = best_dir

    def update(
        self,
        board: MazeBoard,
        player_x: int,
        player_y: int,
        player_dir: Direction,
        blinky_pos: Optional[Tuple[int, int]] = None,
        other_ghosts_pos: Optional[List[Tuple[int, int]]] = None,
    ) -> None:
        """Advance ghost physics, handle mode timers, and trigger AI."""
        if self.data.is_edible:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.data.is_edible = False
                self.speed = self.normal_speed

        if self.is_eaten:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.reset_to_spawn()
                return

        tile_sz: int = self.tile_size
        cur_gx, cur_gy = self.get_current_grid_coords()
        target_px: float = float(cur_gx * tile_sz)
        target_py: float = float(cur_gy * tile_sz)

        if (
            abs(self.pixel_x - target_px) <= self.speed
            and abs(self.pixel_y - target_py) <= self.speed
        ):
            if (
                self.is_eaten
                and cur_gx == self.spawn_x
                and cur_gy == self.spawn_y
            ):
                self.reset_to_spawn()
                return

            target_x, target_y = self._choose_target(
                board, player_x, player_y, player_dir, blinky_pos
            )
            self._decide_direction(
                board,
                cur_gx,
                cur_gy,
                player_x,
                player_y,
                target_x,
                target_y,
                other_ghosts_pos=other_ghosts_pos,
            )

        if self.current_direction != Direction.NONE:
            self.last_heading = self.current_direction

        self.advance_pixel_position(board)
        self.data.direction = self.current_direction
