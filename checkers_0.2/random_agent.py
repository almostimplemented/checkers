# Andrew Edwards -- almostimplemented.com
# =======================================
# A checkers agent that picks a random move
#
# Last updated: July 21, 2014
import random

def move_function(board):
    return random.choice(board.get_moves())
