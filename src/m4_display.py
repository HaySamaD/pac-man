import pygame
from typing import Tuple, List, Dict
from .m2_highscores_system import HighScoreSys


class MainMenu:

    def __init__(
                    self,
                    top_10_scores: HighScoreSys,
                    rules_lst: List[str],
                    screen_dim: Tuple[int, int] = (1920, 1080),
                ) -> None:

        # -------------------- init params ----------------------
        self.width, self.height = screen_dim
        self.top_10_scores: List[Dict[str, int]] = top_10_scores

        # ------- init pygame dependencises -------
        pygame.init()
        self.screen = pygame.display.set_mode(screen_dim)
        self.clock = pygame.time.Clock()

        # -------- init the font of the text ----------
        self.title_font = pygame.font.Font(None, 135)
        self.content_font = pygame.font.Font(None, 50)

        # --------------- composantes of main menu (hors title) ---------------
        self.options: Tuple[str] = (
                        "Start Game", "View Highscores", "Instructions", "Exit"
                                   )
        self.pos: int = 0

        # running flag
        self.running: bool = True

    # ---------------- draw the title in the main menu ------------------
    def print_title(self, content: str, color: str, background: str) -> None:

        text = self.title_font.render(content, True, color, background)
        # for central the title
        x: int = (self.width - text.get_width()) / 2
        y: int = self.height * 0.05
        self.screen.blit(text, (x, y))

    # ---------------------------------------------------------------------
    def print_text(
                    self,
                    content: str | Tuple[str] | List[str],
                    coord: Tuple[int, int] | None,
                    color: str | None,
                    background: str | None,
                 ) -> None:

        # --------------------- display a simple text ------------------------
        if isinstance(content, str):

            text = self.content_font.render(content, True, color, background)
            x, y = coord

            self.screen.blit(text, (x, y))

            return None

        # ------------------- display the menu elements ---------------------
        if isinstance(content, tuple):

            y = self.height * 0.22
            for i, option_str in enumerate(self.options):

                color = "green" if i == self.pos else "white"

                text = self.content_font.render(
                                            option_str, True, color, background
                                               )

                x = (self.width - text.get_width()) / 2

                self.screen.blit(text, (x, y))

                y += self.height * 0.05

            return None

        # ---------------- display the top 10 scores ------------------------
        if isinstance(content, List):

            y = self.height * 0.22
            for i in content:

                name: str = i.name
                score: int = i.score

                text = self.content_font.render(
                                f"{name} ---> {score}", True, "white", "black"
                                               )

                x: int = (self.width - text.get_width()) / 2

                self.screen.blit(text, (x, y))

                y += self.width * 0.035

    # -----------------------------------------------------------------------

    def print_menu_page(self):

        # print the title
        self.print_title("PAC-MAN", "yellow", "black")

        # print options
        # ("Start Game", "View Highscores", "Instructions", "Exit")
        self.print_text(self.options, None, None, None)

    # --------------------------------------------------------
    def print_highscores_page(self) -> None:

        self.print_title("Highscores", "yellow", "black")
        self.print_text(self.top_10_scores, None, None, None)

    # --------------------------------------------------------------------------
    def print_instructions(self) -> None:

        x: int = self.width * 0.22
        y: int = self.height * 0.22

        


    # -----------------------------------------------------
    def run(self):

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("black")
            self.print_instructions()

            self.clock.tick(60)
            # refrech of FPS
            pygame.display.flip()

        pygame.quit()
