# Project Analysis and Technical Choices

## 1. Object-Oriented Programming (OOP)
* We used Object-Oriented Programming (OOP) in this project.
* OOP makes our code more readable and scalable.
* We divided the code into clear classes (like Player, Ghost, GameState, and MazeGenerator) to organize everything easily.

## 2. External Package Integration
- **Wrapper Class (`MazeBoard`):** We imported `MazeGenerator` from the `mazegenerator` package and wrapped it inside our `MazeBoard` class. This keeps the external library separate from the player, ghosts, and renderer logic.
- **Pac-Man Loops (`perfect=False`):** We initialized `MazeGenerator` with `perfect=False`. This removes dead-ends and creates looped corridors so the player is never trapped in a corner by ghosts.
- **Wall Bitmasks and "42" Pattern:** `MazeGenerator.maze` returns a 2D grid of integers representing 4-bit wall masks (`1` = Up, `2` = Right, `4` = Down, `8` = Left). Cells with value `15` form the central "42" pattern, which `MazeBoard` marks as solid walls (`TileType.WALL`) and `Renderer` draws onto the maze surface.
- **Seed Control and Safe Fallback:** Level 1 uses a fixed seed from the configuration file for consistent testing, while higher levels generate random seeds.

## 3. Configuration File and Faulty Values Handling
* **Comments Handling:** Our program reads a JSON configuration file. If the file has comment lines starting with `#`, our code skips them and only reads the important settings.
* **Faulty Values Handling:** If a configuration value is missing or invalid, our program does not crash. It replaces the wrong value with a safe default value and continues running smoothly.