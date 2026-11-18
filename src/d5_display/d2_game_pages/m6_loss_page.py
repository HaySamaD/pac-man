"""Renders the game over (loss) screen."""

from typing import Tuple

from pygame import font
from pygame.surface import Surface

from ...d1_helpers import Rgb
from .. import Printer


class LossPage:
    """
        Handles rendering game over title and name entry prompt.

        Attributes:
            width (int): Screen width.
            height (int): Screen height.
            title_font (font.Font): Title font object.
            content_font (font.Font): Content font object.
            screen (Surface): Pygame display surface.
            p (Printer): Printer utility instance.
    """
    def __init__(
                    self,
                    screen: Surface,
                    title_font: font.Font,
                    content_font: font.Font,
                    resolution: Tuple[int, int]
                ) -> None:
        """
            Initializes loss page layout.

            Args:
                screen (Surface): Target display surface.
                title_font (font.Font): Title font object.
                content_font (font.Font): Content font object.
                resolution (Tuple[int, int]): Screen resolution.
        """
        # ------------------- init params --------------------
        self.width, self.height = resolution
        self.title_font: font.Font = title_font
        self.content_font: font.Font = content_font
        self.screen = screen
        # ----------------------------------------------------
        self.p: Printer = Printer(
                                    self.screen,
                                    self.title_font,
                                    self.content_font,
                                    (self.width, self.height)
                                 )

    # ===================================================================
    def print_loss_page(self) -> None:
        """Renders game over title and name input instructions."""
        # ---------------------------------------------------------------
        self.p.print_title("Game Over: Try again", Rgb.ORANGE, Rgb.BLACK)
        # ---------------------------------------------------------------
        y: int | float = self.height * 0.17
        # ---------------------------------------------------------------
        self.p.print_text(
                            "Enter your name below to save your score",
                            (-99, y),
                            Rgb.WHITE,
                            Rgb.BLACK,
                            center_text=True
                         )
        # ---------------------------------------------------------------
        return None
