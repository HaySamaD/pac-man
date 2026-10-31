from typing import Tuple

from pygame import font
from pygame.surface import Surface

from ..d0_helpers import Rgb
from . import Printer


class LossPage:
    def __init__(
                    self,
                    screen: Surface,
                    title_font: font.Font,
                    content_font: font.Font,
                    resolution: Tuple[int, int]
                ) -> None:
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
    def print_game_over_page(self) -> None:
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
