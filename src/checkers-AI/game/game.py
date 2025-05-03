import pygame
from game.board import Board
from game.gui import (
    draw_board, draw_pieces,
    highlight_moves, highlight_last_move,
    highlight_current_pieces
)
from config import *

class Game:
    def __init__(self, win):
        self.win = win
        self._init()
        self.observation_shape = STATE_SHAPE
        self.action_size = ACTION_SIZE

    def _init(self):
        self.board = Board()
        self.selected = None
        self.valid_moves = {}
        self.turn = RED
        self.last_move = None
        self.movable_pieces = []

    def _get_state(self):
        from utils.helpers import state_to_input
        return state_to_input(self.board.board)

    def get_winner(self):
        return self.board.winner()

    def reset(self):
        self._init()
        self.update_movables()
        return self._get_state()

    def step(self, action):
        """
        Execute one RL action and return (next_state, reward, done, info).
        """
        # Decode flat action to board coordinates
        start_row = action // (COLS * ROWS)
        start_col = (action // ROWS) % COLS
        end_row = action % ROWS
        end_col = action % COLS

        moved = False
        reward = 0
        try:
            piece = self.board.board[start_row][start_col]
            if piece and piece.color == self.turn:
                self.selected = piece
                moved = self.select(end_row, end_col)
        except IndexError:
            pass

        # Reward logic
        if moved:
            reward = 1
            if self.get_winner():
                reward = 100
        else:
            reward = -1

        done = self.get_winner() is not None
        return self._get_state(), reward, done, {}

    def update_movables(self):
        self.movable_pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.board[row][col]
                if piece and piece.color == self.turn and self.board.get_valid_moves(piece):
                    self.movable_pieces.append((row, col))

    def select(self, row, col):
        if self.selected and (row, col) in self.valid_moves:
            skipped = self.valid_moves[(row, col)]
            sr, sc = self.selected.row, self.selected.col
            self.board.move(self.selected, row, col)
            if skipped:
                self.board.remove(skipped)
            self.last_move = ((sr, sc), (row, col))
            self.selected.move(row, col)

            # Double jump
            extra = {}
            if skipped:
                extra = self.board.get_valid_moves(self.selected)
            if skipped and any(extra.values()):
                self.valid_moves = extra
                return False

            # End turn
            self._change_turn()
            self.selected = None
            self.valid_moves = {}
            self.update_movables()
            return True

        # Pick a piece
        piece = self.board.board[row][col]
        if piece and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = {}
            return False

        # Deselect
        self.selected = None
        return False

    def _change_turn(self):
        self.turn = WHITE if self.turn == RED else RED

    def handle_events(self, ai_agent=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (ai_agent is None or self.turn != ai_agent.color) and not self.get_winner():
                    x, y = event.pos
                    col = x // SQUARE_SIZE
                    row = y // SQUARE_SIZE
                    self.select(row, col)
        # AI move if provided
        if ai_agent and self.turn == ai_agent.color and not self.get_winner():
            self._ai_move(ai_agent)
        return True

    def _ai_move(self, ai_agent):
        move = ai_agent.get_move(self.board)
        if not move:
            return
        sr, sc, er, ec = move
        piece = self.board.board[sr][sc]
        if not piece or piece.color != ai_agent.color:
            return
        valid = self.board.get_valid_moves(piece)
        if (er, ec) not in valid:
            return
        skipped = valid[(er, ec)]
        # Perform move
        self.board.move(piece, er, ec)
        if skipped:
            self.board.remove(skipped)
        # Record last move
        self.last_move = ((sr, sc), (er, ec))
        # Multi-capture
        if skipped and self.board.get_valid_moves(piece):
            return
        # Finish turn
        self._change_turn()
        self.selected = None
        self.valid_moves = {}
        self.update_movables()

    def update(self):
        if self.selected:
            self.valid_moves = self.board.get_valid_moves(self.selected)
        else:
            self.valid_moves = {}
        self.update_movables()

    def draw(self):
        draw_board(self.win)
        if self.last_move:
            highlight_last_move(self.win, self.last_move)
        highlight_current_pieces(self.win, self.movable_pieces)
        draw_pieces(self.win, self.board)
        highlight_moves(self.win, self.valid_moves)
