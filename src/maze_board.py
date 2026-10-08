"""Maze board representation and grid state manager for Pac-Man."""

from dataclasses import dataclass
from enum import IntEnum
import random
from typing import Optional


# =============================================================================
# 1. TILE ENUM DEFINITION
# =============================================================================
class TileType(IntEnum):
    """Tile types on the grid."""

    EMPTY = 0
    WALL = 1
    PACGUM = 2
    SUPER_PACGUM = 3


# =============================================================================
# 2. MAZE BOARD DATA CLASS
# =============================================================================
@dataclass
class MazeBoard:
    """Maze grid data and state."""

    width: int
    height: int
    grid: list[list[int]]
    raw_maze: list[list[int]]
    remaining_pacgums: int = 0

    @classmethod
    def from_raw_maze(
        cls,
        raw_maze: list[list[int]],
        max_pacgums: Optional[int] = None,
    ) -> "MazeBoard":
        """Create a MazeBoard object from raw maze numbers.

        Args:
            raw_maze: 2D list of numbers from maze generator.
            max_pacgums: Optional max limit of pac-gums.

        Returns:
            A new MazeBoard instance.
        """
        # =====================================================================
        # Step 1: Read dimensions and build an empty grid
        # =====================================================================
        height: int = len(raw_maze)
        width: int = len(raw_maze[0])
        grid: list[list[int]] = [
            [int(TileType.EMPTY) for _ in range(width)]
            for _ in range(height)
        ]
        valid_paths: list[tuple[int, int]] = []

        # =====================================================================
        # Step 2: Find solid walls and open paths
        # =====================================================================
        # 15 means a full wall block
        for y in range(height):
            for x in range(width):
                if raw_maze[y][x] == 15:
                    grid[y][x] = int(TileType.WALL)
                else:
                    valid_paths.append((x, y))

        # =====================================================================
        # Step 3: Find four corners for super pac-gums
        # =====================================================================
        # Save four corner coordinates
        corners: list[tuple[int, int]] = [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1),
        ]
        corner_set: set[tuple[int, int]] = set(corners)

        # Remove corners from normal path list
        regular_paths: list[tuple[int, int]] = [
            pos for pos in valid_paths if pos not in corner_set
        ]

        # =====================================================================
        # Step 4: Validate config limit and pick target count
        # =====================================================================
        total_available: int = len(regular_paths)
        target_count: int = total_available

        if max_pacgums is not None:
            if 0 < max_pacgums <= total_available:
                target_count = max_pacgums
            else:
                # Print warning and use default count
                print(
                    f"[CONFIG WARNING] Invalid max_pacgums value "
                    f"({max_pacgums}).\n"
                    f"    Must be between 1 and {total_available}.\n"
                    f"    Falling back to default ({total_available})."
                )

        # =====================================================================
        # Step 5: Place normal pac-gums randomly
        # =====================================================================
        # Pick random spots for regular pac-gums
        selected_paths: list[tuple[int, int]] = random.sample(
            regular_paths, target_count
        )
        gums_count: int = 0

        for x, y in selected_paths:
            grid[y][x] = int(TileType.PACGUM)
            gums_count += 1

        # =====================================================================
        # Step 6: Place super pac-gums in corners
        # =====================================================================
        # Add super pac-gums to open corners
        for cx, cy in corners:
            if 0 <= cy < height and 0 <= cx < width:
                if grid[cy][cx] != int(TileType.WALL):
                    grid[cy][cx] = int(TileType.SUPER_PACGUM)
                    gums_count += 1

        # =====================================================================
        # Step 7: Return final board object
        # =====================================================================
        return cls(
            width=width,
            height=height,
            grid=grid,
            raw_maze=raw_maze,
            remaining_pacgums=gums_count,
        )
