# Andrew Edwards -- almostimplemented.com
# =======================================
# A checkers agent class.
#
# Last updated: July 21, 2014


class CheckersAgent:
    def __init__(self, player, board, moveFunction):
        if player not in [RED, BLUE]:
            raise ValueError
        self.player = player
        self.board = board
        self.moveFunction = moveFunction

    def doMove(self):
        return self.moveFunction(self.board)

