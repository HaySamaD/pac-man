import pygame
from typing import Tuple, List, Dict
from .m2_highscores_system import HighScoreSys


class MainMenu:

    def __init__(
                    self,
                    top_10_scores: HighScoreSys,
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
        self.options_font = pygame.font.Font(None, 50)

        # --------------- composantes of main menu (hors title) ---------------
        self.options: List[str] = [
                        "Start Game", "View Highscores", "Instructions", "Exit"
                                  ]
        self.selected: int = 0

        # running flag
        self.running: bool = True

    # ---------------- draw the title in the main menu ------------------
    def draw_title(self) -> None:

        text = self.title_font.render("Pac-Man", True, "yellow", "black")

        # for central the title
        x_text: int = (self.width - text.get_width()) / 2

        self.screen.blit(text, (x_text, 100))

    # -----------------------------------------------------------------------
    def draw_options(self) -> None:

        line_separator: int = 300

        for i, option in enumerate(self.options):

            color: str = "green" if i == self.selected else "white"

            text = self.options_font.render(option, True, color, "black")

            x_text: int = (self.width - text.get_width()) / 2
            y_text: int = line_separator

            self.screen.blit(text, (x_text, y_text))

            line_separator += 100

    # ----------------------------------------
    def run(self):

        while self.running:

            # <=> mlx_key_hook()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:

                    if event.key in [pygame.K_DOWN, pygame.K_s]:

                        if self.selected == 3:
                            self.selected = 0

                        else:
                            self.selected += 1

                    elif event.key in [pygame.K_UP, pygame.K_w]:

                        if self.selected == 0:
                            self.selected = 3

                        else:
                            self.selected -= 1

                    elif event.key in [pygame.K_KP_ENTER, pygame.K_RETURN]:

                        selected_option: str = self.options[self.selected]

                        if selected_option == "Exit":
                            self.running = False

            self.screen.fill("black")

            self.draw_title()
            self.draw_options()

            self.clock.tick(60)
            # refrech of FPS
            pygame.display.flip()

        pygame.quit()
