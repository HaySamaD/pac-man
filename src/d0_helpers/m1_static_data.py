from typing import List


# use this data if we have a wrong config file (file not found or acces denied)
DEFAULT_CONFIG_FILE = {

                "highscore_filename": "highscores.json",

                "levels_data": [
                                    {"width": 42, "height": 42, "pacgum": 42}
                                    for _ in range(10)
                               ],

                "lives": 3,

                "points_per_pacgum": 10,

                "points_per_super_pacgum": 20,

                "points_per_ghost": 40,

                "seed": 42,

                "level_max_time": 300

                    }

# ------------------------- the main menu options --------------------------
MENU: List[str] = ["Start Game", "View Highscores", "Instructions", "Exit"]

# -------------------------- the instructions content -------------------------
INSTRUCTIONS: List[str] = [

        "CONTROLS & GAME INSTRUCTIONS:",

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

        "4. Pause & Navigation:",

        " - Press ESC to pause the game at any time.",

        " - Use the Main Menu to view Top 10 Highscores, read instructions, or"
        " exit."

                            ]

# ------ the pause options ------
PAUSE = ["Resume", "Go to menu"]
