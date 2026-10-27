from ..d4_display import (
                            Printer, MainMenuPage, HighscoresPage,
                            InstructionsPage, HUD, PauseMenuPage,
                            GameOverPage, WinPage
                         )
from ..d1_classes import GameState

from ..d3_parsing_highscores import HighScoreSys

import pygame

from typing import Tuple

from ..d0_helpers import Rgb


class GameLoop:
    def __init__(
                    self,
                    highscores_obj: HighScoreSys,
                    game_state: GameState,
                    final_level: int,
                    resolution: Tuple[int, int] = (1920, 1080)
                ) -> None:
        # ----------- init params -------------------------
        self.highscores_obj: HighScoreSys = highscores_obj
        self.game_state: GameState = game_state
        self.final_level = final_level
        self.width, self.height = resolution

    # --------------------------
    def game_loop(self) -> None:
        # ---------------------- init pygame ----------------------
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()
        # ------------- init fonts -------------
        title_font = pygame.font.Font(None, 135)
        content_font = pygame.font.Font(None, 50)
        # ----------------------------
        p: Printer = Printer(screen, title_font, content_font, (self.width, self.height))
        # -------------------------------------------------------------------
        menu_obj: MainMenuPage = MainMenuPage(
                                                screen,
                                                title_font,
                                                content_font,
                                                (self.width, self.height)
                                             )
        h_score_obj: HighscoresPage = HighscoresPage(
                                                        self.highscores_obj,
                                                        screen,
                                                        title_font,
                                                        content_font
                                                    )
        instruction_obj: InstructionsPage = InstructionsPage(
                                                    screen,
                                                    title_font,
                                                    content_font,
                                                    (self.width, self.height)
                                                            )
        hud_obj: HUD = HUD(
                            self.game_state,
                            screen,
                            title_font,
                            content_font,
                            (self.width, self.height)
                          )
        pause_obj: PauseMenuPage = PauseMenuPage(
                                                    screen,
                                                    title_font,
                                                    content_font,
                                                    (self.width, self.height)
                                                )
        gm_ovr_obj: GameOverPage = GameOverPage(
                                                    screen,
                                                    title_font,
                                                    content_font,
                                                    (self.width, self.height)
                                               )
        win_obj: WinPage = WinPage(
                                    screen,
                                    title_font,
                                    content_font,
                                    (self.width, self.height)
                                  )
        # ------------------------------------------------------------------
        running: bool = True
        player_name: str = ""
        while running:
            screen.fill(Rgb.BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_state.status == "MENU":
                        if event.key == pygame.K_DOWN:
                            menu_obj.pos += 1
                            if menu_obj.pos > 3:
                                menu_obj.pos = 0
                        elif event.key == pygame.K_UP:
                            menu_obj.pos -= 1
                            if menu_obj.pos < 0:
                                menu_obj.pos = 3
                        elif event.key == pygame.K_RETURN:
                            if menu_obj.pos == 0:
                                self.game_state.status = "PLAY"
                            elif menu_obj.pos == 1:
                                self.game_state.status = "HIGHSCORES"
                            elif menu_obj.pos == 2:
                                self.game_state.status = "INSTRUCTIONS"
                            elif menu_obj.pos == 3:
                                running = False
                    elif self.game_state.status == "HIGHSCORES":
                        if event.key == pygame.K_DOWN:
                            h_score_obj.pos += 1
                            if h_score_obj.pos > 1:
                                h_score_obj.pos = 0
                        elif event.key == pygame.K_UP:
                            h_score_obj.pos -= 1
                            if h_score_obj.pos < 0:
                                h_score_obj.pos = 1
                        elif event.key == pygame.K_RETURN:
                            if h_score_obj.pos == 1:
                                self.game_state.status = "MENU"
                    elif self.game_state.status == "INSTRUCTIONS":
                        if event.key == pygame.K_DOWN:
                            instruction_obj.pos += 1
                            if instruction_obj.pos > 1:
                                instruction_obj.pos = 0
                        elif event.key == pygame.K_UP:
                            instruction_obj.pos -= 1
                            if instruction_obj.pos < 0:
                                instruction_obj.pos = 1
                        elif event.key == pygame.K_RETURN:
                            if instruction_obj.pos == 1:
                                self.game_state.status = "MENU"
                    elif self.game_state.status == "PLAY":
                        if self.game_state.lives <= 0:
                            self.game_state.status = "LOSS"
                        elif self.game_state.time_left <= 0:
                            self.game_state.level -= 1
                        elif self.game_state.level > self.final_level:
                            self.game_state.status = "WIN"
                        elif event.type == pygame.K_ESCAPE:
                            self.game_state.status = "PAUSE"
                    elif self.game_state.status == "PAUSE":
                        if event.key == pygame.K_RETURN:
                            if pause_obj.pos == 0:
                                self.game_state.status == "PLAY"
                            elif pause_obj.pos == 1:
                                self.game_state.status == "MENU"
                    elif self.game_state.status in ["LOSS", "WIN"]:
                        if event.key == pygame.K_BACKSPACE:
                            screen.fill(Rgb.BLACK)
                            player_name = player_name[:-1]
                        elif event.key == pygame.K_RETURN:
                            name: str = player_name
                            scrore: int = self.game_state.score
                            self.highscores_obj.add_new_score(
                                                {"name": name, "score": scrore}
                                                             )
                            self.game_state.status = "MENU"
                        char: str = event.unicode
                        if (
                                (char.isalnum() or char.isspace())
                                and len(player_name) < 10
                           ):
                            player_name += char
                            self.highscores_obj.save_top_10_scores()

            if self.game_state.status == "MENU":
                menu_obj.print_main_menu()
            elif self.game_state.status == "HIGHSCORES":
                h_score_obj.print_highscores_page()
            elif self.game_state.status == "INSTRUCTIONS":
                instruction_obj.print_instruction_page()
            elif self.game_state.status == "PLAY":
                hud_obj.print_hud()
            elif self.game_state.status == "PAUSE":
                pause_obj.print_pause_page()
            elif self.game_state.status == "LOSS":
                gm_ovr_obj.print_game_over_page()
                p.print_text(
                                player_name,
                                (-99, self.height * 0.25),
                                Rgb.RED,
                                Rgb.BLACK,
                                True
                            )
            elif self.game_state.status == "WIN":
                win_obj.print_win_page()
                p.print_text(
                                player_name,
                                (-99, self.height * 0.25),
                                Rgb.GREEN,
                                Rgb.BLACK,
                                True
                            )

            clock.tick(60)
            pygame.display.flip()
        # ------------------------------------------------------------------
        pygame.quit()


"""
    links:
    - the game loop: https://www.pygame.fr/en/bb-01-game-loop/
    - using Font for text: https://www.geeksforgeeks.org/python/python-display-text-to-pygame-window/
    - using clock for FPS: https://gamedevacademy.org/pygame-fps-tutorial/
"""
