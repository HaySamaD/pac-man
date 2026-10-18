"""Renderer module managing screen drawing, animations, and wall baking."""

import os
from typing import Dict, List, Tuple
import pygame
from src.d0_helpers.m0_colors_RGB import Rgb
from src.ghost import GhostController
from src.maze_board import MazeBoard, TileType
from src.player import PlayerController


class Renderer:
    """Arcade graphics renderer strictly using MLX-equivalent primitives."""

    def __init__(
        self,
        board: MazeBoard,
        tile_size: int = 40,
    ) -> None:
        """Initialize window, load textures, and bake static maze walls."""
        self.board: MazeBoard = board
        self.tile_size: int = tile_size
        self.maze_pixel_w: int = board.width * tile_size
        self.maze_pixel_h: int = board.height * tile_size

        self.color_bg: Tuple[int, int, int] = Rgb.BLACK
        self.color_wall: Tuple[int, int, int] = Rgb.WALL_BLUE
        self.color_block_fill: Tuple[int, int, int] = Rgb.BLOCK_BLUE

        pygame.init()
        self.screen_w: int = 1920
        self.screen_h: int = 1080
        self.screen: pygame.Surface = pygame.display.set_mode(
            (self.screen_w, self.screen_h), pygame.FULLSCREEN
        )
        pygame.display.set_caption("Pac-Man")

        self.hud_height: int = self.screen_h * 10 // 100
        self.offset_x: int = (self.screen_w - self.maze_pixel_w) // 2
        avail_h: int = self.screen_h - self.hud_height
        self.offset_y: int = self.hud_height + (
            avail_h - self.maze_pixel_h
        ) // 2

        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.img_pacgum: pygame.Surface = pygame.image.load(
            os.path.join("assets/pacgum's", "pacgum.png")
        ).convert_alpha()
        self.img_super_pacgum: pygame.Surface = pygame.image.load(
            os.path.join("assets/pacgum's", "super_pacgum.png")
        ).convert_alpha()
        self.img_dead_eyes: pygame.Surface = pygame.image.load(
            os.path.join("assets/ghost/dead_eyes", "ghost_dead_eyes.png")
        ).convert_alpha()

        self.player_sprites: Dict[str, List[pygame.Surface]] = (
            self._load_player_sprites("assets/pacman")
        )
        self.ghost_sprites: Dict[str, Dict[str, List[pygame.Surface]]] = (
            self._load_ghost_sprites("assets")
        )

        self.maze_surface: pygame.Surface = pygame.Surface(
            (self.screen_w, self.screen_h)
        ).convert()
        self._bake_static_walls()

    def set_board(self, board: MazeBoard) -> None:
        """Switch active board when transitioning between multiple levels."""
        self.board = board
        self.maze_pixel_w = board.width * self.tile_size
        self.maze_pixel_h = board.height * self.tile_size
        self.offset_x = (self.screen_w - self.maze_pixel_w) // 2
        avail_h: int = self.screen_h - self.hud_height
        self.offset_y = self.hud_height + (
            avail_h - self.maze_pixel_h
        ) // 2
        self._bake_static_walls()

    def _put_h(
        self,
        surface: pygame.Surface,
        x1: int,
        x2: int,
        y: int,
        thickness: int = 2,
    ) -> None:
        """Draw horizontal line pixel-by-pixel."""
        for t in range(thickness):
            for px in range(x1, x2):
                if 0 <= px < self.screen_w and 0 <= (y + t) < self.screen_h:
                    surface.set_at((px, y + t), self.color_wall)

    def _put_v(
        self,
        surface: pygame.Surface,
        x: int,
        y1: int,
        y2: int,
        thickness: int = 2,
    ) -> None:
        """Draw vertical line pixel-by-pixel."""
        for t in range(thickness):
            for py in range(y1, y2):
                if 0 <= (x + t) < self.screen_w and 0 <= py < self.screen_h:
                    surface.set_at((x + t, py), self.color_wall)

    def _fill_rect(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        """Fill solid rectangle pixel-by-pixel without using pygame.draw."""
        for row in range(height):
            for col in range(width):
                px: int = x + col
                py: int = y + row
                if 0 <= px < self.screen_w and 0 <= py < self.screen_h:
                    surface.set_at((px, py), self.color_block_fill)

    def _bake_static_walls(self) -> None:
        """Render all maze bitmask walls once into cached surface."""
        self.maze_surface.fill(self.color_bg)
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
                    self._fill_rect(self.maze_surface, px, py, ts, ts)

                if val & 1:
                    self._put_h(self.maze_surface, px, px + ts, py, th)

                if val & 2:
                    self._put_v(
                        self.maze_surface, px + ts - th, py, py + ts, th
                    )

                if val & 4:
                    self._put_h(
                        self.maze_surface, px, px + ts, py + ts - th, th
                    )

                if val & 8:
                    self._put_v(self.maze_surface, px, py, py + ts, th)

    def _load_player_sprites(
        self,
        assets_dir: str,
    ) -> Dict[str, List[pygame.Surface]]:
        """Load Pac-Man walking animation frames for all 4 headings."""
        dir_keys: Dict[str, str] = {
            "RIGHT": "right",
            "LEFT": "left",
            "UP": "up",
            "DOWN": "down",
            "NONE": "right",
        }
        sprites: Dict[str, List[pygame.Surface]] = {}
        for key, name in dir_keys.items():
            f0: pygame.Surface = pygame.image.load(
                os.path.join(assets_dir, f"pacman_{name}_closed.png")
            ).convert_alpha()
            f1: pygame.Surface = pygame.image.load(
                os.path.join(assets_dir, f"pacman_{name}_half.png")
            ).convert_alpha()
            f2: pygame.Surface = pygame.image.load(
                os.path.join(assets_dir, f"pacman_{name}_open.png")
            ).convert_alpha()
            sprites[key] = [f0, f1, f2, f1]

        return sprites

    def _load_ghost_sprites(
        self,
        assets_dir: str,
    ) -> Dict[str, Dict[str, List[pygame.Surface]]]:
        """Load animation frames for all 4 ghosts across all modes."""
        names: List[str] = ["blinky", "pinky", "inky", "clyde"]
        dirs: List[str] = ["right", "left", "up", "down"]
        sprites: Dict[str, Dict[str, List[pygame.Surface]]] = {}
        ghost_base: str = os.path.join(assets_dir, "ghost")

        for name in names:
            sprites[name] = {}
            folder: str = os.path.join(ghost_base, name)
            for d in dirs:
                f0: pygame.Surface = pygame.image.load(
                    os.path.join(folder, f"ghost_{name}_{d}_f0.png")
                ).convert_alpha()
                f1: pygame.Surface = pygame.image.load(
                    os.path.join(folder, f"ghost_{name}_{d}_f1.png")
                ).convert_alpha()
                sprites[name][d] = [f0, f1]

        frightened_dir: str = os.path.join(ghost_base, "frightened")
        b0: pygame.Surface = pygame.image.load(
            os.path.join(frightened_dir, "ghost_frightened_blue_f0.png")
        ).convert_alpha()
        b1: pygame.Surface = pygame.image.load(
            os.path.join(frightened_dir, "ghost_frightened_blue_f1.png")
        ).convert_alpha()
        w0: pygame.Surface = pygame.image.load(
            os.path.join(frightened_dir, "ghost_frightened_white_f0.png")
        ).convert_alpha()
        w1: pygame.Surface = pygame.image.load(
            os.path.join(frightened_dir, "ghost_frightened_white_f1.png")
        ).convert_alpha()

        sprites["frightened"] = {"blue": [b0, b1], "white": [w0, w1]}
        return sprites

    def render_ghost(self, ghost: GhostController) -> None:
        """Render ghost sprite on screen based on active state and heading."""
        render_x: int = self.offset_x + int(ghost.pixel_x)
        render_y: int = self.offset_y + int(ghost.pixel_y)

        if ghost.is_eaten:
            self.screen.blit(self.img_dead_eyes, (render_x, render_y))
            return

        frame_idx: int = (ghost.anim_frame // 2) % 2

        if ghost.data.is_edible:
            state_color: str = "blue"
            if (
                ghost.frightened_timer < 120
                and (ghost.frightened_timer // 15) % 2
            ):
                state_color = "white"
            sprite: pygame.Surface = (
                self.ghost_sprites["frightened"][state_color][frame_idx]
            )
            self.screen.blit(sprite, (render_x, render_y))
            return

        name: str = str(ghost.data.ghost_type.value).lower()
        dir_key: str = str(ghost.current_direction.value).lower()
        if dir_key not in ["right", "left", "up", "down"]:
            dir_key = "up"

        sprite = self.ghost_sprites[name][dir_key][frame_idx]
        self.screen.blit(sprite, (render_x, render_y))

    def render_player(self, controller: PlayerController) -> None:
        """Render Pac-Man sprite animated according to heading direction."""
        current_dir = controller.data.direction
        direction_key: str = str(current_dir.value)

        if direction_key == "NONE":
            next_dir = controller.next_direction
            if str(next_dir.value) != "NONE":
                direction_key = str(next_dir.value)
            else:
                direction_key = "RIGHT"

        if direction_key not in self.player_sprites:
            direction_key = "RIGHT"

        frame_idx: int = controller.anim_frame % 4
        sprite: pygame.Surface = (
            self.player_sprites[direction_key][frame_idx]
        )
        render_x: int = self.offset_x + int(controller.pixel_x)
        render_y: int = self.offset_y + int(controller.pixel_y)
        self.screen.blit(sprite, (render_x, render_y))

    def render_map(self) -> None:
        """Stamp pre-baked static maze surface and dynamic collectibles."""
        self.screen.blit(self.maze_surface, (0, 0))
        ts: int = self.tile_size

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

    def update_display(self) -> None:
        """Present back-buffer frame on monitor and throttle loop to 60 FPS."""
        pygame.display.flip()
        self.clock.tick(60)
