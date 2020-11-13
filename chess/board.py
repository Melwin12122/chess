import pygame
from .constants import ROWS, COLS, CELL_SIZE, BLACK, WHITE, BROWN, RED, YELLOW, BLUE, PURPLE
from .piece import Rook, King, Queen, Bishop, Pawn, Knight
from tkinter import *

class Board:
    
    def __init__(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.selected = []
        self.turn = 'w'

        self.board[0][0] = Rook(0, 0, "b")
        self.board[0][1] = Knight(0, 1, "b")
        self.board[0][2] = Bishop(0, 2, "b")
        self.board[0][3] = Queen(0, 3, "b")
        self.board[0][4] = King(0, 4, "b")
        self.board[0][5] = Bishop(0, 5, "b")
        self.board[0][6] = Knight(0, 6, "b")
        self.board[0][7] = Rook(0, 7, "b")

        self.board[1][0] = Pawn(1, 0, "b")
        self.board[1][1] = Pawn(1, 1, "b")
        self.board[1][2] = Pawn(1, 2, "b")
        self.board[1][3] = Pawn(1, 3, "b")
        self.board[1][4] = Pawn(1, 4, "b")
        self.board[1][5] = Pawn(1, 5, "b")
        self.board[1][6] = Pawn(1, 6, "b")
        self.board[1][7] = Pawn(1, 7, "b")

        self.board[7][0] = Rook(7, 0, "w")
        self.board[7][1] = Knight(7, 1, "w")
        self.board[7][2] = Bishop(7, 2, "w")
        self.board[7][3] = Queen(7, 3, "w")
        self.board[7][4] = King(7, 4, "w")
        self.board[7][5] = Bishop(7, 5, "w")
        self.board[7][6] = Knight(7, 6, "w")
        self.board[7][7] = Rook(7, 7, "w")

        self.board[6][0] = Pawn(6, 0, "w")
        self.board[6][1] = Pawn(6, 1, "w")
        self.board[6][2] = Pawn(6, 2, "w")
        self.board[6][3] = Pawn(6, 3, "w")
        self.board[6][4] = Pawn(6, 4, "w")
        self.board[6][5] = Pawn(6, 5, "w")
        self.board[6][6] = Pawn(6, 6, "w")
        self.board[6][7] = Pawn(6, 7, "w")
        self.pawn_promo = None


    def draw(self, win):
        win.fill(BROWN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (CELL_SIZE * col, CELL_SIZE * row, CELL_SIZE, CELL_SIZE))
                

        if self.selected != []:
            pygame.draw.rect(win, YELLOW, (CELL_SIZE * self.selected[0][1], CELL_SIZE * self.selected[0][0], CELL_SIZE, CELL_SIZE))

        if len(self.selected) == 1:
            row = self.selected[0][0]
            col = self.selected[0][1]
            for r, c in self.board[row][col].move_list:
                pygame.draw.rect(win, YELLOW, (CELL_SIZE * c, CELL_SIZE * r, CELL_SIZE, CELL_SIZE))
                if self.board[r][c] != 0: # Opposition piece
                    pygame.draw.rect(win, RED, (CELL_SIZE * c, CELL_SIZE * r, CELL_SIZE, CELL_SIZE))
            if self.board[row][col].king or self.board[row][col].pawn:
                for r, c in self.board[row][col].specialmoves:
                    pygame.draw.rect(win, PURPLE, (CELL_SIZE * c, CELL_SIZE * r, CELL_SIZE, CELL_SIZE))

        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != 0:
                    if self.board[row][col].king:
                        if self.board[row][col].colour == 'b' and self.board[row][col].b_check:
                            pygame.draw.rect(win, BLUE, (CELL_SIZE * col, CELL_SIZE * row, CELL_SIZE, CELL_SIZE))
                        elif self.board[row][col].colour == 'w' and self.board[row][col].w_check:
                            pygame.draw.rect(win, BLUE, (CELL_SIZE * col, CELL_SIZE * row, CELL_SIZE, CELL_SIZE))
                    self.board[row][col].draw(win)
                    self.board[row][col].valid_moves(self.board)
                pygame.draw.rect(win, BLACK, (CELL_SIZE * col, CELL_SIZE * row, CELL_SIZE, CELL_SIZE), 2) # border
                    
  
    def select(self, row, col):
        # UNSELECT and same team selection
        if self.board[row][col] != 0 or self.selected != []:
            if self.selected == [] and self.occupied(row, col):
                if (self.turn == 'w' and self.board[row][col].colour == 'w') or (self.turn == 'b' and self.board[row][col].colour == 'b'):
                    self.selected.append((row, col))
            elif len(self.selected) == 1 and (row, col) == self.selected[0]:
                self.selected = []
            elif len(self.selected) == 1 and (row, col) in self.board[self.selected[0][0]][self.selected[0][1]].move_list:
                self.selected.append((row, col))
                r1, c1 = self.selected[0][0], self.selected[0][1]
                r2, c2 = self.selected[1][0], self.selected[1][1]
                self.change_pos(r1, c1, r2, c2)
                self.selected = []
            elif len(self.selected) == 1 and self.board[self.selected[0][0]][self.selected[0][1]].king:
                r = self.selected[0][0]
                c = self.selected[0][1]
                if (row, col) in self.board[r][c].specialmoves:
                    if col > c:
                        if self.board[r][c].colour == 'w':
                            self.board[7][6] = self.board[7][4]
                            self.board[7][5] = self.board[7][7]
                            self.board[7][4] = self.board[7][7] = 0
                            self.board[7][6].col = 6
                            self.board[7][5].col = 5
                            self.board[7][6].castled = True
                        elif self.board[r][c].colour == 'b':
                            self.board[0][6] = self.board[0][4]
                            self.board[0][5] = self.board[0][7]
                            self.board[0][4] = self.board[0][7] = 0
                            self.board[0][6].col = 6
                            self.board[0][5].col = 5
                            self.board[0][6].castled = True
                    elif col < c:
                        if self.board[r][c].colour == 'w':
                            self.board[7][2] = self.board[7][4]
                            self.board[7][3] = self.board[7][0]
                            self.board[7][4] = self.board[7][0] = 0
                            self.board[7][2].col = 2
                            self.board[7][3].col = 3
                            self.board[7][2].castled = True
                        elif self.board[r][c].colour == 'b':
                            self.board[0][2] = self.board[0][4]
                            self.board[0][3] = self.board[0][0]
                            self.board[0][4] = self.board[0][0] = 0
                            self.board[0][2].col = 2
                            self.board[0][3].col = 3
                            self.board[0][2].castled = True
                    self.turn = 'w' if self.turn == 'b' else 'b'
                    self.selected = []
            elif len(self.selected) == 1 and self.board[self.selected[0][0]][self.selected[0][1]].pawn:
                r = self.selected[0][0]
                c = self.selected[0][1]
                if (row, col) in self.board[r][c].specialmoves:
                    self.board[r][c].row = self.board[r][c].col = None
                    self.popup()
                    if self.board[row][col] != 0:
                        self.board[row][col].row = self.board[row][col].col = None
                        if self.board[row][col].colour == 'b':
                            self.board[r][c].black_pieces.remove(self.board[row][col])
                        elif self.board[row][col].colour == 'w':
                            self.board[r][c].white_pieces.remove(self.board[row][col])
                    if self.board[r][c].colour == 'w':
                        self.board[r][c].white_pieces.remove(self.board[r][c])
                        self.board[r][c] = 0
                        if self.pawn_promo == 'queen' or self.pawn_promo is None:
                            self.board[row][col] = Queen(row, col, 'w')
                        elif self.pawn_promo == 'rook':
                            self.board[row][col] = Rook(row, col, 'w')
                        elif self.pawn_promo == 'knight':
                            self.board[row][col] = Knight(row, col, 'w')
                        elif self.pawn_promo == 'bishop':
                            self.board[row][col] = Bishop(row, col, 'w')
                    elif self.board[r][c].colour == 'b':
                        self.board[r][c].black_pieces.remove(self.board[r][c])
                        self.board[r][c] = 0
                        if self.pawn_promo == 'queen' or self.pawn_promo is None:
                            self.board[row][col] = Queen(row, col, 'b')
                        elif self.pawn_promo == 'rook':
                            self.board[row][col] = Rook(row, col, 'b')
                        elif self.pawn_promo == 'knight':
                            self.board[row][col] = Knight(row, col, 'b')
                        elif self.pawn_promo == 'bishop':
                            self.board[row][col] = Bishop(row, col, 'b')
                
                    self.turn = 'w' if self.turn == 'b' else 'b'
                    self.selected = []
            elif len(self.selected) == 1 and not self.occupied(row, col):
                pass
            if len(self.selected) == 1 and self.occupied(row, col):
                if (self.turn == 'w' and self.board[row][col].colour == 'w') or (self.turn == 'b' and self.board[row][col].colour == 'b'):
                    self.selected[0] = (row, col)


            
    def occupied(self, row, col):
        if self.board[row][col] != 0:
            return True
        return False

    def change_pos(self, r1, c1, r2, c2):
        if self.board[r2][c2] != 0:
            self.board[r2][c2].move_list = list()
            self.board[r2][c2].possible_move = list()
            self.board[r2][c2].row = None
            self.board[r2][c2].col = None

        if self.board[r1][c1].pawn:
            self.board[r1][c1].first_move = False

        self.board[r1][c1].row = r2
        self.board[r1][c1].col = c2

        if self.board[r2][c2] != 0:
            if self.board[r2][c2].colour == 'w':
                self.board[r2][c2].white_pieces.remove(self.board[r2][c2])
            elif self.board[r2][c2].colour == 'b':
                self.board[r2][c2].black_pieces.remove(self.board[r2][c2])        
                    
        self.board[r2][c2] = self.board[r1][c1]
        self.board[r1][c1] = 0
        self.turn = 'w' if self.turn == 'b' else 'b'

    def popup(self):
        root = Tk()
        root.overrideredirect(True)

        Button(root, text="QUEEN", padx=50, pady=30, command=lambda: self.click("queen", root)).grid(row=0, column=0)
        Button(root, text="ROOK", padx=50, pady=30, command=lambda: self.click("rook", root)).grid(row=0, column=1)
        Button(root, text="KNIGHT", padx=50, pady=30, command=lambda: self.click("knight", root)).grid(row=1, column=0)
        Button(root, text="BISHOP", padx=50, pady=30, command=lambda: self.click("bishop", root)).grid(row=1, column=1)

        root.mainloop()
    
    def click(self, str1, root):
        root.destroy()
        self.pawn_promo = str1