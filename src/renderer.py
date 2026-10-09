"""Renderer module: draws the maze and game objects on screen."""

import os
import pygame
from src.maze_board import TileType, MazeBoard


class Renderer:
    """Game renderer using cached surface and bitwise wall parsing."""

    def __init__(
        self,
        board: MazeBoard,
        tile_size: int = 40,
        assets_dir: str = "assets",
    ) -> None:
        """Set up screen, bake static walls, and load textures.

        Class Algo:
            1. Save the map data and tile size.
            2. Open a fullscreen window.
            3. Center the maze in the middle of the screen.
            4. Load picture files into memory.
            5. Pre-render (bake) all static walls once onto a cached surface.
        """
        # =====================================================================
        # Step 1: Save map information and compute pixel sizes
        # =====================================================================
        self.board: MazeBoard = board
        self.tile_size: int = tile_size

        # Total width and height of the maze in pixels
        self.maze_pixel_w: int = board.width * tile_size
        self.maze_pixel_h: int = board.height * tile_size

        # Theme colors: dark night background and gentle blue walls
        self.COLOR_BG: tuple[int, int, int] = (12, 12, 16)
        self.COLOR_WALL: tuple[int, int, int] = (40, 65, 135)
        self.COLOR_BLOCK_FILL: tuple[int, int, int] = (30, 48, 102)

        # =====================================================================
        # Step 2: Start pygame and open fullscreen window (like mlx_new_window)
        # =====================================================================
        pygame.init()

        self.screen_w: int = 1920
        self.screen_h: int = 1080
        self.screen: pygame.Surface = pygame.display.set_mode(
            (self.screen_w, self.screen_h), pygame.FULLSCREEN
        )
        pygame.display.set_caption("Pac-Man")

        # =====================================================================
        # Step 3: Leave room at the top for HUD and center the maze
        # =====================================================================
        # 100 pixels at the top reserved for score, lives, and time
        self.hud_height: int = 100

        # Center horizontally: split leftover width evenly on both sides
        self.offset_x: int = (self.screen_w - self.maze_pixel_w) // 2

        # Center vertically: split leftover space below the HUD
        available_h: int = self.screen_h - self.hud_height
        self.offset_y: int = self.hud_height + (
            available_h - self.maze_pixel_h
        ) // 2

        # Frame rate controller (keeps game running smoothly at 60 FPS)
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # =====================================================================
        # Step 4: Load images from disk (like mlx_xpm_file_to_image)
        # =====================================================================
        self.img_pacgum: pygame.Surface = pygame.image.load(
            os.path.join(assets_dir, "pacgum.png")
        ).convert_alpha()
        self.img_super_pacgum: pygame.Surface = pygame.image.load(
            os.path.join(assets_dir, "super_pacgum.png")
        ).convert_alpha()

        # =====================================================================
        # Step 5: Bake static maze walls into an off-screen surface
        # =====================================================================
        self.maze_surface: pygame.Surface = pygame.Surface(
            (self.screen_w, self.screen_h)
        ).convert()
        self.maze_surface.fill(self.COLOR_BG)
        self._bake_static_walls()

    # =========================================================================
    # Helper 1: Put a horizontal line on a surface (like mlx_pixel_put)
    # =========================================================================
    def _put_h(
        self,
        surface: pygame.Surface,
        x1: int,
        x2: int,
        y: int,
        th: int = 2,
    ) -> None:
        """Draw a flat line from x1 to x2 with thickness th."""
        for t in range(th):
            for px in range(x1, x2):
                if 0 <= px < self.screen_w and 0 <= (y + t) < self.screen_h:
                    surface.set_at((px, y + t), self.COLOR_WALL)

    # =========================================================================
    # Helper 2: Put a vertical line on a surface (like mlx_pixel_put)
    # =========================================================================
    def _put_v(
        self,
        surface: pygame.Surface,
        x: int,
        y1: int,
        y2: int,
        th: int = 2,
    ) -> None:
        """Draw an upright line from y1 to y2 with thickness th."""
        for t in range(th):
            for py in range(y1, y2):
                if 0 <= (x + t) < self.screen_w and 0 <= py < self.screen_h:
                    surface.set_at((x + t, py), self.COLOR_WALL)

    #   Visual Cell Diagram (Tile Coordinates & Offsets):
    #
    #   (px, py) ────────────────────────────────── (px + ts, py)
    #      │         Top Wall: Bit 1 (North)           │
    #      │                                           │
    #      │ Left: Bit 8                 Right: Bit 2  │
    #      │ (West)                      (East)        │
    #      │                                           │
    #      │        Bottom Wall: Bit 4 (South)         │
    #   (px, py + ts) ───────────────────────────── (px + ts, py + ts)

    # =========================================================================
    #Helper 3: Fill solid rectangular tile area pixel by pixel
    # =========================================================================
    def _fill_rect(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        w: int,
        h: int,
    ) -> None:
        """Fill a rectangle area pixel by pixel without using pygame.draw."""
        for row in range(h):
            for col in range(w):
                px = x + col
                py = y + row
                if 0 <= px < self.screen_w and 0 <= py < self.screen_h:
                    surface.set_at((px, py), self.COLOR_BLOCK_FILL,)

    # =========================================================================
    # Pre-render: Draw all maze lines once during startup
    # =========================================================================
    def _bake_static_walls(self) -> None:
        """Render all maze walls once at startup using bitwise checks.

        Bake Algo:
            1. Iterate over every grid coordinate (x, y).
            2. Skip empty tiles (value 0).
            3. Convert tile index to screen pixels.
            4. Check bit flags (1, 2, 4, 8) and draw matching wall lines.
        """
        ts: int = self.tile_size
        th: int = 2

        for y in range(self.board.height):
            for x in range(self.board.width):
                val: int = self.board.raw_maze[y][x]
                if val == 0:
                    continue

                # Convert grid (x, y) to screen pixels (px, py)
                px: int = self.offset_x + x * ts
                py: int = self.offset_y + y * ts

                # Special Case: Fill center '42' logo blocks (solid tile 15)
                if val == 15:
                    self._fill_rect(
                        self.maze_surface,
                        px,
                        py,
                        ts,
                        ts,
                    )

                # Bit 1 = Top wall (North)
                if val & 1:
                    self._put_h(self.maze_surface, px, px + ts, py, th)

                # Bit 2 = Right wall (East)
                if val & 2:
                    self._put_v(
                        self.maze_surface,
                        px + ts - th,
                        py,
                        py + ts,
                        th,
                    )

                # Bit 4 = Bottom wall (South)
                if val & 4:
                    self._put_h(
                        self.maze_surface,
                        px,
                        px + ts,
                        py + ts - th,
                        th,
                    )

                # Bit 8 = Left wall (West)
                if val & 8:
                    self._put_v(self.maze_surface, px, py, py + ts, th)

    # =========================================================================
    # Main Render: Draw the whole board on screen
    # =========================================================================
    def render_map(self) -> None:
        """Stamp baked walls and render remaining dots on top.

        Method Algo:
            1. Fast blit of the pre-rendered maze background.
            2. Loop over grid cells.
            3. Skip cells marked as EMPTY.
            4. Stamp dots or super dots on active positions.
        """
        # Step 1: Draw pre-rendered maze surface in a single blit call
        self.screen.blit(self.maze_surface, (0, 0))

        ts: int = self.tile_size

        # Step 2: Draw dynamic collectible dots on top
        for y in range(self.board.height):
            for x in range(self.board.width):
                tile: int = self.board.grid[y][x]
                if tile == int(TileType.EMPTY):
                    continue

                px: int = self.offset_x + x * ts
                py: int = self.offset_y + y * ts

                if tile == int(TileType.PACGUM):
                    self.screen.blit(self.img_pacgum, (px, py))
                elif tile == int(TileType.SUPER_PACGUM):
                    self.screen.blit(self.img_super_pacgum, (px, py))

    # =========================================================================
    # Display Update: Show frame and limit FPS (like mlx_loop_hook)
    # =========================================================================
    def update_display(self) -> None:
        """Show new frame on screen and wait to keep 60 FPS."""
        pygame.display.flip()
        self.clock.tick(60)
