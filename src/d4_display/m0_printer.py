from pygame import font

from typing import Tuple, Any


class Printer:
    def __init__(
                    self,
                    screen: Any,
                    title_font: font.Font,
                    text_font: font.Font,
                    resolution: Tuple[int, int]
                ) -> None:

        # ------------- init params ----------------
        self.screen: Any = screen
        self.title_font: font.Font = title_font
        self.text_font: font.Font = text_font
        self.width, self.height = resolution

    # ===================== Draw a title ====================
    def print_title(
                        self,
                        content: str,
                        color: Tuple[int, int, int],
                        background: Tuple[int, int, int]
                   ) -> None:
        # -------------- create a text object ---------------
        text = self.title_font.render(
                                        content,
                                        True,
                                        color,
                                        background
                                     )
        # ------------- for central the title ---------------
        x: int | float = (self.width - text.get_width()) / 2
        y: int | float = self.height * 0.05
        # ---------------- display the test -----------------
        self.screen.blit(text, (x, y))
        # ---------------------------------------------------
        return None

    # ======================= draw a normal text ========================
    def print_text(
                    self,
                    content: str,
                    coord: Tuple[float, float],
                    color: Tuple[int, int, int],
                    background: Tuple[int, int, int],
                    center_text: bool
                  ) -> None:
        # ---------------------------------------------------------------
        x, y = coord
        # -------------------- create a text object ---------------------
        text = self.text_font.render(content, True, color, background)
        # ---------------------------------------------------------------
        if center_text:
            x = (self.width - text.get_width()) / 2
        # ---------------------- display the test -----------------------
        self.screen.blit(text, (x, y))
        # ---------------------------------------------------------------
        return None
