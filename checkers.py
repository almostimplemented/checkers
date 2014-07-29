"""
    This module defines the CheckerBoard class.
"""
# Andrew Edwards -- almostimplemented.com
# =======================================
# A simple and efficient checkers class.
#
# Last updated: July 21, 2014

from copy import deepcopy

# Constants for board positions
EMPTY, RED, RED_KING, BLUE, BLUE_KING = range(5)

class CheckerBoard:
    """
        Represents a checker board. Holds state data and legal moves.
    """

    def __init__(self):
        """
            Initiates board via newGame().
        """
        self.new_game()

    def new_game(self):
        """
            Changes current state to new game state.
        """
        self.current_player = RED
        self.mandatory_jumps = None
        self.state = [ [BLUE, EMPTY] * 4, \
                       [EMPTY, BLUE] * 4, \
                       [BLUE, EMPTY] * 4, \
                       [EMPTY, EMPTY] * 4, \
                       [EMPTY, EMPTY] * 4, \
                       [EMPTY, RED] * 4, \
                       [RED, EMPTY] * 4, \
                       [EMPTY, RED] * 4 ]

    def piece_at(self, row, col):
        try:
            return self.state[row][col]
        except IndexError:
            return -1

    def make_move(self, move):
        """
            Assumes move = (row_old, col_old, row_new, col_new)

            Make the move from (row_old, col_old) to (row_new, col_new).
            Assumes the move is legal. If the move is a jump, the jumped
            piece is removed from the board. If (row_new, col_new) is the
            last row on the opponent's side, the piece is kinged.
        """
        row_old, col_old, row_new, col_new = move
        self.state[row_new][col_new] = self.state[row_old][col_old]
        self.state[row_old][col_old] = EMPTY

        if abs(row_old - row_new) == 2:
            row_jumped = (row_old + row_new) / 2
            col_jumped = (col_old + col_new) / 2

            self.state[row_jumped][col_jumped] = EMPTY

            self.mandatory_jumps = self.jumps_from_spot(self.current_player, row_new, col_new)
            if self.mandatory_jumps:
                return

        if row_new == 0 and self.state[row_new][col_new] == RED:
            self.state[row_new][col_new] = RED_KING
        if row_new == 7 and self.state[row_new][col_new] == BLUE:
            self.state[row_new][col_new] = BLUE_KING

        if self.current_player == RED:
            self.current_player = BLUE
        else:
            self.current_player = RED

    def peek_move(self, move):
        """
            Assumes move = (row_old, col_old, row_new, col_new)

            Return a new CheckerBoard object reflecting the change in
            the game state resulting from move.
        """
        future_board = deepcopy(self)
        future_board.make_move(move)
        return future_board

    def get_legal_moves(self, player):
        """
            Returns list of all legal moves that player can make.
            If player can jump, he must, so only jumps are returned.
        """
        if player != RED and player != BLUE:
            return None

        if self.mandatory_jumps:
            return self.mandatory_jumps

        legal_moves = [(row_old, col_old, row_old + i, col_old + j)
                        for row_old in range(8)
                        for col_old in range(8)
                        for i in (-2, 2)
                        for j in (-2, 2)
                          if self.piece_at(row_old, col_old) in [player, player + 1]
                         and self.can_jump(player, (row_old, col_old, row_old + i, col_old + j))]
        if len(legal_moves) != 0:
            return legal_moves

        legal_moves = [(row_old, col_old, row_old + i, col_old + j)
                        for row_old in range(8)
                        for col_old in range(8)
                        for i in (-1, 1)
                        for j in (-1, 1)
                          if self.piece_at(row_old, col_old) in [player, player + 1]
                         and self.can_move(player, (row_old, col_old, row_old + i, col_old + j))]

        if len(legal_moves) == 0:
            return None
        return legal_moves


    def can_jump(self, player, move):
        """
            Boolean function to determine of the player, move pair is legal.
            Has precondition that the move is of the form:
                        (x, y, x +/- 2, y +/- 2)
        """
        row_old, col_old, row_new, col_new = move

        row_jumped = (row_old + row_new) / 2
        col_jumped = (col_old + col_new) / 2

        if row_new < 0 or row_new > 7 or col_new < 0 or col_new > 7:
            return False

        if self.piece_at(row_new, col_new) != EMPTY:
            return False

        if player == RED:
            if self.piece_at(row_old, col_old) == RED and row_new > row_old:
                return False
            if self.piece_at(row_jumped, col_jumped) != BLUE and \
               self.piece_at(row_jumped, col_jumped) != BLUE_KING:
                return False
            return True

        if player == BLUE:
            if self.piece_at(row_old, col_old) == BLUE and row_new < row_old:
                return False
            if self.piece_at(row_jumped, col_jumped) != RED and \
               self.piece_at(row_jumped, col_jumped) != RED_KING:
                return False
            return True

    def jumps_from_spot(self, player, row, col):
        jumps = [(row, col, row + i, col + j) for i in (-2, 2) for j in (-2, 2)
                     if self.can_jump(player, (row, col, row + i, col + j))]
        return jumps if jumps else None

    def can_move(self, player, move):
        """
            Boolean function to determine of the player, move pair is legal.
            Has precondition that the move is of the form:
                        (x, y, x +/- 1, y +/- 1)
        """
        row_old, col_old, row_new, col_new = move

        if row_new < 0 or row_new > 7 or col_new < 0 or col_new > 7:
            return False

        if self.piece_at(row_new, col_new) != EMPTY:
            return False

        if player == RED:
            if self.piece_at(row_old, col_old) == RED and row_new > row_old:
                return False
            return True

        if player == BLUE:
            if self.piece_at(row_old, col_old) == BLUE and row_new < row_old:
                return False
            return True

    def game_over(self, player):
        return self.get_legal_moves(player) == None

    def __str__(self):
        """
            Prints out ASCII art representation of board.
            Uses ANSI color codes. If not compatible with your configurations,
            set color constants at top of module to null strings.
        """
        # Constants for coloring the board
        FORE_RED = '\033[31m\033[1m'
        FORE_BLUE = '\033[34m\033[1m'
        DEF_FONT = '\033[39m\033[22m'

        board = [None] * 17
        for i in range(9):
            board[2*i] = ["+", " - "] + ["+", " - "]*7 + ["+", "\n"]
            if i < 8:
              board[2*i + 1] = ["|", "   "] \
                             + [a for subl in [["|", "   "] for _ in range(7)] for a in subl] \
                             + ["|", "\n"]

        # Flesh out board with pieces
        i = 0
        for row in self.state:
            j = 0
            for cell in row:
                if cell == RED:
                    board[2*i+1][2*j+1] = FORE_RED + str(i) + 'r' + str(j) + DEF_FONT
                elif cell == RED_KING:
                    board[2*i+1][2*j+1] = FORE_RED + str(i) + 'R' + str(j) + DEF_FONT
                elif cell == BLUE:
                    board[2*i+1][2*j+1] = FORE_BLUE + str(i) + 'b' + str(j) + DEF_FONT
                elif cell == BLUE_KING:
                    board[2*i+1][2*j+1] = FORE_BLUE + str(i) + 'B' + str(j) + DEF_FONT
                elif (i + j) % 2 == 0:
                    board[2*i+1][2*j+1] = str(i) + "," + str(j)
                j += 1
            i += 1

        return "".join(map(lambda x: "".join(x), board))

# end of CheckerBoard class


