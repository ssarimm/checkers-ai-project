from game.piece import Piece
from config import ROWS, COLS, RED, WHITE

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 18
        self.red_kings = self.white_kings = 0
        self.create_board()

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col] = 0
        piece.move(row, col)
        self.board[row][col] = piece

        if row == 0 and piece.color == RED and not piece.king:
            piece.make_king()
            self.red_kings += 1
        elif row == ROWS - 1 and piece.color == WHITE and not piece.king:
            piece.make_king()
            self.white_kings += 1

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, col, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if col < 0:
                break

            current = self.board[r][col]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, col)] = last + skipped
                else:
                    moves[(r, col)] = last

                if last:
                    row_direction = step
                    moves.update(self._traverse_left(r + row_direction, stop, step, color, col - 1, skipped=last))
                    moves.update(self._traverse_right(r + row_direction, stop, step, color, col + 1, skipped=last))
                break

            elif current.color == color:
                break
            else:
                last = [current]

            col -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, col, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if col >= COLS:
                break

            current = self.board[r][col]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, col)] = last + skipped
                else:
                    moves[(r, col)] = last

                if last:
                    row_direction = step
                    moves.update(self._traverse_left(r + row_direction, stop, step, color, col - 1, skipped=last))
                    moves.update(self._traverse_right(r + row_direction, stop, step, color, col + 1, skipped=last))
                break

            elif current.color == color:
                break
            else:
                last = [current]

            col += 1

        return moves

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None

    def get_all_pieces(self, color):
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    yield piece

    def copy(self):
        import copy
        return copy.deepcopy(self)
