"""Renders the victory congratulation screen."""

from typing import Tuple

from pygame import font
from pygame.surface import Surface

from ...d1_helpers import Rgb
from ...d2_classes import GameState
from .. import Printer


class WinPage:
    """
        Handles rendering victory title and score saving prompt.

        Attributes:
            screen (Surface): Pygame display surface.
            title_font (font.Font): Title font object.
            content_font (font.Font): Content font object.
            width (int): Screen width.
            height (int): Screen height.
            p (Printer): Printer utility instance.
    """
    def __init__(
                    self,
                    screen: Surface,
                    title_font: font.Font,
                    content_font: font.Font,
                    game_state: GameState,
                    p: Printer,
                    resolution: Tuple[int, int]
                ) -> None:
        """
            Initializes win page layout.

            Args:
                screen (Surface): Target display surface.
                title_font (font.Font): Title font object.
                content_font (font.Font): Content font object.
                resolution (Tuple[int, int]): Screen resolution.
        """

        # ------------------- init params --------------------
        self.screen: Surface = screen
        self.title_font: font.Font = title_font
        self.content_font: font.Font = content_font
        self.game_state: GameState = game_state
        self.p: Printer = p
        self.width, self.height = resolution

    # ======================================================================
    def print_win_page(self) -> None:
        """Renders victory congratulation title and name entry prompt."""
        # ------------------------------------------------------------------
        self.p.print_title("Congratulations: You Win", Rgb.GREEN, Rgb.BLACK)
        self.p.print_text(
                            f"Your score is: {self.game_state.score}",
                            (-99, self.height * 0.25),
                            Rgb.WHITE,
                            Rgb.BLACK,
                            center_text=True
                         )
        # ------------------------------------------------------------------
        x: int | float = -99
        y: int | float = self.height * 0.17
        # ------------------------------------------------------------------
        self.p.print_text(
                            "Enter your name below to save your score",
                            (x, y),
                            Rgb.WHITE,
                            Rgb.BLACK,
                            center_text=True
                         )
        # ------------------------------------------------------------------
        return None
