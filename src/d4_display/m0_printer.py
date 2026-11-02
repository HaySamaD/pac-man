"""
    Provides utility functions to render titles and formatted text onto the
                                                                Pygame surface.
"""

from pygame import font

from typing import Tuple, Any


class Printer:
    """
        Handles drawing titles and text strings on the display screen.

        Attributes:
            screen (Any): Pygame display surface.
            title_font (font.Font): Font used for titles.
            text_font (font.Font): Font used for regular text.
            width (int): Screen width resolution.
            height (int): Screen height resolution.
    """
    def __init__(
                    self,
                    screen: Any,
                    title_font: font.Font,
                    text_font: font.Font,
                    resolution: Tuple[int, int]
                ) -> None:
        """
            Initializes printer with display surface, fonts, and resolution.

            Args:
                screen (Any): Target Pygame surface.
                title_font (font.Font): Font for rendering titles.
                text_font (font.Font): Font for rendering normal text.
                resolution (Tuple[int, int]): Screen width and height.
        """

        # ------------- init params ----------------
        self.screen: Any = screen
        self.title_font: font.Font = title_font
        self.text_font: font.Font = text_font
        self.width, self.height = resolution

    # ============================= Draw a title ==============================
    def print_title(
                        self,
                        content: str,
                        color: Tuple[int, int, int],
                        background: Tuple[int, int, int]
                   ) -> None:
        """
            Renders and centers a title string at the top of the screen.

            Args:
                content (str): Title text content.
                color (Tuple[int, int, int]): RGB color for the text.
                background (Tuple[int, int, int]): RGB color for the
                                                                    background.
        """
        # ----------------------- create a text object ------------------------
        text = self.title_font.render(
                                        content,
                                        True,
                                        color,
                                        background
                                     )
        # ----------------------- for central the title -----------------------
        x: int | float = (self.width - text.get_width()) / 2
        y: int | float = self.height * 0.05
        # -------------------------- display the test -------------------------
        self.screen.blit(text, (x, y))
        # ---------------------------------------------------------------------
        return None

    # ========================== draw a normal text ===========================
    def print_text(
                    self,
                    content: str,
                    coord: Tuple[float, float],
                    color: Tuple[int, int, int],
                    background: Tuple[int, int, int],
                    center_text: bool
                  ) -> None:
        """
            Renders a text string at given coordinates with optional centering.

            Args:
                content (str): Text content to render.
                coord (Tuple[float, float]): (x, y) coordinates for placement.
                color (Tuple[int, int, int]): RGB text color.
                background (Tuple[int, int, int]): RGB background color.
                center_text (bool): Flag to center text horizontally.
        """
        # ---------------------------------------------------------------------
        x, y = coord
        # -------------------- create a text object ---------------------
        text = self.text_font.render(content, True, color, background)
        # ---------------------------------------------------------------------
        if center_text:
            x = (self.width - text.get_width()) / 2
        # ------------------------- display the test --------------------------
        self.screen.blit(text, (x, y))
        # ---------------------------------------------------------------------
        return None
