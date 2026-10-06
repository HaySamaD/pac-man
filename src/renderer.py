import os
import pygame
from src.maze_board import TileType, MazeBoard


# =============================================================================

class Renderer:
    def __init__(
                        self,
                        board: MazeBoard,
                        tile_size: int = 40,
                        assets_dir: str = "assets"
            ) -> None:

        self.board = board
        self.tile_size = tile_size
        self.maze_pixel_w = board.width * tile_size
        self.maze_pixel_h = board.height * tile_size

        self.COLOR_BG = (0, 0, 0)

        pygame.init()
        info = pygame.display.Info()
        self.screen_w = info.current_w
        self.screen_h = info.current_h
        self.screen = pygame.display.set_mode(
            (self.screen_w, self.screen_h), pygame.FULLSCREEN
        )
        pygame.display.set_caption("Pac-Man")

        self.offset_x = (self.screen_w - self.maze_pixel_w) // 2
        self.offset_y = (self.screen_h - self.maze_pixel_h) // 2

        self.clock = pygame.time.Clock()

        wall_img = pygame.image.load(os.path.join(assets_dir, "tile_wall.png")).convert_alpha()
        gum_img = pygame.image.load(os.path.join(assets_dir, "pacgum.png")).convert_alpha()
        super_img = pygame.image.load(os.path.join(assets_dir, "super_pacgum.png")).convert_alpha()

        self.img_wall = pygame.transform.scale(wall_img, (self.tile_size, self.tile_size))
        self.img_pacgum = pygame.transform.scale(gum_img, (self.tile_size, self.tile_size))
        self.img_super_pacgum = pygame.transform.scale(super_img, (self.tile_size, self.tile_size))

    def render_map(self):
        self.screen.fill(self.COLOR_BG)
        ts = self.tile_size

        for y in range(self.board.height):
            for x in range(self.board.width):
                tile = self.board.grid[y][x]
                px = self.offset_x + x * ts
                py = self.offset_y + y * ts

                if tile == TileType.WALL:
                    self.screen.blit(self.img_wall, (px, py))
                elif tile == TileType.PACGUM:
                    self.screen.blit(self.img_pacgum, (px, py))
                elif tile == TileType.SUPER_PACGUM:
                    self.screen.blit(self.img_super_pacgum, (px, py))

    def update_desplay(self):
        pygame.display.flip()
        self.clock.tick(60)
