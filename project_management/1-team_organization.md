# Team Organization

## Team Members
* **Member 1 (Login):** ybajdou
* **Member 2 (Login):** aryahi

---

## Shared Responsibilities
Both team members worked together on these parts:
* Designing the general architecture and classes of the project.
* Setting up the `Makefile` (install, run, clean, lint), `flake8`, and `mypy`.
* Packaging the game for deployment on Itch.io.
* Managing the project and writing the `README.md` file.

---

## Individual Tasks

### 1. ybajdou (Core System & UI)
* **Backend:**
  * Read and process the configuration file (JSON with comments).
  * Implement the Highscore system (saving, reading, and managing the top 10 scores).
* **Frontend:**
  * Design and render all menus (Main Menu, Pause Menu, Game Over, and Victory screens).
  * Render the in-game HUD (displaying score, lives, time, and current level).
  * track progress (Main Menu, Playing, Paused, Loss, Win).
  * Implement the full game loop (join all events)

### 2. aryahi (Gameplay Logic & Rendering)
* **Backend:**
  * Integrate the external `A-Maze-ing` package to generate mazes.
  * Implement player logic (movement in corridors, collisions, eating pacgums) and ghost logic (AI, chasing, running away, respawning).
  * Implement the Cheat mode (invincibility, extra lives, level skip).
  * Build the Game State Machine
* **Frontend:**
  * Render the maze and its elements (corridors, pacgums, and super-pacgums in the corners).
  * Render and animate the player and the 4 ghosts on the screen.

---

## Decision Making and Conflict Resolution
* **Updating Structure:** When we want to clean the code and modify classes or project structure, we talk to each other immediately and update the plan together.
* **Git Workflow:** We work using Git. Each member works on their own branch, and when we finish a task, we merge our code together.
* **Conflict Resolution:** We did not have many problems or big fights during the project because we communicated well.
