import pygame
from chess.constants import WIDTH, HEIGHT, CELL_SIZE, BLACK
from chess.board import Board

pygame.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
clock.tick(FPS)

board = Board()

done = None

def main():
    global board, WIN, done
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                col = pos[0] // CELL_SIZE
                row = pos[1] // CELL_SIZE
                board.select(row, col)
        
        if done is None:
            done = board.draw(WIN)
        if done == 'cm' or done == 'sm':
            WIN.fill(BLACK)
    
        pygame.display.update()

main()
pygame.quit()
