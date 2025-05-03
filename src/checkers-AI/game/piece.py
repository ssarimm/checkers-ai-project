import pygame
from config import *


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.calc_pos()

    def calc_pos(self):
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        
        #pygame.draw.circle(win, BLUE, (self.x, self.y), radius + self.OUTLINE)
        
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

        if self.king:
            crown_radius = radius // 2
            pygame.draw.circle(win, (255, 215, 0), (self.x, self.y), crown_radius)  # gold color for king

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return f"{'K' if self.king else 'P'}({self.color})"
