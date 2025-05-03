import numpy as np
from config import WHITE

def state_to_input(state):
    """
    Convert board.board (2D list of Piece or 0) to numpy array for NN input.
    """
    arr = np.zeros((len(state), len(state[0])), dtype=int)
    for r in range(len(state)):
        for c in range(len(state[0])):
            piece = state[r][c]
            if piece == 0:
                val = 0
            else:
                val = 1 if piece.color == WHITE else -1
                if piece.king:
                    val *= 2
            arr[r, c] = val
    return arr.reshape((*arr.shape, 1))