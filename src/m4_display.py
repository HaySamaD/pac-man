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

        # -------------------- init the font of the text ----------------------
        self.title_font = pygame.font.Font(None, 135)
        self.options_font = pygame.font.Font(None, 50)

        # --------------------------- menu elements ---------------------------
        self.options: List[str] = [
                        "Start Game", "View Highscores", "Instructions", "Exit"
                                  ]
        self.selected: int = 0

        # ----- running flag -----
        self.running: bool = True

    # ---------------- draw the title in the main menu ------------------
    def draw_title(self):
        text = self.title_font.render("Pac-Man", True, "yellow", "black")
        self.screen.blit(text, (self.width / 2.46, self.height / 15))

    # --------------------------------------
    def draw_options(self):

        start_game = self.options_font.render("Start Game", True, "white", "black")
        self.screen.blit(start_game, (self.width/2.2, self.height/4))

        view_highscores = self.options_font.render("View Highscores", True, "white", "black")
        self.screen.blit(view_highscores, (self.width/2.3, self.height/3))

        instructions = self.options_font.render("Instructions", True, "white", "black")
        self.screen.blit(instructions, (self.width/2.23, self.height/2.35))

        exit = self.options_font.render("Exit", True, "white", "black")
        self.screen.blit(exit, (self.width/2.07, self.height/1.95))

    # ----------------------------------------
    def run(self):

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("black")

            self.draw_title()
            self.draw_options()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
