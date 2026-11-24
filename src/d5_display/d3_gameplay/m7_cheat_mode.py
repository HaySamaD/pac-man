"""Minimal keyboard-only cheat mode controller for evaluation."""

import pygame


class CheatController:
    """Manages cheat mode, invincibility, speed boost, and level skip."""

    def __init__(self) -> None:
        """Initialize cheat flags to disabled state."""
        self.is_enabled: bool = False
        self.invinc_mode: bool = False
        self.speed_mult: int = 2

    def handle_key(self, key: int) -> bool:
        """Process cheat keys; return True if level skip is triggered."""
        if key == pygame.K_c:
            self.is_enabled = not self.is_enabled
            if not self.is_enabled:
                self.invinc_mode = False
                self.speed_mult = 1
        elif self.is_enabled and key == pygame.K_i:
            self.invinc_mode = not self.invinc_mode
        elif self.is_enabled and key == pygame.K_PERIOD:
            self.speed_mult = min(4, self.speed_mult * 2)
        elif self.is_enabled and key == pygame.K_COMMA:
            self.speed_mult = max(1, self.speed_mult // 2)
        elif self.is_enabled and key == pygame.K_n:
            return True
        return False
