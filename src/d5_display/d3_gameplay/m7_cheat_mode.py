"""Minimal keyboard-only cheat mode controller for evaluation."""

import pygame


class CheatController:
    """Manages cheat mode activation, god mode, and level skipping."""

    def __init__(self) -> None:
        """Initialize cheat flags to disabled state."""
        self.is_enabled: bool = False
        self.god_mode: bool = False

    def handle_key(self, key: int) -> bool:
        """Process cheat keys; return True if level skip is triggered."""
        if key == pygame.K_c:
            self.is_enabled = not self.is_enabled
            if not self.is_enabled:
                self.god_mode = False
            return False

        if not self.is_enabled:
            return False

        if key == pygame.K_g:
            self.god_mode = not self.god_mode
            return False

        if key == pygame.K_n:
            return True

        return False
