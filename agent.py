# Andrew Edwards -- almostimplemented.com
# =======================================
# A checkers agent class.
#
# Last updated: July 21, 2014


class CheckersAgent:
    def __init__(self, move_function):
        self.move_function = move_function

    def make_move(self, board):
        return self.move_function(board)
