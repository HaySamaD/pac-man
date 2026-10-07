import os
import pygame
from src.maze_board import TileType, MazeBoard


class Renderer:
    def __init__(self, board: MazeBoard, tile_size: int = 40, assets_dir: str = "assets"):
        self.board = board
        self.tile_size = tile_size

        self.maze_pixel_w = board.width * tile_size
        self.maze_pixel_h = board.height * tile_size

        # Eye-soothing colors (Neon Retro)
        self.COLOR_BG = (10, 10, 15)           # Dark greyish eyeliner
        self.COLOR_WALL = (0, 180, 216)        # Cyan: calm and elegant.
        self.COLOR_WALL_BLOCK = (0, 119, 182)  # Consistent grade for Block 42

        pygame.init()

        self.screen_w = 1920
        self.screen_h = 1080
        self.screen = pygame.display.set_mode(
            (self.screen_w, self.screen_h), pygame.FULLSCREEN
        )
        pygame.display.set_caption("Pac-Man")

        # Reserve space for the top HUD.
        self.hud_height = 100
        self.offset_x = (self.screen_w - self.maze_pixel_w) // 2
        available_h = self.screen_h - self.hud_height
        self.offset_y = self.hud_height + (available_h - self.maze_pixel_h) // 2

        self.clock = pygame.time.Clock()

        # Download ready-made images (textures)
        self.img_pacgum = pygame.image.load(os.path.join(assets_dir, "pacgum.png")).convert_alpha()
        self.img_super_pacgum = pygame.image.load(os.path.join(assets_dir, "super_pacgum.png")).convert_alpha()

        # Creating a wall block (42) in a coordinated color.
        self.block_surf = pygame.Surface((self.tile_size, self.tile_size))
        self.block_surf.fill(self.COLOR_WALL_BLOCK)

    # Helper functions for drawing lines (equivalent to mlx_pixel_put)
    def _draw_h_line(self, x1: int, x2: int, y: int, th: int = 3):
        for t in range(th):
            py = y + t
            for px in range(x1, x2 + 1):
                self.screen.set_at((px, py), self.COLOR_WALL)

    def _draw_v_line(self, x: int, y1: int, y2: int, th: int = 3):
        for t in range(th):
            px = x + t
            for py in range(y1, y2 + 1):
                self.screen.set_at((px, py), self.COLOR_WALL)

    def render_map(self):
        self.screen.fill(self.COLOR_BG)
        ts = self.tile_size
        th = 3  # Line thickness (light and comfortable)

        for y in range(self.board.height):
            for x in range(self.board.width):
                tile = self.board.grid[y][x]
                val = self.board.raw_maze[y][x]
                px = self.offset_x + x * ts
                py = self.offset_y + y * ts

                # 1. Block 42
                if val == 15:
                    self.screen.blit(self.block_surf, (px, py))
                    continue

                # 2. Points
                if tile == TileType.PACGUM:
                    self.screen.blit(self.img_pacgum, (px, py))
                elif tile == TileType.SUPER_PACGUM:
                    self.screen.blit(self.img_super_pacgum, (px, py))

                # 3. Wall lines based on bits
                if val & 1:  # North
                    self._draw_h_line(px, px + ts, py, th)
                if val & 2:  # East
                    self._draw_v_line(px + ts - th, py, py + ts, th)
                if val & 4:  # South
                    self._draw_h_line(px, px + ts, py + ts - th, th)
                if val & 8:  # West
                    self._draw_v_line(px, py, py + ts, th)

    def update_desplay(self):
        pygame.display.flip()
        self.clock.tick(60)
