*This project has been created as part of the 42 curriculum by [ybajdou, aryahi].*

# Pac-Man (Python Pygame Implementation)

## Description

This project is a Python recreation of the classic arcade game **Pac-Man** using **Pygame**. It combines the core system, configuration parser, highscore manager, and UI developed by **ybajdou** with the gameplay engine, maze integration, BFS pathfinding, ghost AI, and MLX-style renderer developed by **aryahi**.

## Instructions

### Prerequisites

* Python 3.10 or higher
* Pygame library
* Pydantic library
* Pyinstaller library
* pillow library

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

1. `highscore_filename` (String):
   * **Description:** The name of the JSON file where highscores are saved.
   * **Accepted Values:** Any valid filename ending with `.json` (e.g., `"highscores.json"`).
   * **Default:** `"highscores.json"`

2. `levels_data` (List of Levels):
   * **Description:** Defines the settings for each game level (at least 10 levels required).
   * **Object Keys:**
     * `width` (Integer): Width of the maze. Must be between `14` and `46`. (Default: `46`)
     * `height` (Integer): Height of the maze. Must be between `10` and `22`. (Default: `42`)
     * `pacgum` (Integer): Number of small dots. Must be between `1` and the maximum map capacity. (Default: `42`)

3. `lives` (Integer):
   * **Description:** Number of lives the player starts with.
   * **Accepted Values:** Integer $\ge 1$.
   * **Default:** `3`

4. `points_per_pacgum` (Integer):
   * **Description:** Points earned when eating a normal pacgum.
   * **Accepted Values:** Integer $\ge 1$.
   * **Default:** `10`

5. `points_per_super_pacgum` (Integer):
   * **Description:** Points earned when eating a super-pacgum (power pellet).
   * **Accepted Values:** Integer $\ge 1$.
   * **Default:** `20`

6. `points_per_ghost` (Integer):
   * **Description:** Points earned when eating an edible ghost.
   * **Accepted Values:** Integer $\ge 1$.
   * **Default:** `40`

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
  "highscore_filename": "highscores.json",
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
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,
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

## General Software Architecture

The code is organized into clear packages:

* `d1_helpers`: Colors (`Rgb`, `Color`), static menus, instructions text, and safe file reading utilities.
* `d2_classes`: Pydantic validation models (`Config`, `Level`, `NameScore`) and dataclasses (`GameState`, `Player`, `Ghost`, `Position`).
* `d3_parsing_config_file`: Parses custom JSON config files and handles errors safely.
* `d4_parsing_highscores`: Reads and saves the Top 10 high scores in a JSON file.

* `d5_display`: UI rendering engine (`Printer`) for Main Menu, Highscores page, Instructions page, HUD, Pause, Win, Loss, and the gameplay screens.
* `d6_game_loop`: Handles keyboard events and game state transitions.

---

### Gameplay & Rendering Engine

Located inside `src/d5_display/d3_gameplay/`, the gameplay engine is built using clean OOP:

- `m1_maze_board.py` (`MazeBoard`): Integrates the external `mazegenerator` (`A-Maze-ing`) package, manages the 2D grid, handles 4-bit wall bitmasks (`1`, `2`, `4`, `8`, and `15` for the central `"42"` block), and places pacgums and corner super-pacgums.
- `m2_bfs.py` (`Bfs`): Implements Breadth-First Search (`get_distance_map`) to compute shortest corridor distances across the maze.
- `m3_movement.py` (`MovementController`): Base class handling smooth pixel-to-grid movement, intersection alignment, direction reversal, and wall collision checks.
- `m4_player.py` (`PlayerController`): Inherits from `MovementController` to handle keyboard input (`Arrow keys` / `WASD`), item consumption, and score updates.
- `m5_ghost.py` (`GhostController`): Inherits from `MovementController` to control autonomous ghost targeting, frightened fleeing, and respawn timers.
- `m6_renderer.py` (`Renderer`): Pre-bakes maze walls pixel-by-pixel onto a surface and renders collectibles, animated Pac-Man, and ghosts each frame.
- `m7_cheat_mode.py` (`CheatController`): Provides keyboard shortcuts to test invincibility and level progression during evaluation.
- `m8_gameplay.py` (`Gameplay`): Unified facade class connecting all gameplay modules with the main game loop, timers, lives, and collision detection.

---

## Gameplay Mechanics & Ghost AI

### Controls
- **Move Pac-Man:** `Arrow Keys` (`Up`, `Down`, `Left`, `Right`) or `W`, `A`, `S`, `D`.
- **Cheat Mode (Evaluation):**
  - `C`: Toggle Cheat Mode on/off.
  - `I`: Toggle Invincibility Mode (when Cheat Mode is active).
  - `N`: Skip immediately to the next level (when Cheat Mode is active).

### Ghost AI Behavior
All four ghosts navigate using **BFS shortest-path distance maps** without reversing direction at intersections, while slightly penalizing tiles occupied by other active ghosts to prevent stacking:
- **Blinky (Red):** Targets Pac-Man's exact current tile directly.
- **Pinky (Pink):** Targets 4 tiles ahead of Pac-Man's movement direction to block corridors.
- **Inky (Cyan):** Calculates a flanking target opposite to Blinky relative to 2 tiles ahead of Pac-Man (target of Inky = pos_player * 2 - red_pos).
- **Clyde (Orange):** Chases Pac-Man directly, but switches to fleeing when within 8 corridor cells (`BFS distance <= 8`).
- **Frightened & Eaten States:** Eating a super-pacgum turns ghosts edible (blue, flashing white before expiring) for 7 seconds (`420` frames at 60 FPS). When eaten, ghost eyes return to their home corner and freeze for 6 seconds (`360` frames) before respawning.

### Graphics Rendering (MLX-Equivalent Primitives)
To respect the project's graphical constraints, `Renderer` uses only Pygame operations that mirror the **MiniLibX (`mlx`)** library:
- **Pixel-by-Pixel Wall Baking:** Static background and maze walls are drawn once per level using `Surface.set_at()` (equivalent to `mlx_pixel_put`).
- **Sprite Blitting:** Collectibles, Pac-Man animation frames, and ghost sprites are drawn onto the screen using `Surface.blit()` (equivalent to `mlx_put_image_to_window`).

---

## Project Management

You can view the project timeline, task breakdown, and others in the [Project Management Document](./project_management).

---

## Resources & AI Usage

### References & Links

#### Core System & UI
* [Game Loop](https://www.pygame.fr/en/bb-01-game-loop/)
* [Display Text](https://gamedevacademy.org/display-text-pygame-tutorial-complete-guide/)
* [FPS Tutorial](https://gamedevacademy.org/pygame-fps-tutorial/)
* [Get the size of any screen](https://bugnet.io/blog/fix-pygame-fullscreen-resolution-wrong-size)
* [Load a image in pygame](https://gamedevacademy.org/pygame-image-load-tutorial-complete-guide/)

#### Gameplay, AI & Rendering
* **Pac-Man Ghost AI Personality & Targeting:** [The Pac-Man Dossier by Jamey Pittman](https://cs.au.dk/~ocaprani/GameAI/PacMan/The%20Pac-Man%20Dossier.pdf) & [Pac-Man Patterns — Ghost Movement](https://dev.to/code2bits/pac-man-patterns--ghost-movement-strategy-pattern-1k1a?_sp=ee6d56cc-48d7-4d2e-9df8-786ed73897a8)
* **BFS Pathfinding & Distance Maps:** [Breadth-First Search Distance Maps on Grids (Red Blob Games)](https://www.redblobgames.com/pathfinding/distance-to-any/)
* **MLX-Style Pixel Rendering (`set_at` & `blit`):** [pygame.Surface Reference Guide (Pygame Docs)](https://www.pygame.org/docs/ref/surface.html)

### AI Usage Disclosure
Throughout the development of this project, the AI was used exclusively as a supporting tool to better understand the general project requirements and architecture, as well as to generate custom test cases for verifying and testing the codebase's functionality.