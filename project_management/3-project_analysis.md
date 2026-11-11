# Project Analysis and Technical Choices

## 1. Object-Oriented Programming (OOP)
* We used Object-Oriented Programming (OOP) in this project.
* OOP makes our code more readable and scalable.
* We divided the code into clear classes (like Player, Ghost, GameState, and MazeGenerator) to organize everything easily.

## 2. External Package Integration (`A-Maze-ing`)
#####
#########################################
How did you integrate the external A-Maze-ing package?
#########################################
#####

## 3. Configuration File and Faulty Values Handling
* **Comments Handling:** Our program reads a JSON configuration file. If the file has comment lines starting with `#`, our code skips them and only reads the important settings.
* **Faulty Values Handling:** If a configuration value is missing or invalid, our program does not crash. It replaces the wrong value with a safe default value and continues running smoothly.