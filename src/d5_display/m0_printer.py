from pygame import Surface, font

from typing import Tuple


class Printer:
    def __init__(
                    self,
                    screen: Surface,
                    title_font: font.Font,
                    content_font: font.Font,
                    resolution: Tuple[int, int] = (1920, 1080)
                ) -> None:

        # ------------- init params ----------------
        self.screen: Surface = screen
        self.title_font: font.Font = title_font
        self.content_font: font.Font = content_font
        self.width, self.height = resolution

    # ------------------- draw the title of the page -------------------
    def print_title(
                        self,
                        content: str,
                        color: Tuple[int],
                        background: Tuple[int]
                   ) -> None:

        text = self.title_font.render(content, True, color, background)

        # for central the title
        x: int = (self.width - text.get_width()) / 2
        y: int = self.height * 0.05

        self.screen.blit(text, (x, y))

        return None

    # ------------------------------------------------------------------
    def print_text(
                    self,
                    content: str,
                    coord: Tuple[int, int],
                    color: Tuple[int],
                    background: Tuple[int],
                    center_text: bool
                  ) -> None:

        x, y = coord

        text: Surface = self.content_font.render(
                                            content, True, color, background
                                                )

        if center_text:
            x = (self.width - text.get_width()) / 2

        self.screen.blit(text, (x, y))
