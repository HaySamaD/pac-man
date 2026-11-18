"""Graphics renderer strictly using MLX-equivalent Pygame primitives."""

import os
from typing import Dict, List, Tuple

import pygame

from ...d2_classes import TileType
from .m5_ghost import GhostController
from .m1_maze_board import MazeBoard
from .m4_player import PlayerController


class Renderer:
    """Renders static maze walls, collectibles, player, and ghosts."""

    def __init__(
        self,
        screen: pygame.Surface,
        board: MazeBoard,
        tile_size: int = 40,
    ) -> None:
        """Initialize textures and pre-bake maze walls onto surface."""
        self.screen: pygame.Surface = screen
        self.board: MazeBoard = board
        self.tile_size: int = tile_size
        self.screen_w: int = screen.get_width()
        self.screen_h: int = screen.get_height()
        self.hud_height: int = self.screen_h * 8 // 100
        self.offset_x: int = 0
        self.offset_y: int = 0

        self.color_bg: Tuple[int, int, int] = (12, 12, 16)
        self.color_wall: Tuple[int, int, int] = (40, 65, 135)
        self.color_block: Tuple[int, int, int] = (30, 48, 102)

        self.img_pacgum: pygame.Surface = pygame.image.load(
            os.path.join("assets/pacgum's", "pacgum.png")
        ).convert_alpha()
        self.img_super: pygame.Surface = pygame.image.load(
            os.path.join("assets/pacgum's", "super_pacgum.png")
        ).convert_alpha()
        self.img_eyes: pygame.Surface = pygame.image.load(
            os.path.join("assets/ghost/dead_eyes", "ghost_dead_eyes.png")
        ).convert_alpha()

        self.player_sprites: Dict[str, List[pygame.Surface]] = (
            self.load_player_sprites("assets/pacman")
        )
        self.ghost_sprites: Dict[str, Dict[str, List[pygame.Surface]]] = (
            self.load_ghost_sprites("assets/ghost")
        )
        self.maze_surface: pygame.Surface = pygame.Surface(
            (self.screen_w, self.screen_h)
        ).convert()
        self.set_board(board)

    def set_board(self, board: MazeBoard) -> None:
        """Update active maze board and bake its static walls."""
        self.board = board
        maze_w: int = board.width * self.tile_size
        maze_h: int = board.height * self.tile_size
        self.offset_x = max(0, (self.screen_w - maze_w) // 2)
        avail_h: int = self.screen_h - self.hud_height
        self.offset_y = max(
            self.hud_height, self.hud_height + (avail_h - maze_h) // 2
        )
        self.bake_walls()

    def put_h(
        self, x1: int, x2: int, y: int, thickness: int = 2
    ) -> None:
        """Draw horizontal wall segment pixel-by-pixel."""
        for t in range(thickness):
            for px in range(x1, x2):
                if 0 <= px < self.screen_w and 0 <= y + t < self.screen_h:
                    self.maze_surface.set_at((px, y + t), self.color_wall)

    def put_v(
        self, x: int, y1: int, y2: int, thickness: int = 2
    ) -> None:
        """Draw vertical wall segment pixel-by-pixel."""
        for t in range(thickness):
            for py in range(y1, y2):
                if 0 <= x + t < self.screen_w and 0 <= py < self.screen_h:
                    self.maze_surface.set_at((x + t, py), self.color_wall)

    def fill_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: Tuple[int, int, int],
    ) -> None:
        """Fill rectangular region pixel-by-pixel."""
        for row in range(h):
            for col in range(w):
                px: int = x + col
                py: int = y + row
                if 0 <= px < self.screen_w and 0 <= py < self.screen_h:
                    self.maze_surface.set_at((px, py), color)

    def bake_walls(self) -> None:
        """Pre-render maze background and walls once per level."""
        self.fill_rect(0, 0, self.screen_w, self.screen_h, self.color_bg)
        ts: int = self.tile_size
        th: int = 2
        for y in range(self.board.height):
            for x in range(self.board.width):
                val: int = self.board.raw_maze[y][x]
                if val == 0:
                    continue
                px: int = self.offset_x + x * ts
                py: int = self.offset_y + y * ts
                if val == 15:
                    self.fill_rect(px, py, ts, ts, self.color_block)
                if val & 1:
                    self.put_h(px, px + ts, py, th)
                if val & 2:
                    self.put_v(px + ts - th, py, py + ts, th)
                if val & 4:
                    self.put_h(px, px + ts, py + ts - th, th)
                if val & 8:
                    self.put_v(px, py, py + ts, th)

    def load_player_sprites(
        self, folder: str
    ) -> Dict[str, List[pygame.Surface]]:
        """Load Pac-Man animation frames for each movement direction."""
        mapping: Dict[str, str] = {
            "RIGHT": "right",
            "LEFT": "left",
            "UP": "up",
            "DOWN": "down",
            "NONE": "right",
        }
        sprites: Dict[str, List[pygame.Surface]] = {}
        for key, name in mapping.items():
            f0 = pygame.image.load(
                os.path.join(folder, f"pacman_{name}_closed.png")
            ).convert_alpha()
            f1 = pygame.image.load(
                os.path.join(folder, f"pacman_{name}_half.png")
            ).convert_alpha()
            f2 = pygame.image.load(
                os.path.join(folder, f"pacman_{name}_open.png")
            ).convert_alpha()
            sprites[key] = [f0, f1, f2, f1]
        return sprites

    def load_ghost_sprites(
        self, folder: str
    ) -> Dict[str, Dict[str, List[pygame.Surface]]]:
        """Load animation frames for ghosts and frightened states."""
        names: List[str] = ["blinky", "pinky", "inky", "clyde"]
        dirs: List[str] = ["right", "left", "up", "down"]
        sprites: Dict[str, Dict[str, List[pygame.Surface]]] = {}
        for name in names:
            sprites[name] = {}
            for d in dirs:
                f0 = pygame.image.load(
                    os.path.join(folder, name, f"ghost_{name}_{d}_f0.png")
                ).convert_alpha()
                f1 = pygame.image.load(
                    os.path.join(folder, name, f"ghost_{name}_{d}_f1.png")
                ).convert_alpha()
                sprites[name][d] = [f0, f1]

        f_dir: str = os.path.join(folder, "frightened")
        b0 = pygame.image.load(
            os.path.join(f_dir, "ghost_frightened_blue_f0.png")
        ).convert_alpha()
        b1 = pygame.image.load(
            os.path.join(f_dir, "ghost_frightened_blue_f1.png")
        ).convert_alpha()
        w0 = pygame.image.load(
            os.path.join(f_dir, "ghost_frightened_white_f0.png")
        ).convert_alpha()
        w1 = pygame.image.load(
            os.path.join(f_dir, "ghost_frightened_white_f1.png")
        ).convert_alpha()
        sprites["frightened"] = {"blue": [b0, b1], "white": [w0, w1]}
        return sprites

    def render_all(
        self,
        player: PlayerController,
        ghosts: List[GhostController],
    ) -> None:
        """Blit maze, collectibles, player, and ghosts onto screen."""
        self.screen.blit(self.maze_surface, (0, 0))
        ts: int = self.tile_size
        for y in range(self.board.height):
            for x in range(self.board.width):
                tile: int = self.board.grid[y][x]
                if tile == TileType.PACGUM:
                    self.screen.blit(
                        self.img_pacgum,
                        (self.offset_x + x * ts, self.offset_y + y * ts),
                    )
                elif tile == TileType.SUPER_PACGUM:
                    self.screen.blit(
                        self.img_super,
                        (self.offset_x + x * ts, self.offset_y + y * ts),
                    )

        p_dir: str = player.data.direction
        if p_dir == "NONE" or p_dir not in self.player_sprites:
            p_dir = (
                player.next_direction
                if player.next_direction in self.player_sprites
                and player.next_direction != "NONE"
                else "RIGHT"
            )
        p_sprite: pygame.Surface = self.player_sprites[p_dir][
            player.anim_frame % 4
        ]
        self.screen.blit(
            p_sprite,
            (
                self.offset_x + int(player.pixel_x),
                self.offset_y + int(player.pixel_y),
            ),
        )

        for ghost in ghosts:
            gx: int = self.offset_x + int(ghost.pixel_x)
            gy: int = self.offset_y + int(ghost.pixel_y)
            if ghost.is_eaten:
                self.screen.blit(self.img_eyes, (gx, gy))
                continue
            f_idx: int = (ghost.anim_frame // 2) % 2
            if ghost.data.is_edible:
                col: str = "blue"
                if (
                    ghost.frightened_timer < 120
                    and (ghost.frightened_timer // 15) % 2 == 1
                ):
                    col = "white"
                self.screen.blit(
                    self.ghost_sprites["frightened"][col][f_idx], (gx, gy)
                )
                continue
            g_name: str = ghost.data.ghost_type.lower()
            g_dir: str = ghost.current_direction.lower()
            if g_dir not in ("right", "left", "up", "down"):
                g_dir = "up"
            self.screen.blit(
                self.ghost_sprites[g_name][g_dir][f_idx], (gx, gy)
            )
