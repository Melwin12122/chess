import pygame
import os
from .constants import CELL_SIZE



class Piece:
    black_pieces = []
    white_pieces = []
    b_check = False
    w_check = False
    b_checkmate = False
    w_checkmate = False
    b_stalemate = False
    w_stalemate = False

    def __init__(self, row, col, colour):
        self.row = row
        self.col = col
        self.colour = colour
        self.selected = False
        self.img = None
        self.king = False
        self.pawn = False
        self.knight = False
        self.move_list = [] # Moves which could be moved
        self.possible_move = [] # Moves beyond opponent piece
        self.saving_move = [] # Moves which could backup a same piece
        if self.colour == 'w':
            Piece.white_pieces.append(self)
        elif self.colour == 'b':
            Piece.black_pieces.append(self)

    def isSelected(self):
        return self.selected

    def draw(self, win):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        win.blit(self.img, (x, y))

    def cause_check(self):
        if self.colour == 'w':
            for bp in Piece.black_pieces:
                if (self.row, self.col) in bp.move_list:
                    for wp in Piece.white_pieces:
                        if wp.king and (wp.row, wp.col) in bp.move_list:
                            return False , ()
                        elif wp.king and (wp.row, wp.col) in bp.possible_move:
                            return True, (bp.row, bp.col)
        elif self.colour == 'b':
            for wp in Piece.white_pieces:
                if (self.row, self.col) in wp.move_list:
                    for bp in Piece.black_pieces:
                        if bp.king and (bp.row, bp.col) in wp.move_list:
                            return False, ()
                        elif bp.king and (bp.row, bp.col) in wp.possible_move:
                            return True , (wp.row, wp.col)
        return False, ()

    def check_moves(self, moves):
        temp3 = []
        if self.colour == 'w':
            if Piece.w_check:
                for wp in Piece.white_pieces:
                    if wp.king:
                        for bp in Piece.black_pieces:
                            if (wp.row, wp.col) in bp.move_list:
                                if (bp.row, bp.col) in moves:
                                    temp3.append((bp.row, bp.col))
                                block_moves = self.find_moves(wp, bp)
                                for move in moves:
                                    if move in block_moves:
                                        temp3.append(move)
        elif self.colour == 'b':
            if Piece.b_check:
                for bp in Piece.black_pieces:
                    if bp.king:
                        for wp in Piece.white_pieces:
                            if (bp.row, bp.col) in wp.move_list:
                                if (wp.row, wp.col) in moves:
                                    temp3.append((wp.row, wp.col))
                                block_moves = self.find_moves(bp, wp)
                                for move in moves:
                                    if move in block_moves:
                                        temp3.append(move)
        return temp3


    def find_moves(self, king, other):
        moves = []
        if king.row == other.row:
            incr = -1 if other.col > king.col else 1
            for i in range(other.col+incr, king.col, incr):
                moves.append((king.row, i))
        elif king.col == other.col:
            incr = -1 if other.row > king.row else 1
            for i in range(other.row+incr, king.row, incr):
                moves.append((i, king.col))
        elif abs(king.row - other.row) == abs(king.col - other.col):
            r_incr = -1 if other.row > king.row else 1
            c_incr = -1 if other.col > king.col else 1
            if other.col < king.col:
                for i in range(other.col+1, king.col):
                    moves.append((other.row+r_incr, other.col+c_incr))
                    r_incr += r_incr
                    c_incr += c_incr
            elif other.col > king.col:
                for i in range(king.col+1, other.col):
                    moves.append((other.row+r_incr, other.col+c_incr))
                    r_incr += r_incr
                    c_incr += c_incr
        return moves

    def move_straight(self, board, moves, temp, temp2):
        r = self.row
        c = self.col
        beyond = False
        # Up 
        while r > 0:
            r -= 1
            if not beyond:
                if board[r][c] == 0:
                    moves.append((r, c))
                elif board[r][c].colour == self.colour:
                    temp2.append((r, c))
                    temp.append((r, c))
                    break
                elif board[r][c].colour != self.colour:
                    moves.append((r, c))
                    beyond = True
            else:
                if board[r][c] == 0:
                    temp.append((r, c))
                else:
                    temp.append((r, c))
                    break
        
        r = self.row
        beyond = False
        # Down
        while r < 7:
            r += 1
            if not beyond:
                if board[r][c] == 0:
                    moves.append((r, c))
                elif board[r][c].colour == self.colour:
                    temp.append((r, c))
                    temp2.append((r, c))
                    break
                elif board[r][c].colour != self.colour:
                    moves.append((r, c))
                    beyond = True
            else:
                if board[r][c] == 0:
                    temp.append((r, c))
                else:
                    temp.append((r, c))
                    break

        r = self.row
        c = self.col
        beyond = False
        # Left
        while c > 0:
            c -= 1
            if not beyond:
                if board[r][c] == 0:
                    moves.append((r, c))
                elif board[r][c].colour == self.colour:
                    temp.append((r, c))
                    temp2.append((r, c))
                    break
                elif board[r][c].colour != self.colour:
                    moves.append((r, c))
                    beyond = True
            else:
                if board[r][c] == 0:
                    temp.append((r, c))
                else:
                    temp.append((r, c))
                    break
        
        c = self.col
        beyond = False
        # Right
        while c < 7:
            c += 1
            if not beyond:
                if board[r][c] == 0:
                    moves.append((r, c))
                elif board[r][c].colour == self.colour:
                    temp.append((r, c))
                    temp2.append((r, c))
                    break
                elif board[r][c].colour != self.colour:
                    moves.append((r, c))
                    beyond = True
            else:
                if board[r][c] == 0:
                    temp.append((r, c))
                else:
                    temp.append((r, c))
                    break

    def move_diagonal(self, board, moves, temp, temp2):
        r = self.row
        lc = self.col # left column
        rc = self.col # right column
        Lbeyond = False
        Rbeyond = False

        # Diagonal Up
        while r > 0:
            r -= 1

            lc -= 1
            if lc >= 0 and not Lbeyond:
                if board[r][lc] == 0:
                    moves.append((r, lc))
                elif board[r][lc].colour == self.colour:
                    temp.append((r, lc))
                    temp2.append((r, lc))
                    lc = -1 # Stop running this block
                elif board[r][lc].colour != self.colour:
                    moves.append((r, lc))
                    Lbeyond = True
            elif lc >= 0 and Lbeyond:
                if board[r][lc] == 0:
                    temp.append((r, lc))
                else:
                    temp.append((r, lc))
                    lc = -1
                    Lbeyond = False

            rc += 1
            if rc <= 7 and not Rbeyond:
                if board[r][rc] == 0:
                    moves.append((r, rc))
                elif board[r][rc].colour == self.colour:
                    temp.append((r, rc))
                    temp2.append((r, rc))
                    rc = 8 # Stop running this block  
                elif board[r][rc].colour != self.colour:
                    moves.append((r, rc))
                    Rbeyond = True
            elif rc <= 7 and Rbeyond:
                if board[r][rc] == 0:
                    temp.append((r, rc))
                else:
                    temp.append((r, rc))
                    rc = 8
                    Rbeyond = False

        r = self.row
        lc = self.col # left column
        rc = self.col # right column
        Lbeyond = False
        Rbeyond = False

        # Diagonal Down
        while r < 7:
            r += 1

            lc -= 1
            if lc >= 0 and not Lbeyond:
                if board[r][lc] == 0:
                    moves.append((r, lc))
                elif board[r][lc].colour == self.colour:
                    temp.append((r, lc))
                    temp2.append((r, lc))
                    lc = -1 # Stop running this block
                elif board[r][lc].colour != self.colour:
                    moves.append((r, lc))
                    Lbeyond = True
            elif lc >= 0 and Lbeyond:
                if board[r][lc] == 0:
                    temp.append((r, lc))
                else:
                    temp.append((r, lc))
                    lc = -1
                    Lbeyond = False

            rc += 1
            if rc <= 7 and not Rbeyond:
                if board[r][rc] == 0:
                    moves.append((r, rc))
                elif board[r][rc].colour == self.colour:
                    temp.append((r, rc))
                    temp2.append((r, rc))
                    rc = 8 # Stop running this block
                elif board[r][rc].colour != self.colour:
                    moves.append((r, rc))
                    Rbeyond = True
            elif rc <= 7 and not  Rbeyond:
                if board[r][rc] == 0:
                    temp.append((r, rc))
                else:
                    temp.append((r, rc))
                    rc = 8
                    Rbeyond = False

class Rook(Piece):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("imgs" , colour + "R.png")), (CELL_SIZE, CELL_SIZE))

    def valid_moves(self, board):

        moves = []
        temp = []
        temp2 = []
        
        self.move_straight(board ,moves, temp, temp2)

        temp3 = self.check_moves(moves)

        value, pos = self.cause_check()
        
        if value:
            if pos in moves:
                moves = []
                moves.append(pos)
            else:
                moves = [] 

        if (Piece.w_check and self.colour == 'w') or (Piece.b_check and self.colour == 'b'):
            self.move_list = temp3
        else:
            self.move_list = moves

        self.possible_move = temp
        self.saving_move = temp2
        

class Queen(Piece):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("imgs" , colour + "Q.png")), (CELL_SIZE, CELL_SIZE))

    def valid_moves(self, board):
        moves = []
        temp = []
        temp2 = []
        
        self.move_straight(board, moves, temp, temp2)
        self.move_diagonal(board, moves, temp, temp2)
        
        temp3 = self.check_moves(moves)
                                
        value, pos = self.cause_check()
        
        if value:
            if pos in moves:
                moves = []
                moves.append(pos)
            else:
                moves = []

        if (Piece.w_check and self.colour == 'w') or (Piece.b_check and self.colour == 'b'):
            self.move_list = temp3
        else:
            self.move_list = moves

        self.possible_move = temp
        self.saving_move = temp2

class King(Piece):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.king = True
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("imgs" , colour + "K.png")), (CELL_SIZE, CELL_SIZE))

    def valid_moves(self, board):
        r = self.row
        c = self.col 
        moves = []
        temp = []

        if r >= 1 and c >= 1 and (board[r-1][c-1] == 0 or board[r-1][c-1].colour != self.colour):
            if self.king_pos(r-1, c-1, board):
                moves.append((r-1, c-1))
            else:
                temp.append((r-1, c-1))
        

        if r >= 1 and (board[r-1][c] == 0 or board[r-1][c].colour != self.colour):
            if self.king_pos(r-1, c, board):
                moves.append((r-1, c))
            else:
                temp.append((r-1, c))

        if r >= 1 and c <= 6 and (board[r-1][c+1] == 0 or board[r-1][c+1].colour != self.colour):
            if self.king_pos(r-1, c+1, board):
                moves.append((r-1, c+1))
            else:
                temp.append((r-1, c+1))

        if c >= 1 and (board[r][c-1] == 0 or board[r][c-1].colour != self.colour):
            if self.king_pos(r, c-1, board):
                moves.append((r, c-1))
            else:
                temp.append((r, c-1))

        if c <= 6 and (board[r][c+1] == 0 or board[r][c+1].colour != self.colour):
            if self.king_pos(r, c+1, board):
                moves.append((r, c+1))
            else:
                temp.append((r, c+1))
            
        if r <= 6 and c >= 1 and (board[r+1][c-1] == 0 or board[r+1][c-1].colour != self.colour):
            if self.king_pos(r+1, c-1, board):
                moves.append((r+1, c-1))
            else:
                temp.append((r+1, c-1))
        
        if r <= 6 and (board[r+1][c] == 0 or board[r+1][c].colour != self.colour):
            if self.king_pos(r+1, c, board):
                moves.append((r+1, c))
            else:
                temp.append((r+1, c))
            
        if r <= 6 and c <= 6 and (board[r+1][c+1] == 0 or board[r+1][c+1].colour != self.colour):
            if self.king_pos(r+1, c+1, board):
                moves.append((r+1, c+1))
            else:
                temp.append((r+1, c+1))
        
        if self.colour == 'b':
            for wp in Piece.white_pieces:
                if (self.row, self.col) in wp.move_list:
                    Piece.b_check = True
                    break
            else:
                Piece.b_check = False
        
            if Piece.b_check and moves == []:
                for bp in Piece.black_pieces:
                    if bp.move_list == []:
                        Piece.b_checkmate = True

            if not Piece.b_check and moves == []:
                for bp in Piece.black_pieces:
                    if bp.move_list == []:
                        Piece.b_stalemate = True
        elif self.colour == 'w':
            for bp in Piece.black_pieces:
                if (self.row, self.col) in bp.move_list:
                    Piece.w_check = True
                    break
            else:
                Piece.w_check = False
                
                if Piece.w_check and moves == []:
                    for wp in Piece.white_pieces:
                        if wp.move_list == []:
                            Piece.w_checkmate = True
                
                if not Piece.w_check and moves == []:
                    for wp in Piece.white_pieces:
                        if wp.move_list == []:
                            Piece.w_stalemate = True

        self.move_list = moves
        self.possible_move = temp

    def king_pos(self, r, c, board):
        if self.colour == 'w':
            for bp in Piece.black_pieces:
                if bp.king:
                    if r in range(bp.row-1, bp.row+2):
                        if c in range(bp.col-1, bp.col+2):
                            return False 
                if (r, c) in bp.move_list:
                    if not bp.pawn:
                        return False
                    else:
                        if (r, c) in ((bp.row+1, bp.col-1), (bp.row+1, bp.col+1)):
                            return False
                if Piece.w_check and (r, c) in bp.possible_move and (self.row, self.col) in bp.move_list:
                    return False
                if (r, c) == (bp.row, bp.col):
                    for bp2 in Piece.black_pieces:
                        if (r, c) in bp2.saving_move:
                            return False
                
        if self.colour == 'b':
            for wp in Piece.white_pieces:
                if wp.king:
                    if r in range(wp.row-1, wp.row+2):
                        if c in range(wp.col-1, wp.col+2):
                            return False 
                if (r, c) in wp.move_list:
                    if not wp.pawn:
                        return False
                    else:
                        if (r, c) in ((wp.row-1, wp.col-1), (wp.row-1, wp.col+1)):
                            return False
                if Piece.b_check and (r, c) in wp.possible_move and (self.row, self.col) in wp.move_list:
                    return False 
                if (r, c) == (wp.row, wp.col):
                    for wp2 in Piece.white_pieces:
                        if (r, c) in wp2.saving_move:
                            return False
        return True

        
class Knight(Piece):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.knight = True
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("imgs" , colour + "Kn.png")), (CELL_SIZE, CELL_SIZE))

    def valid_moves(self, board):
        r = self.row
        c = self.col
        moves = []
        temp = []

        # Up
        if r >= 2:
            if c >= 1 and (board[r-2][c-1] == 0 or board[r-2][c-1].colour != self.colour):
                moves.append((r-2, c-1))
            elif c >= 1 and (board[r-2][c-1] == 0 or board[r-2][c-1].colour == self.colour):
                temp.append((r-2, c-1))
        
            if c <= 6 and (board[r-2][c+1] == 0 or board[r-2][c+1].colour != self.colour):
                moves.append((r-2, c+1))
            elif c <= 6 and (board[r-2][c+1] == 0 or board[r-2][c+1].colour == self.colour):
                temp.append((r-2, c+1))
        
        # Down
        if r <= 5:
            if c >= 1 and (board[r+2][c-1] == 0 or board[r+2][c-1].colour != self.colour):
                moves.append((r+2, c-1))
            elif c >= 1 and (board[r+2][c-1] == 0 or board[r+2][c-1].colour == self.colour):
                temp.append((r+2, c-1))

            if c <= 6 and (board[r+2][c+1] == 0 or board[r+2][c+1].colour != self.colour):
                moves.append((r+2, c+1))
            elif c <= 6 and (board[r+2][c+1] == 0 or board[r+2][c+1].colour == self.colour):
                temp.append((r+2, c+1))

        # Left
        if c >= 2:
            if r >= 1 and (board[r-1][c-2] == 0 or board[r-1][c-2].colour != self.colour):
                moves.append((r-1, c-2))
            elif r >= 1 and (board[r-1][c-2] == 0 or board[r-1][c-2].colour == self.colour):
                temp.append((r-1, c-2))

            if r <= 6 and (board[r+1][c-2] == 0 or board[r+1][c-2].colour != self.colour):
                moves.append((r+1, c-2))
            elif r <= 6 and (board[r+1][c-2] == 0 or board[r+1][c-2].colour == self.colour):
                temp.append((r+1, c-2))

        # Right
        if c <= 5:
            if r >= 1 and (board[r-1][c+2] == 0 or board[r-1][c+2].colour != self.colour):
                moves.append((r-1, c+2))
            elif r >= 1 and (board[r-1][c+2] == 0 or board[r-1][c+2].colour == self.colour):
                temp.append((r-1, c+2))

            if r <= 6 and (board[r+1][c+2] == 0 or board[r+1][c+2].colour != self.colour):
                moves.append((r+1, c+2))
            elif r <= 6 and (board[r+1][c+2] == 0 or board[r+1][c+2].colour == self.colour):
                temp.append((r+1, c+2))

        temp3 = self.check_moves(moves)

        if (Piece.w_check and self.colour == 'w') or (Piece.b_check and self.colour == 'b'):
            self.move_list = temp3
        else:
            self.move_list = moves

        self.possible_move = temp
        self.saving_move = self.possible_move

class Bishop(Piece):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("imgs" , colour + "B.png")), (CELL_SIZE, CELL_SIZE))

    def valid_moves(self, board):
        moves = []
        temp = []
        temp2 = []

        self.move_diagonal(board, moves, temp, temp2)

        temp3 = self.check_moves(moves)

        value, pos = self.cause_check()
        
        if value:
            if pos in moves:
                moves = []
                moves.append(pos)
            else:
                moves = []

        if (Piece.w_check and self.colour == 'w') or (Piece.b_check and self.colour == 'b'):
            self.move_list = temp3
        else:
            self.move_list = moves


        self.possible_move = temp 
        self.saving_move = temp2

class Pawn(Piece):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.first_move = True
        self.pawn = True
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("imgs" , colour + "P.png")), (CELL_SIZE, CELL_SIZE))


    def valid_moves(self, board):
        r = self.row
        c = self.col
        moves = []
        temp2 = []

        if self.colour == 'w':
            if self.first_move:
                for i in range(1, 3):
                    if board[r-i][c] != 0:
                        break
                    moves.append((r-i, c))
                if c >= 1 and board[r-1][c-1] != 0 and board[r-1][c-1].colour != self.colour:
                    for wp in Piece.white_pieces:
                        if wp.king:
                            for bp in Piece.black_pieces:
                                if (wp.row, wp.col) in bp.possible_move:
                                    break
                            else:
                                moves.append((r-1, c-1))
                if c<= 6 and board[r-1][c+1] != 0 and board[r-1][c+1].colour != self.colour:
                    for wp in Piece.white_pieces:
                        if wp.king:
                            for bp in Piece.black_pieces:
                                if (wp.row, wp.col) in bp.possible_move:
                                    break
                            else:
                                moves.append((r-1, c+1))
                if c >= 1 and board[r-1][c-1] != 0 and board[r-1][c-1].colour == self.colour:
                    temp2.append((r-1, c-1))
                if c<= 6 and board[r-1][c+1] != 0 and board[r-1][c+1].colour == self.colour:
                    temp2.append((r-1, c+1))
                
            else:
                if board[r-1][c] == 0:
                    moves.append((r-1, c))
                if r >= 1 and c >= 1 and board[r-1][c-1] != 0 and board[r-1][c-1].colour != self.colour:
                    for wp in Piece.white_pieces:
                        if wp.king:
                            for bp in Piece.black_pieces:
                                if (wp.row, wp.col) in bp.possible_move:
                                    break
                            else:
                                moves.append((r-1, c-1))
                if r >= 1 and c<= 6 and board[r-1][c+1] != 0 and board[r-1][c+1].colour != self.colour:
                    for wp in Piece.white_pieces:
                        if wp.king:
                            for bp in Piece.black_pieces:
                                if (wp.row, wp.col) in bp.possible_move:
                                    break
                            else:
                                moves.append((r-1, c+1))
                if r >= 1 and c >= 1 and board[r-1][c-1] != 0 and board[r-1][c-1].colour == self.colour:
                    temp2.append((r-1, c-1))
                if r >= 1 and c<= 6 and board[r-1][c+1] != 0 and board[r-1][c+1].colour == self.colour:
                    temp2.append((r-1, c+1))

        elif self.colour == 'b':
            if self.first_move:
                for i in range(1, 3):
                    if board[r+i][c] != 0:
                        break
                    moves.append((r+i, c))
                if c >= 1 and board[r+1][c-1] != 0 and board[r+1][c-1].colour != self.colour:
                    for bp in Piece.black_pieces:
                        if bp.king:
                            for wp in Piece.white_pieces:
                                if (bp.row, bp.col) in wp.possible_move:
                                    break
                            else:
                                moves.append((r+1, c-1))
                if c<= 6 and board[r+1][c+1] != 0 and board[r+1][c+1].colour != self.colour:
                    for bp in Piece.black_pieces:
                        if bp.king:
                            for wp in Piece.white_pieces:
                                if (bp.row, bp.col) in wp.possible_move:
                                    break
                            else:
                                moves.append((r+1, c+1))
                if c >= 1 and board[r+1][c-1] != 0 and board[r+1][c-1].colour == self.colour:
                    temp2.append((r+1, c-1))
                if c<= 6 and board[r+1][c+1] != 0 and board[r+1][c+1].colour == self.colour:
                    temp2.append((r+1, c+1))
            else:
                if board[r+1][c] == 0:
                    moves.append((r+1, c))
                if r <= 6 and c >= 1 and board[r+1][c-1] != 0 and board[r+1][c-1].colour != self.colour:
                    for bp in Piece.black_pieces:
                        if bp.king:
                            for wp in Piece.white_pieces:
                                if (bp.row, bp.col) in wp.possible_move:
                                    break
                            else:
                                moves.append((r+1, c-1))
                if r <= 6 and c<= 6 and board[r+1][c+1] != 0 and board[r+1][c+1].colour != self.colour:
                    for bp in Piece.black_pieces:
                        if bp.king:
                            for wp in Piece.white_pieces:
                                if (bp.row, bp.col) in wp.possible_move:
                                    break
                            else:
                                moves.append((r+1, c+1))
                if r <= 6 and c >= 1 and board[r+1][c-1] != 0 and board[r+1][c-1].colour == self.colour:
                    temp2.append((r+1, c-1))
                if r <= 6 and c<= 6 and board[r+1][c+1] != 0 and board[r+1][c+1].colour == self.colour:
                    temp2.append((r+1, c+1))
        
        temp3 = self.check_moves(moves)
    
        if (Piece.w_check and self.colour == 'w') or (Piece.b_check and self.colour == 'b'):
            self.move_list = temp3
        else:
            self.move_list = moves

        self.saving_move = temp2
        