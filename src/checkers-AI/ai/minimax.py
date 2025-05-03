import math
from game.board import Board
from config import RED, WHITE

class MinimaxAgent:
    def __init__(self, depth=4, color=WHITE):
        self.depth = depth
        self.color = color

    def evaluate(self, board):
        white = sum(1 for _ in board.get_all_pieces(WHITE))
        red = sum(1 for _ in board.get_all_pieces(RED))
        return white - red if self.color == WHITE else red - white

    def get_move(self, board):
        
        if board.winner() is not None:
            return None
            
        _, move = self.minimax(board, self.depth, -math.inf, math.inf, True)
        return move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.winner():
            return self.evaluate(board), None

        best_move = None
        if maximizing_player:
            max_eval = -math.inf
            for move in self.get_all_possible_moves(board, self.color):
                eval, _ = self.minimax(move[1], depth-1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move[0]
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            opponent_color = RED if self.color == WHITE else WHITE
            for move in self.get_all_possible_moves(board, opponent_color):
                eval, _ = self.minimax(move[1], depth-1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move[0]
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_all_possible_moves(self, board, color):
        """
        Generate (move, new_board) pairs for the given color.
        If any captures exist, only return capture moves.
        """
        captures = []
        non_caps = []
    
        for piece in board.get_all_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            for (r, c), skipped in valid_moves.items():
                new_board = board.copy()
                temp_piece = new_board.board[piece.row][piece.col]
                new_board.move(temp_piece, r, c)
                if skipped:
                    new_board.remove(skipped)
                    captures.append(((piece.row, piece.col, r, c), new_board))
                else:
                    non_caps.append(((piece.row, piece.col, r, c), new_board))
    
        # If any capturing moves, those are mandatory:
        return captures if captures else non_caps
