import pygame
from pygame import Surface, font

from typing import Tuple, List

from .m0_helpers import Rgb


# ======================== STATIC ELEMNTS OF SCREEN ========================

MENU: List[str] = ["Start Game", "View Highscores", "Instructions", "Exit"]

INSTRUCTIONS: List[str] = [

        "CONTROLS & GAME INSTRUCTIONS",

        "1. Player Movement:",

        " - Use ARROW KEYS or WASD to move Pac-Man through the corridors.",

        " - Pac-Man can only move through open corridors, not through walls.",

        "2. Objectives:",

        " - Eat all Pacgums (small dots) scattered across the corridors to win"
        " the current level.",

        " - Avoid ghosts. Touching a ghost causes Pac-Man to lose a life and"
        " restart in the middle.",

        " - The game ends when all lives are lost or all 10 levels are"
        " completed.",

        "3. Power Pellets (Super-Pacgums):",

        " - Located in the 4 corners of the maze.",

        " - Eating a super-pacgum grants points and makes ghosts edible for a"
        " short time.",

        " - Eating edible ghosts awards extra points.",

        "4. Scoring:",

        " - Pacgum: +10 points",

        " - Super-Pacgum: +50 points",

        " - Ghost: +200 points",

        "5. Pause & Navigation:"

        " - Press ESC to pause the game at any time."

        " - Use the Main Menu to view Top 10 Highscores, read instructions, or"
        " exit."

                            ]


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


# ========================= THE MAIN MENU CLASS =========================

class MainMenu:

    def __init__(
                    self, resolution: Tuple[int, int] = (1920, 1080)
                ) -> None:

        # -------------------- init params ----------------------
        self.width, self.height = resolution

        # ------------------ init pygame elements ------------------
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # ---------------- init fonts of text --------------------
        self.title_font: font.Font = pygame.font.Font(None, 135)
        self.content_font: font.Font = pygame.font.Font(None, 50)

        # --------------------- the printer class --------------------
        self.printer: Printer = Printer(
                                            self.screen,
                                            self.title_font,
                                            self.content_font,
                                            (self.width, self.height)
                                       )

        # -- the selected option now is 'Start Game'
        # (for lopping for each elements of MENU) --
        self.pos: int = 0

    # ------------------------------------------------------

    def print_main_menu(self) -> None:

        # fill the screen first before printing
        self.screen.fill(Rgb.BLACK)

        self.printer.print_title("Pac-man", Rgb.YELLOW, Rgb.BLACK)

        x: int = -99
        y: int = self.height * 0.25
        for pos, option_content in enumerate(MENU):

            color: Tuple[int] = Rgb.GREEN if pos == self.pos else Rgb.WHITE

            self.printer.print_text(
                                option_content, (x, y), color, Rgb.BLACK, True
                                   )

            y += self.height * 0.1

        return None

    # -------------------------------------------------------------
    def run(self):

        running: bool = True

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                self.print_main_menu()

            self.clock.tick(60)
            # refrech of FPS
            pygame.display.flip()

        pygame.quit()
