import pygame

pygame.init()
screen = pygame.display.set_mode((500, 400))

print(pygame.QUIT)

running = True

while running:
    for event in pygame.event.get():
        print(event.type)

        if event.type == pygame.QUIT:
            running = False

pygame.quit()