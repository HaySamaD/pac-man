"""Minimal keyboard-only cheat mode controller for evaluation."""

import pygame


class CheatController:
    """Manages cheat mode activation, god mode, and level skipping."""

    def __init__(self) -> None:
        """Initialize cheat flags to disabled state."""
        self.is_enabled: bool = False
        self.invinc_mode: bool = False

    def handle_key(self, key: int) -> bool:
        """Process cheat keys; return True if level skip is triggered."""
        if key == pygame.K_c:
            self.is_enabled = not self.is_enabled
            self.invinc_mode = self.invinc_mode and self.is_enabled
        elif self.is_enabled and key == pygame.K_i:
            self.invinc_mode = not self.invinc_mode
        elif self.is_enabled and key == pygame.K_n:
            return True
        return False
