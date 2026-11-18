# Acceptance Test Plan and Bug Fixing

## 1. Testing Methods and Tools
* **Traceback Monitoring:** We use Python traceback messages to detect and track errors during execution.
* **Print Debugging:** We use `print()` functions in our code to check outputs, test variables, and verify values at every step.

## 2. Important Bug Found and Fixed (Refactoring the Game Loop)
* **The Problem:** When we first tried to write the game loop, the code became extremely long, especially with too many `if` statements.
* **The Solution:** We divided the code into 6 separate files, where each file represents a single class and object. This made the code cleaner, shorter, and much easier to maintain.

## 3. Testing Cheat Mode and Configuration Files
* **Cheat Mode Testing:** We tested cheat features (like invincibility and level skipping) during gameplay to make sure evaluators can easily test all parts of the game.
* **Config Testing:** We tested missing or broken configuration files to verify that our program handles errors smoothly with `try-except` and default values without crashing.