*This project has been created as part of the 42 curriculum by [ybajdou, aryahi].*

# Pac-Man (Python Pygame Implementation)

## Description

This project is a Python recreation of the classic arcade game **Pac-Man** using **Pygame**. This documentation covers the core system, configuration parser, highscore manager, and user interface developed by **ybajdou**.

## Instructions

### Prerequisites

* Python 3.10 or higher
* Pygame library
* Pydantic library
* Pyinstaller library

### Installation & Execution

You can use the `Makefile` to manage the project easily:

* **Install dependencies:**
  ```bash
  make install
  ```

* **Run the game:**
  ```bash
  python3 pac-man.py config.json
  # Or use:
  make run
  ```

* **Run code checks (flake8 and mypy):**
  ```bash
  make lint
  ```

* **Clean temporary files:**
  ```bash
  make clean
  ```

---

## Configuration File Structure

The game reads a custom JSON configuration file passed as a command-line argument. 

### Features of the Parser:
* **Comment Support:** Any line starting with `#` is ignored.
* **Safety & Defaults:** If any key is missing or has an invalid value, the program does not crash. It automatically uses safe default values and prints a clear warning message.

### Accepted Configuration Keys and Values:

1. `highscore_file` (String):
   * **Description:** The name of the JSON file where highscores are saved.
   * **Accepted Values:** Any valid filename ending with `.json` (e.g., `"highscores.json"`).
   * **Default:** `"highscores.json"`

2. `levels_data` (List of Levels):
   * **Description:** Defines the settings for each game level (at least 10 levels required).
   * **Object Keys:**
     * `width` (Integer): Width of the maze. Must be between `14` and `48`. (Default: `42`)
     * `height` (Integer): Height of the maze. Must be between `10` and `24`. (Default: `42`)
     * `pacgum` (Integer): Number of small dots. Must be between `1` and the maximum map capacity. (Default: `42`)

3. `lives` (Integer):
   * **Description:** Number of lives the player starts with.
   * **Accepted Values:** Integer $\ge 1$.
   * **Default:** `3`

4. `pacgum_points` (Integer):
   * **Description:** Points earned when eating a normal pacgum.
   * **Accepted Values:** Integer $\ge 1$.
   * **Default:** `10`

5. `super_pacgum_points` (Integer):
   * **Description:** Points earned when eating a super-pacgum (power pellet).
   * **Accepted Values:** Integer $\ge 1$.
   * **Default:** `50`

6. `ghost_points` (Integer):
   * **Description:** Points earned when eating an edible ghost.
   * **Accepted Values:** Integer $\ge 1$.
   * **Default:** `200`

7. `seed` (Integer):
   * **Description:** Random seed used for maze generation on the first level.
   * **Accepted Values:** Integer $\ge 1$.
   * **Default:** `42`

8. `level_max_time` (Integer):
   * **Description:** Time limit in seconds for each level.
   * **Accepted Values:** Integer $\ge 1$.
   * **Default:** `90`

### Example of Custom `config.json`:
```json
{
  "highscore_file": "highscores.json",
  "levels_data": [
                    {"width": 20, "height": 20, "pacgum": 42},
                    {"width": 20, "height": 20, "pacgum": 42},
                    {"width": 20, "height": 20, "pacgum": 42},
                    {"width": 20, "height": 20, "pacgum": 42},
                    {"width": 20, "height": 20, "pacgum": 42},
                    {"width": 20, "height": 20, "pacgum": 42},
                    {"width": 20, "height": 20, "pacgum": 42},
                    {"width": 20, "height": 20, "pacgum": 42},
                    {"width": 20, "height": 20, "pacgum": 42},
                    {"width": 20, "height": 20, "pacgum": 42}
                 ],
  "lives": 3,
  "pacgum_points": 10,
  "super_pacgum_points": 50,
  "ghost_points": 200,
  "seed": 42,
  "level_max_time": 90
}
```

---

## Highscore System Structure

The highscore system saves player results permanently in a JSON file.

### Structure of `highscores.json`:
The file stores a list of player objects. Each object contains:
* `name` (String): The player's name.
  * **Rules:** Maximum 10 characters long. Only letters, numbers, and spaces are allowed (`isalnum()` or `isspace()`). If invalid, it defaults to `"Player"`.
* `score` (Integer): The final score achieved.
  * **Rules:** Must be a non-negative integer ($\ge 0$).

### How It Works:
1. **Loading:** Highscores are loaded automatically when the game starts.
2. **Ranking:** The system automatically sorts all scores from highest to lowest and keeps only the **Top 10** scores.
3. **Saving:** When a game ends (Win or Loss), the player types their name, and the updated list is instantly saved back to the JSON file.

### Example of `highscores.json`:
```json
[
  {
    "name": "Player1",
    "score": 1500
  },
  {
    "name": "Player2",
    "score": 1200
  }
]
```

---

## Software Architecture (ybajdou Implementation)

The code is organized into clear packages:

* `d1_helpers`: Colors (`Rgb`, `Color`), static menus, instructions text, and safe file reading utilities.
* `d2_classes`: Pydantic validation models (`Config`, `Level`, `NameScore`) and dataclasses (`GameState`, `Player`, `Ghost`, `Position`).
* `d3_parsing_config_file`: Parses custom JSON config files and handles errors safely.
* `d4_parsing_highscores`: Reads and saves the Top 10 high scores in a JSON file.

* `d5_display`: UI rendering engine (`Printer`) for Main Menu, Highscores page, Instructions page, HUD, Pause, Win, Loss, and the gameplay screens.
* `d6_game_loop`: Handles keyboard events and game state transitions.

---

## Project Management

You can view the project timeline, task breakdown, and others in the [Project Management Document](./project_management).

---

## Resources & AI Usage

### References & Links
* [Game Loop](https://www.pygame.fr/en/bb-01-game-loop/)
* [Display Text](https://gamedevacademy.org/display-text-pygame-tutorial-complete-guide/)
* [FPS Tutorial](https://gamedevacademy.org/pygame-fps-tutorial/)
* [Get the size of any screen](https://bugnet.io/blog/fix-pygame-fullscreen-resolution-wrong-size)
* [Load a image in pygame](https://gamedevacademy.org/pygame-image-load-tutorial-complete-guide/)
* [Resizing a image using pillow (PIL)](https://dev.to/mary_kariuki_944435052aa9/how-to-resize-an-image-in-python-using-pil-pillow-5hmj)

### AI Usage Disclosure
Throughout the development of this project, the AI was used exclusively as a supporting tool to better understand the general project requirements and architecture, as well as to generate custom test cases for verifying and testing the codebase's functionality.