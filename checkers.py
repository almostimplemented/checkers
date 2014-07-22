# Andrew Edwards -- almostimplemented.com
# =======================================
# A simple and efficient checkers class.
#
# Last updated: July 21, 2014

# Constants for board positions
EMPTY, WHITE, WHITE_KING, BLACK, BLACK_KING = range(5)

class CheckerBoard:
    """
        Represents a checker board. Holds state data and legal moves.
    """

    def __init__(self):
        """
            Initiates board via newGame().
        """
        self.newGame()

    def newGame(self):
        """
            Changes current state to new game state.
        """
        self.state = [ [BLACK, EMPTY] * 4, \
                       [EMPTY, BLACK] * 4, \
                       [BLACK, EMPTY] * 4, \
                       [EMPTY, EMPTY] * 4, \
                       [EMPTY, EMPTY] * 4, \
                       [EMPTY, WHITE] * 4, \
                       [WHITE, EMPTY] * 4, \
                       [EMPTY, WHITE] * 4 ]

    def pieceAt(self, row, column):
        """
            Returns the cell contents at (row, column).
        """
        return self.state[row][column]

    def makeMove(self, rowOld, colOld, rowNew, colNew):
        """
            Make the move from (rowOld, colOld) to (rowNew, colNew).
            Assumes the move is legal. If the move is a jump, the jumped
            piece is removed from the board. If (rowNew, colNew) is the
            last row on the opponent's side, the piece is kinged.
        """
        self.state[rowNew][colNew] = self.state[rowOld][colOld]
        self.state[rowOld][colOld] = EMPTY

        if abs(rowOld - rowNew) == 2:
            rowJumped = (rowOld + rowNew) / 2
            colJumped = (colOld + colNew) / 2

            self.state[rowJumped][colJumped] = EMPTY

        if rowNew == 0 and self.state[rowNew][colNew] == WHITE:
            self.state[rowNew][colNew] = WHITE_KING
        if rowNew == 7 and self.state[rowNew][colNew] == BLACK:
            self.state[rowNew][colNew] = BLACK_KING

    def getLegalMoves(self, player):
        """
            Returns list of all legal moves that player can make.
            If player can jump, he must, so only jumps are returned.
        """
        if player != WHITE and player != BLACK:
            return None

        legalMoves = [(rowOld, colOld, rowOld + i, colOld + j) \
                        for rowOld in range(8)          \
                        for colOld in range(8)          \
                        for i in (-2, 2)                \
                        for j in (-2, 2)                \
                            if self.state[rowOld][colOld] == [player, player + 1] \
                            and self.canJump(player, (rowOld, colOld, rowOld + i, colOld + j))]

        if len(legalMoves) != 0:
            return legalMoves

        legalMoves = [(rowOld, colOld, rowOld + i, colOld + j) \
                        for rowOld in range(8)          \
                        for colOld in range(8)          \
                        for i in (-1, 1)                \
                        for j in (-1, 1)                \
                            if self.state[rowOld][colOld] in [player, player + 1] \
                            and self.canMove(player, (rowOld, colOld, rowOld + i, colOld + j))]

        if len(legalMoves) == 0:
            return None
        return legalMoves


    def canJump(self, player, move):
        """
            Boolean function to determine of the player, move pair is legal.
            Has precondition that the move is of the form:
                        (x, y, x +/- 2, y +/- 2)
        """
        (rowOld, colOld, rowNew, colNew) = move

        rowJumped = (rowOld + rowNew) / 2
        colJumped = (colOld + colNew) / 2

        if rowNew < 0 or rowNew > 7 or colNew < 0 or colNew > 7:
            return False

        if self.state[rowNew][colNew] != EMPTY:
            return False

        if player == WHITE:
            if self.state[rowOld][colOld] == WHITE and rowNew > rowOld:
                return False
            if self.state[rowJumped][colJumped] != BLACK and \
               self.state[rowJumped][colJumped] != BLACK_KING:
                return False
            return True

        if player == BLACK:
            if self.state[rowOld][colOld] == BLACK and rowNew > rowOld:
                return False
            if self.state[rowJumped][colJumped] != WHITE and \
               self.state[rowJumped][colJumped] != WHITE_KING:
                return False
            return True

    def canMove(self, player, move):
        """
            Boolean function to determine of the player, move pair is legal.
            Has precondition that the move is of the form:
                        (x, y, x +/- 1, y +/- 1)
        """
        (rowOld, colOld, rowNew, colNew) = move

        if rowNew < 0 or rowNew > 7 or colNew < 0 or colNew > 7:
            return False

        if self.state[rowNew][colNew] != EMPTY:
            return False

        if player == WHITE:
            if self.state[rowOld][rowNew] == WHITE and rowNew > rowOld:
                return False
            return True

        if player == BLACK:
            if self.state[rowOld][colOld] == BLACK and rowNew > rowOld:
                return False
            return True
