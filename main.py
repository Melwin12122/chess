import pygame
from chess.constants import WIDTH, HEIGHT, CELL_SIZE, BLACK, button_font, RED, GREEN
from chess.board import Board
import sys

pygame.init()


FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

clock = pygame.time.Clock()
clock.tick(FPS)



done = None
events = None

def text_objects(text, font, colour, pos):
    global WIN
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.center = pos
    WIN.blit(text_surface, text_rect)

def button(text, x, y, w, h, colour, active_colour, action=None):
    global events
    mouse = pygame.mouse.get_pos()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(WIN, active_colour, (x-4, y-4, w+10, h+10))
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and action is not None:
                action()
                return True # Button pressed

    else:
        pygame.draw.rect(WIN, colour, (x, y, w, h))


    text_objects(text, button_font, BLACK, ((x + (w // 2)), (y + (h // 2))))


def quit_game():
    pygame.quit()
    sys.exit()

def main():
    global WIN, done, events
    running = True
    board = Board()
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                quit_game()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[1] <= HEIGHT - 58:
                    col = pos[0] // CELL_SIZE
                    row = pos[1] // CELL_SIZE
                    board.select(row, col)
        
        if done is None:
            done = board.draw(WIN)
        if done == 'cm' or done == 'sm':
            menu()

        pygame.draw.rect(WIN, BLACK, (0, HEIGHT-58, WIDTH, 58))
        button("Play again", WIDTH-120, HEIGHT-54, 100, 50, GREEN, RED, action=main)

        pygame.display.update()



def menu():
    global WIN, events
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                quit_game()

        WIN.fill(BLACK)

        button("Start", (WIDTH//2)-50, (HEIGHT//2)-60, 100, 50, RED, GREEN, action=main)
        button("Exit", (WIDTH//2)-50, (HEIGHT//2)+60, 100, 50, GREEN, RED, action=quit_game)

        pygame.display.update()

menu()
