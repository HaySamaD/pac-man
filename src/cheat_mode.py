"""Cheat mode controller engine with pause menu UI integration."""

from typing import List, Optional, Tuple
import pygame
from src.d0_helpers.m0_colors_RGB import Rgb
from src.d1_classes.m1_dataclasses import GameState
from src.player import PlayerController


class CheatController:
    """Manage cheat state toggles and evaluation UI interactions."""

    def __init__(self, is_enabled: bool = False) -> None:
        """Initialize cheat states and UI geometry trackers."""
        self.is_enabled: bool = is_enabled
        self.god_mode: bool = is_enabled
        self.ghosts_frozen: bool = False
        self.speed_boost: bool = False
        self.base_speed: Optional[int] = None
        self.menu_open: bool = False
        self.btn_rect: pygame.Rect = pygame.Rect(760, 480, 400, 70)

    def set_enabled(self, enabled: bool) -> None:
        """Turn master cheat switch on or off cleanly."""
        self.is_enabled = enabled
        if enabled:
            self.god_mode = True
        else:
            self.god_mode = False
            self.ghosts_frozen = False
            self.speed_boost = False
            self.menu_open = False

    def toggle_god_mode(self) -> bool:
        """Toggle player invincibility."""
        if self.is_enabled:
            self.god_mode = not self.god_mode
        return self.god_mode

    def toggle_freeze(self) -> bool:
        """Toggle ghost movement freeze."""
        if self.is_enabled:
            self.ghosts_frozen = not self.ghosts_frozen
        return self.ghosts_frozen

    def toggle_speed(self, player_ctrl: PlayerController) -> bool:
        """Toggle player speed between normal and double turbo pace."""
        if not self.is_enabled:
            return False

        if self.base_speed is None:
            self.base_speed = player_ctrl.speed

        self.speed_boost = not self.speed_boost
        if self.speed_boost:
            player_ctrl.speed = self.base_speed * 2
        else:
            player_ctrl.speed = self.base_speed

        return self.speed_boost

    def add_life(self, game_state: GameState) -> int:
        """Award player an extra life."""
        if self.is_enabled:
            game_state.lives += 1
        return game_state.lives

    def handle_mouse_click(
        self,
        pos: Tuple[int, int],
        player_ctrl: PlayerController,
        game_state: GameState,
    ) -> bool:
        """Process mouse clicks on pause screen cheat button and items."""
        if not self.is_enabled:
            return False

        mx, my = pos
        if not self.menu_open:
            if self.btn_rect.collidepoint(mx, my):
                self.menu_open = True
            return False

        start_y = 380
        opt_height = 50
        opts = ["god", "freeze", "speed", "life", "skip", "close"]

        for idx, opt in enumerate(opts):
            r = pygame.Rect(710, start_y + idx * opt_height, 500, 45)
            if r.collidepoint(mx, my):
                if opt == "god":
                    self.toggle_god_mode()
                elif opt == "freeze":
                    self.toggle_freeze()
                elif opt == "speed":
                    self.toggle_speed(player_ctrl)
                elif opt == "life":
                    self.add_life(game_state)
                elif opt == "skip":
                    return True
                elif opt == "close":
                    self.menu_open = False
                break

        return False

    def handle_cheat_keys(
        self,
        event: pygame.event.Event,
        player_ctrl: PlayerController,
        game_state: GameState,
    ) -> bool:
        """Handle developer evaluation keyboard shortcuts."""
        if not self.is_enabled or event.type != pygame.KEYDOWN:
            return False

        if event.key == pygame.K_g:
            self.toggle_god_mode()
        elif event.key == pygame.K_f:
            self.toggle_freeze()
        elif event.key == pygame.K_b:
            self.toggle_speed(player_ctrl)
        elif event.key == pygame.K_h:
            self.add_life(game_state)
        elif event.key == pygame.K_l:
            return True

        return False

    def render_pause_overlay(
        self,
        surface: pygame.Surface,
        font_title: pygame.font.Font,
        font_body: pygame.font.Font,
    ) -> None:
        """Draw Pause Screen and optional Cheat Mode UI button."""
        frame_rect = pygame.Rect(200, 60, 1520, 960)
        pygame.draw.rect(
            surface, (230, 115, 115), frame_rect, width=4, border_radius=30
        )

        title_surf = font_title.render("Game Paused", True, (240, 120, 120))
        tx = (surface.get_width() - title_surf.get_width()) // 2
        surface.blit(title_surf, (tx, 260))

        if not self.is_enabled:
            return

        if not self.menu_open:
            bx, by, bw, bh = self.btn_rect
            btn_surf = pygame.Surface((bw, bh))
            btn_surf.fill((215, 218, 222))
            surface.blit(btn_surf, (bx, by))

            pygame.draw.rect(
                surface,
                (240, 120, 120),
                self.btn_rect,
                width=3,
                border_radius=16,
            )

            text_surf = font_body.render(
                "Cheat Mode Settings", True, Rgb.BLACK
            )
            sx = bx + (bw - text_surf.get_width()) // 2
            sy = by + (bh - text_surf.get_height()) // 2
            surface.blit(text_surf, (sx, sy))
        else:
            self._render_settings_list(surface, font_body)

    def _render_settings_list(
        self, surface: pygame.Surface, font_body: pygame.font.Font
    ) -> None:
        """Draw interactive cheat toggles list when button is clicked."""
        items: List[Tuple[str, str, Tuple[int, int, int]]] = [
            (
                "1. God Mode",
                "ON" if self.god_mode else "OFF",
                Rgb.GREEN if self.god_mode else Rgb.RED,
            ),
            (
                "2. Freeze Ghosts",
                "ON" if self.ghosts_frozen else "OFF",
                Rgb.GREEN if self.ghosts_frozen else Rgb.RED,
            ),
            (
                "3. Speed Boost (2x)",
                "ON" if self.speed_boost else "OFF",
                Rgb.GREEN if self.speed_boost else Rgb.RED,
            ),
            ("4. Add Extra Life", "+1", Rgb.YELLOW),
            ("5. Skip Level", "WIN", Rgb.YELLOW),
            ("Back to Pause", "CLOSE", Rgb.WHITE),
        ]

        start_y: int = 380
        for idx, (label, state_str, col) in enumerate(items):
            box_r = pygame.Rect(710, start_y + idx * 50, 500, 45)
            pygame.draw.rect(
                surface, (30, 32, 40), box_r, border_radius=8
            )
            pygame.draw.rect(
                surface, (70, 75, 95), box_r, width=2, border_radius=8
            )

            txt = font_body.render(f"{label}: {state_str}", True, col)
            surface.blit(txt, (box_r.x + 20, box_r.y + 8))
