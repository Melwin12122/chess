import pygame
from chess.constants import WIDTH, HEIGHT, CELL_SIZE
from chess.board import Board

pygame.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
clock.tick(FPS)

board = Board()

def main():
    global board, WIN
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and not board.check:
                pos = pygame.mouse.get_pos()
                col = pos[0] // CELL_SIZE
                row = pos[1] // CELL_SIZE
                board.select(row, col)
        
        board.draw(WIN)
    
        pygame.display.update()

main()
pygame.quit()
