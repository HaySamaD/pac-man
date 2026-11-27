# Risk Analysis and Mitigation

## 1. Configuration and Save File Errors
* **Risk:** The configuration file or save files might be missing, have wrong permissions, or contain invalid JSON syntax/values.
* **Mitigation:** 
  * We used `try-except` blocks around file loading operations.
  * If a file error happens or values are invalid, the program falls back to safe default values and continues running smoothly without any tracebacks.

## 2. Performance and Lag Issues
* **Risk:** The game could slow down or crash during evaluation due to heavy graphical rendering.
* **Mitigation:** 
  * We avoided heavy real-time drawing in Pygame. Instead, we blit pre-rendered images onto the screen.
  * This optimization keeps the game performance high, stable, and fast.