"""Renders the in-game Heads-Up Display (HUD)."""

from typing import Tuple

from pygame import font
from pygame.surface import Surface

from ...d1_helpers import Rgb
from ...d2_classes import GameState
from .. import Printer


class HUD:
    """
        Handles displaying active game statistics during gameplay.

        Attributes:
            game_state (GameState): Current game state object.
            width (int): Screen width.
            height (int): Screen height.
            screen (Surface): Pygame display surface.
            title_font (font.Font): Title font object.
            content_font (font.Font): Content font object.
            p (Printer): Printer utility instance.
    """
    def __init__(
                    self,
                    game_state: GameState,
                    screen: Surface,
                    title_font: font.Font,
                    content_font: font.Font,
                    p: Printer,
                    resolution: Tuple[int, int],
                ) -> None:
        """
            Initializes HUD with game state reference and display settings.

            Args:
                game_state (GameState): Game state instance.
                screen (Surface): Target display surface.
                title_font (font.Font): Title font object.
                content_font (font.Font): Content font object.
                resolution (Tuple[int, int]): Screen resolution.
        """

        # ------------------- init params -------------------
        self.game_state: GameState = game_state
        self.screen = screen
        self.title_font: font.Font = title_font
        self.content_font: font.Font = content_font
        self.p: Printer = p
        self.width, self.height = resolution

    # ==================================================================
    def print_hud(self) -> None:
        """Renders score, lives, level, and remaining time on screen."""
        # --------------------------------------------------------------
        score: int = self.game_state.score
        lives: int = self.game_state.lives
        level: int = self.game_state.level
        time_left: int = self.game_state.time_left
        # --------------------------------------------------------------
        x: int | float = self.width * 0.20
        y: int | float = self.height * 0.025
        # --------------------------------------------------------------
        self.p.print_text(
                            (
                                f"Score: {score}                      "
                                f"Lives: {lives}                      "
                                f"Level: {level}                      "
                                f"Time left: {time_left}"
                            ),
                            (x, y),
                            Rgb.WHITE,
                            Rgb.BLACK,
                            False
                         )
        # --------------------------------------------------------------
        return None
