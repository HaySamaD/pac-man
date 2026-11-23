"""Graphics renderer strictly using MLX-equivalent Pygame primitives."""

import os
from typing import Dict, List, Optional, Tuple

import pygame

from ...d2_classes import TileType
from .m1_maze_board import MazeBoard
from .m4_player import PlayerController
from .m5_ghost import GhostController


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
        self.hud_height: int = self.screen_h // 100
        self.offset_x: int = 0
        self.offset_y: int = 0

        self.color_bg: Tuple[int, int, int] = (12, 12, 16)
        self.color_wall: Tuple[int, int, int] = (40, 65, 135)
        self.color_block: Tuple[int, int, int] = (30, 48, 102)

        self.tile_imgs: Dict[int, pygame.Surface] = {
            TileType.PACGUM: self.load_img("assets/pacgum's", "pacgum.png"),
            TileType.SUPER_PACGUM: self.load_img(
                "assets/pacgum's", "super_pacgum.png"
            ),
        }
        self.img_eyes: pygame.Surface = self.load_img(
            "assets/ghost/dead_eyes", "ghost_dead_eyes.png"
        )
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

    def load_img(self, *parts: str) -> pygame.Surface:
        """Load an image file with alpha transparency."""
        img: pygame.Surface = pygame.image.load(
            os.path.join(*parts)
        ).convert_alpha()
        return img

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

    def fill_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: Tuple[int, int, int],
    ) -> None:
        """Fill rectangular region pixel-by-pixel."""
        x0: int = max(0, x)
        y0: int = max(0, y)
        x1: int = min(self.screen_w, x + w)
        y1: int = min(self.screen_h, y + h)
        for py in range(y0, y1):
            for px in range(x0, x1):
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
                    self.fill_rect(px, py, ts, th, self.color_wall)
                if val & 2:
                    self.fill_rect(
                        px + ts - th, py, th, ts, self.color_wall
                    )
                if val & 4:
                    self.fill_rect(
                        px, py + ts - th, ts, th, self.color_wall
                    )
                if val & 8:
                    self.fill_rect(px, py, th, ts, self.color_wall)

    def load_player_sprites(
        self, folder: str
    ) -> Dict[str, List[pygame.Surface]]:
        """Load Pac-Man animation frames for each movement direction."""
        sprites: Dict[str, List[pygame.Surface]] = {}
        for d in ("RIGHT", "LEFT", "UP", "DOWN"):
            low: str = d.lower()
            frames: List[pygame.Surface] = [
                self.load_img(folder, f"pacman_{low}_{state}.png")
                for state in ("closed", "half", "open")
            ]
            sprites[d] = [frames[0], frames[1], frames[2], frames[1]]
        sprites["NONE"] = sprites["RIGHT"]
        return sprites

    def load_ghost_sprites(
        self, folder: str
    ) -> Dict[str, Dict[str, List[pygame.Surface]]]:
        """Load animation frames for ghosts and frightened states."""
        sprites: Dict[str, Dict[str, List[pygame.Surface]]] = {}
        for name in ("blinky", "pinky", "inky", "clyde"):
            sprites[name] = {
                d: [
                    self.load_img(folder, name, f"ghost_{name}_{d}_f{i}.png")
                    for i in (0, 1)
                ]
                for d in ("right", "left", "up", "down")
            }
        sprites["frightened"] = {
            col: [
                self.load_img(
                    folder, "frightened", f"ghost_frightened_{col}_f{i}.png"
                )
                for i in (0, 1)
            ]
            for col in ("blue", "white")
        }
        return sprites

    def get_ghost_sprite(self, ghost: GhostController) -> pygame.Surface:
        """Select the appropriate animation frame for a ghost."""
        if ghost.is_eaten:
            return self.img_eyes
        f_idx: int = (ghost.anim_frame // 2) % 2
        if ghost.data.is_edible:
            flash: bool = (
                ghost.frightened_timer < 120
                and (ghost.frightened_timer // 15) % 2 == 1
            )
            col: str = "white" if flash else "blue"
            return self.ghost_sprites["frightened"][col][f_idx]
        g_name: str = ghost.data.ghost_type.lower()
        g_dir: str = ghost.current_direction.lower()
        if g_dir not in ("right", "left", "up", "down"):
            g_dir = "up"
        return self.ghost_sprites[g_name][g_dir][f_idx]

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
                img: Optional[pygame.Surface] = self.tile_imgs.get(
                    self.board.grid[y][x]
                )
                if img is not None:
                    self.screen.blit(
                        img,
                        (self.offset_x + x * ts, self.offset_y + y * ts),
                    )

        p_dir: str = player.data.direction
        if p_dir == "NONE" or p_dir not in self.player_sprites:
            p_dir = player.next_direction
        if p_dir == "NONE" or p_dir not in self.player_sprites:
            p_dir = "RIGHT"
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
            self.screen.blit(
                self.get_ghost_sprite(ghost),
                (
                    self.offset_x + int(ghost.pixel_x),
                    self.offset_y + int(ghost.pixel_y),
                ),
            )
