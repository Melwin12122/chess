import pygame
pygame.font.init()

WIDTH, HEIGHT = 560, 618
ROWS, COLS = 8, 8
CELL_SIZE = WIDTH // COLS

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (207, 58, 159)

# Fonts
button_font = pygame.font.SysFont("comicsans", 20)