from utils import *

def alphabeta_search(board, d=4, cutoff_test=None, eval_fn=score):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    def max_value(board, alpha, beta, depth):
        if cutoff_test(board, depth):
            return eval_fn(board)
        v = -infinity
        for move in board.get_moves():
            active = board.active
            B = board.peek_move(move)
            if B.active != active:
                v = max(v, min_value(B, alpha, beta, depth+1))
            else:
                v = max(v, max_value(B, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(board, alpha, beta, depth):
        if cutoff_test(board, depth):
            return eval_fn(board)
        v = infinity
        for move in board.get_moves():
            active = board.active
            B = board.peek_move(move)
            if B.active != active:
                v = min(v, max_value(B, alpha, beta, depth+1))
            else:
                v = min(v, min_value(B, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda board,depth: depth>d or board.is_over()))

    def best(move):
        B = board.peek_move(move)
        if B.active != board.active:
            return min_value(B, -infinity, infinity, 0)
        else:
            return max_value(B, -infinity, infinity, 0)

    return argmax(board.get_moves(), best)

