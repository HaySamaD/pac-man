import sys
import pygame
from mazegenerator import MazeGenerator
from src.maze_board import MazeBoard
from src.renderer import Renderer


# --------------------------------------------------------------------------------

def main() -> None:
    gen = MazeGenerator(size=(21, 21), seed=42)
    board = MazeBoard.from_raw_maze(gen.maze)

    renderer = Renderer(board, tile_size=45)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        renderer.render_map()
        renderer.update_desplay()

    pygame.quit()
    sys.exit(0)

# --------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
