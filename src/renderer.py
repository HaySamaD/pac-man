import pygame
from src.maze_board import TileType, MazeBoard


class Renderer:
    def __init__(self, board: MazeBoard, tile_size: int = 40):
        self.board = board
        self.tile_size = tile_size
        self.maze_pixel_w = board.width * tile_size
        self.maze_pixel_h = board.height * tile_size

        # Classec Pac-Man colores
        self.COLOR_BG = "black"
        self.COLOR_WALL = "blue"
        self.COLOR_PACGUM = (255, 183, 174)
        self.COLOR_SUPER = "white"

        pygame.init()
        info = pygame.display.Info()
        self.screen_w = info.current_w
        self.screen_h = info.current_h
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), pygame.FULLSCREEN)
        pygame.display.set_caption("Pac-Man")

        self.offset_x = (self.screen_w - self.maze_pixel_w) // 2
        self.offset_y = (self.screen_h - self.maze_pixel_h) // 2

        self.clock = pygame.time.Clock()

    def render_map(self):
        self.screen.fill(self.COLOR_BG)
        ts = self.tile_size

        for y in range(self.board.height):
            for x in range(self.board.width):
                tile = self.board.grid[y][x]
                px = self.offset_x + x * ts
                py = self.offset_y + y * ts
                center = (px + ts // 2, py + ts // 2)

                if tile == TileType.WALL:
                    # nrsmo l7itt kamostatil
                    pygame.draw.rect(self.screen, self.COLOR_WALL, (px, py, ts, ts))
                elif tile == TileType.PACGUM:
                    # hh yup nrsmo no9tta sghira
                    pygame.draw.circle(self.screen, self.COLOR_PACGUM, center, 3)
                elif tile == TileType.SUPER_PACGUM:
                    # nrsmo no9tta kbira
                    pygame.draw.circle(self.screen, self.COLOR_SUPER, center, 6)

    def update_desplay(self):
        pygame.display.flip()
        self.clock.tick(60)
