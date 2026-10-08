"""Maze board module: manages grid data, walls, and dots."""

from dataclasses import dataclass
from enum import IntEnum
import random
from typing import Optional


# =============================================================================
# 1. TILE ENUM DEFINITION
# =============================================================================
class TileType(IntEnum):
    """Simple numbers representing what is inside each grid cell."""

    EMPTY = 0
    WALL = 1
    PACGUM = 2
    SUPER_PACGUM = 3


# =============================================================================
# 2. MAZE BOARD DATA CLASS
# =============================================================================
@dataclass
class MazeBoard:
    """Store the grid map, generator numbers, and remaining dot count."""

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
        """Build and populate a MazeBoard instance.

        ELI5:
        1. Measure how many rows and columns the maze has.
        2. Create an empty 2D grid filled with zeros.
        3. Separate full walls (number 15) from open walking paths.
        4. Reserve the 4 outer corners for big power pellets.
        5. Check if the config asked for fewer dots than available.
        6. Pick random spots and drop small pac-gums.
        7. Place big super pac-gums in open corners.
        8. Return the finished board object ready to play.
        """
        # =====================================================================
        # Step 1: Read dimensions and build an empty grid (all zeros)
        # =====================================================================
        height: int = len(raw_maze)
        width: int = len(raw_maze[0])
        grid: list[list[int]] = [
            [int(TileType.EMPTY) for _ in range(width)]
            for _ in range(height)
        ]
        valid_paths: list[tuple[int, int]] = []

        # =====================================================================
        # Step 2: Find solid blocks and walkable paths
        # =====================================================================
        # Number 15 means all four walls are closed (solid block 42)
        for y in range(height):
            for x in range(width):
                if raw_maze[y][x] == 15:
                    grid[y][x] = int(TileType.WALL)
                else:
                    valid_paths.append((x, y))

        # =====================================================================
        # Step 3: Find four outer corners for super pac-gums
        # =====================================================================
        # Coordinates of the four corners of the map
        corners: list[tuple[int, int]] = [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1),
        ]
        corner_set: set[tuple[int, int]] = set(corners)

        # Keep paths that are not corners for regular small dots
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
                # Log a clear warning message and keep playing safely
                print(
                    f"[CONFIG WARNING] Invalid max_pacgums value "
                    f"({max_pacgums}).\n"
                    f"    Must be between 1 and {total_available}.\n"
                    f"    Falling back to default ({total_available})."
                )

        # =====================================================================
        # Step 5: Place normal pac-gums randomly on the paths
        # =====================================================================
        # Choose random cell spots based on target count
        selected_paths: list[tuple[int, int]] = random.sample(
            regular_paths, target_count
        )
        gums_count: int = 0

        for x, y in selected_paths:
            grid[y][x] = int(TileType.PACGUM)
            gums_count += 1

        # =====================================================================
        # Step 6: Place super pac-gums in the 4 corners
        # =====================================================================
        # If a corner is an open corridor, place a super pellet there
        for cx, cy in corners:
            if 0 <= cy < height and 0 <= cx < width:
                if grid[cy][cx] != int(TileType.WALL):
                    grid[cy][cx] = int(TileType.SUPER_PACGUM)
                    gums_count += 1

        # =====================================================================
        # Step 7: Pack everything into a new MazeBoard object
        # =====================================================================
        return cls(
            width=width,
            height=height,
            grid=grid,
            raw_maze=raw_maze,
            remaining_pacgums=gums_count,
        )
