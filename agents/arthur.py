# Andrew Edwards -- almostimplemented.com
# =======================================
# A checkers agent implementaiton based
# on Arthur Samuel's historic program.
#
# Last updated: July 21, 2014

def moveFunction(board):
    legal_moves = board.get_legal_moves(board.current_player)
    return legal_moves[0]
