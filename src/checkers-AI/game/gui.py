import pygame
from config import *

def draw_board(win):
    win.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else GREY
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(win, board):
    for row in board.board:
        for piece in row:
            if piece != 0:
                piece.draw(win)

def highlight_moves(win, moves):
    for (r, c) in moves:
        pygame.draw.circle(win, BLUE, (c*SQUARE_SIZE+SQUARE_SIZE//2, r*SQUARE_SIZE+SQUARE_SIZE//2), 15)

def highlight_last_move(win, last_move):
    (sr, sc), (er, ec) = last_move
    rect_start = pygame.Rect(sc*SQUARE_SIZE, sr*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    rect_end   = pygame.Rect(ec*SQUARE_SIZE, er*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(win, YELLOW, rect_start, 4)
    pygame.draw.rect(win, YELLOW, rect_end, 4)

def highlight_current_pieces(win, pieces):
    for (r, c) in pieces:
        center = (c*SQUARE_SIZE + SQUARE_SIZE//2, r*SQUARE_SIZE + SQUARE_SIZE//2)
        pygame.draw.circle(win, GREEN, center, SQUARE_SIZE//2 - 5, 3)
