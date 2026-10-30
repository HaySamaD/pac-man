from typing import Tuple

from pygame import font

from ..d0_helpers import Rgb
from ..d0_helpers import INSTRUCTIONS
from ..d4_display import Printer


class InstructionsPage:
    def __init__(
                    self,
                    screen,
                    title_font,
                    content_font,
                    resolution: Tuple[int, int] = (1920, 1080)
                ) -> None:
        # ------------------- init params -------------------
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
        # ---------------------------------------------------
        self.pos: int = 0

    # =========================================================================
    def print_instruction_page(self) -> None:
        # -------------- fill the screen first before printing ----------------
        self.screen.fill(Rgb.BLACK)
        # ---------------------------------------------------------------------
        self.p.print_title("Instructions", Rgb.RED, Rgb.BLACK)
        # ---------------------------------------------------------------------
        x: int | float = self.width * 0.05
        y: int | float = self.height * 0.15
        # ---------------------------------------------------------------------
        for i in INSTRUCTIONS:
            if i.startswith(("1", "2", "3", "4")):
                y += self.height * 0.08
            elif i.startswith(" -"):
                y += self.height * 0.028
            else:
                y += self.height * 0.0128
            self.p.print_text(i, (x, y), Rgb.WHITE, Rgb.BLACK, False)

        # ------------------ print the 'previous' boutton ---------------------
        color: Tuple[int, int, int] = Rgb.GREEN if self.pos == 1 else Rgb.WHITE
        # ---------------------------------------------------------------------
        self.p.print_text(
                            "previous",
                            (self.width * 0.8, self.height * 0.8),
                            color,
                            Rgb.BLACK, False
                         )
