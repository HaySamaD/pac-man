"""Renderer module: draws the maze and game objects on screen."""

import os
import pygame
from src.maze_board import TileType, MazeBoard


class Renderer:
    """Game renderer using MLX-compatible Pygame functions."""

    def __init__(
        self,
        board: MazeBoard,
        tile_size: int = 40,
        assets_dir: str = "assets",
    ) -> None:
        """Set up screen, compute offsets, and load image textures.

        ELI5:
        1. Save the map data and tile size.
        2. Open a fullscreen window.
        3. Center the maze in the middle of the screen.
        4. Load picture files into memory.
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
        self.img_wall: pygame.Surface = pygame.image.load(
            os.path.join(assets_dir, "tile_wall.png")
        ).convert_alpha()
        self.img_pacgum: pygame.Surface = pygame.image.load(
            os.path.join(assets_dir, "pacgum.png")
        ).convert_alpha()
        self.img_super_pacgum: pygame.Surface = pygame.image.load(
            os.path.join(assets_dir, "super_pacgum.png")
        ).convert_alpha()

    # =========================================================================
    # Helper 1: Put a horizontal line pixel by pixel (like mlx_pixel_put)
    # =========================================================================
    def _put_h(self, x1: int, x2: int, y: int, th: int = 2) -> None:
        """Draw a flat line from x1 to x2 with thickness th."""
        for t in range(th):
            for px in range(x1, x2):
                self.screen.set_at((px, y + t), self.COLOR_WALL)

    # =========================================================================
    # Helper 2: Put a vertical line pixel by pixel (like mlx_pixel_put)
    # =========================================================================
    def _put_v(self, x: int, y1: int, y2: int, th: int = 2) -> None:
        """Draw an upright line from y1 to y2 with thickness th."""
        for t in range(th):
            for py in range(y1, y2):
                self.screen.set_at((x + t, py), self.COLOR_WALL)

    # =========================================================================
    # Main Render: Draw the whole board on screen
    # =========================================================================
    def render_map(self) -> None:
        """Clear screen and draw tiles, pac-gums, and walls.

        ELI5:
        1. Paint the entire background black.
        2. Loop over every cell in the grid.
        3. If it is block 42, stamp the wall picture.
        4. If it has a dot, stamp the dot picture.
        5. Check numbers (1, 2, 4, 8) and draw thin wall borders.
        """
        # 1. Clear old screen frame
        self.screen.fill(self.COLOR_BG)
        ts: int = self.tile_size
        th: int = 2

        # 2. Check each cell one by one
        for y in range(self.board.height):
            for x in range(self.board.width):
                tile: int = self.board.grid[y][x]
                val: int = self.board.raw_maze[y][x]

                # Convert grid (x, y) to real screen pixels (px, py)
                px: int = self.offset_x + x * ts
                py: int = self.offset_y + y * ts

                # Case A: Solid block 42 (number 15 means fully closed wall)
                if val == 15:
                    self.screen.blit(self.img_wall, (px, py))
                    continue

                # Case B: Draw dots (small dot or big super dot)
                if tile == int(TileType.PACGUM):
                    self.screen.blit(self.img_pacgum, (px, py))
                elif tile == int(TileType.SUPER_PACGUM):
                    self.screen.blit(self.img_super_pacgum, (px, py))

                # Case C: Draw thin wall edges using binary bits
                # Bit 1 = Top wall (North)
                if val & 1:
                    self._put_h(px, px + ts, py, th)

                # Bit 2 = Right wall (East)
                if val & 2:
                    self._put_v(px + ts - th, py, py + ts, th)

                # Bit 4 = Bottom wall (South)
                if val & 4:
                    self._put_h(px, px + ts, py + ts - th, th)

                # Bit 8 = Left wall (West)
                if val & 8:
                    self._put_v(px, py, py + ts, th)

    # =========================================================================
    # Display Update: Show frame and limit FPS (like mlx_loop_hook)
    # =========================================================================
    def update_desplay(self) -> None:
        """Show new frame on screen and wait to keep 60 FPS."""
        pygame.display.flip()
        self.clock.tick(60)
