"""Renders the highscores leaderboard screen."""

from typing import Tuple

from pygame.surface import Surface
from pygame import font

from ...d1_helpers import Rgb
from ...d4_parsing_highscores import HigherScore
from .. import Printer


class HighscoresPage:
    """
        Handles rendering top player scores and navigation buttons.

        Attributes:
            highscores (HigherScore): Highscore manager instance.
            screen (Surface): Pygame display surface.
            title_font (font.Font): Font for the page title.
            content_font (font.Font): Font for score entries.
            width (int): Screen width.
            height (int): Screen height.
            p (Printer): Printer utility instance.
            pos (int): Current selected navigation option.
    """
    def __init__(
                    self,
                    highscores: HigherScore,
                    screen: Surface,
                    title_font: font.Font,
                    content_font: font.Font,
                    resolution: Tuple[int, int] = (1920, 1080)
                ) -> None:
        """
            Initializes highscores page with data source and fonts.

            Args:
                highscores (HigherScore): Highscore records instance.
                screen (Surface): Target display surface.
                title_font (font.Font): Title font object.
                content_font (font.Font): Content font object.
                resolution (Tuple[int, int]): Screen resolution.
        """
        # ------------------- init params -------------------
        self.highscores: HigherScore = highscores
        self.screen = screen
        self.title_font: font.Font = title_font
        self.content_font: font.Font = content_font
        self.width, self.height = resolution
        # ---------------------------------------------------
        self.p: Printer = Printer(
                                    self.screen,
                                    self.title_font,
                                    self.content_font,
                                    (self.width, self.height)
                                 )
        # -- the selected option now is the highscores text -
        self.pos: int = 0

    # =========================================================================
    def print_highscores_page(self) -> None:
        """Renders the top 10 leaderboard list and previous button."""
        # ------------- fill the screen first before printing -----------------
        self.screen.fill(Rgb.BLACK)
        # ---------------------------------------------------------------------
        self.p.print_title("Highscores", Rgb.PINK, Rgb.BLACK)
        # ---------------------------------------------------------------------
        x: int | float = -99
        y: int | float = self.height * 0.20
        # ---------------------------------------------------------------------
        for i in self.highscores.top_10_scores:
            name: str = i.name
            score: int = i.score
            self.p.print_text(
                                f"{name} ----> {score}",
                                (x, y),
                                Rgb.WHITE, Rgb.BLACK, center_text=True
                             )
            y += self.height * 0.05
        # ------------------- print the 'previous' boutton --------------------
        color: Tuple[int, int, int] = Rgb.GREEN if self.pos == 1 else Rgb.WHITE
        # ---------------------------------------------------------------------
        self.p.print_text(
                            "previous",
                            (self.width * 0.8, self.height * 0.8),
                            color,
                            Rgb.BLACK, False
                         )
