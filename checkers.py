# Andrew Edwards -- almostimplemented.com
# =======================================
# A simple and efficient checkers class.
#
# Last updated: July 21, 2014

# Constants for colors and board positions
FORE_RED = '\033[31m\033[1m'
FORE_BLUE = '\033[34m\033[1m'
DEF_FONT = '\033[39m\033[22m'
EMPTY, RED, RED_KING, BLUE, BLUE_KING = range(5)

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
        self.state = [ [BLUE, EMPTY] * 4, \
                       [EMPTY, BLUE] * 4, \
                       [BLUE, EMPTY] * 4, \
                       [EMPTY, EMPTY] * 4, \
                       [EMPTY, EMPTY] * 4, \
                       [EMPTY, RED] * 4, \
                       [RED, EMPTY] * 4, \
                       [EMPTY, RED] * 4 ]

    def pieceAt(self, row, column):
        """
            Returns the cell contents at (row, column).
        """
        return self.state[row][column]

    def makeMove(self, move):
        """
            Assumes move = (rowOld, colOld, rowNew, colNew)

            Make the move from (rowOld, colOld) to (rowNew, colNew).
            Assumes the move is legal. If the move is a jump, the jumped
            piece is removed from the board. If (rowNew, colNew) is the
            last row on the opponent's side, the piece is kinged.
        """
        rowOld, colOld, rowNew, colNew = move
        self.state[rowNew][colNew] = self.state[rowOld][colOld]
        self.state[rowOld][colOld] = EMPTY

        if abs(rowOld - rowNew) == 2:
            rowJumped = (rowOld + rowNew) / 2
            colJumped = (colOld + colNew) / 2

            self.state[rowJumped][colJumped] = EMPTY

        if rowNew == 0 and self.state[rowNew][colNew] == RED:
            self.state[rowNew][colNew] = RED_KING
        if rowNew == 7 and self.state[rowNew][colNew] == BLUE:
            self.state[rowNew][colNew] = BLUE_KING

    def peekMove(self, move):
        """
            Assumes move = (rowOld, colOld, rowNew, colNew)

            Return a 2D integer array representing the change
            in game state resulting from move.
        """
        rowOld, colOld, rowNew, colNew = move
        futureState = [[c for c in x] for x in self.state]
        futureState[rowNew][colNew] = futureState[rowOld][colOld]
        futureState[rowOld][colOld] = EMPTY

        if abs(rowOld - rowNew) == 2:
            rowJumped = (rowOld + rowNew) / 2
            colJumped = (colOld + colNew) / 2

            futureState[rowJumped][colJumped] = EMPTY

        if rowNew == 0 and futureState[rowNew][colNew] == RED:
            futureState[rowNew][colNew] = RED_KING
        if rowNew == 7 and futureState[rowNew][colNew] == BLUE:
            futureState[rowNew][colNew] = BLUE_KING

        return futureState

    def getLegalMoves(self, player):
        """
            Returns list of all legal moves that player can make.
            If player can jump, he must, so only jumps are returned.
        """
        if player != RED and player != BLUE:
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

        if player == RED:
            if self.state[rowOld][colOld] == RED and rowNew > rowOld:
                return False
            if self.state[rowJumped][colJumped] != BLUE and \
               self.state[rowJumped][colJumped] != BLUE_KING:
                return False
            return True

        if player == BLUE:
            if self.state[rowOld][colOld] == BLUE and rowNew > rowOld:
                return False
            if self.state[rowJumped][colJumped] != RED and \
               self.state[rowJumped][colJumped] != RED_KING:
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

        if player == RED:
            if self.state[rowOld][rowNew] == RED and rowNew > rowOld:
                return False
            return True

        if player == BLUE:
            if self.state[rowOld][colOld] == BLUE and rowNew < rowOld:
                return False
            return True

    def __str__(self):
        """
            Prints out ASCII art representation of board.
            Uses ANSI color codes. If not compatible with your configurations,
            set color constants at top of module to null strings.
        """
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
                    board[2*i+1][2*j+1] = FORE_RED + ' r ' + DEF_FONT
                elif cell == RED_KING:
                    board[2*i+1][2*j+1] = FORE_RED + ' R ' + DEF_FONT
                elif cell == BLUE:
                    board[2*i+1][2*j+1] = FORE_BLUE + ' b ' + DEF_FONT
                elif cell == BLUE_KING:
                    board[2*i+1][2*j+1] = FORE_BLUE + ' B ' + DEF_FONT
                j += 1
            i += 1

        return "".join(map(lambda x: "".join(x), board))



# Exo-class functions
def printBoard(state):
    """
        Prints out ASCII art representation of board.
        Uses ANSI color codes. If not compatible with your configurations,
        set color constants at top of module to null strings.
    """
    board = [None] * 17
    for i in range(9):
        board[2*i] = ["+", " - "] + ["+", " - "]*7 + ["+", "\n"]
        if i < 8:
          board[2*i + 1] = ["|", "   "] \
                         + [a for subl in [["|", "   "] for _ in range(7)] for a in subl] \
                         + ["|", "\n"]

    # Flesh out board with pieces
    i = 0
    for row in state:
        j = 0
        for cell in row:
            if cell == RED:
                board[2*i+1][2*j+1] = FORE_RED + ' r ' + DEF_FONT
            elif cell == RED_KING:
                board[2*i+1][2*j+1] = FORE_RED + ' R ' + DEF_FONT
            elif cell == BLUE:
                board[2*i+1][2*j+1] = FORE_BLUE + ' b ' + DEF_FONT
            elif cell == BLUE_KING:
                board[2*i+1][2*j+1] = FORE_BLUE + ' B ' + DEF_FONT
            j += 1
        i += 1

    print "".join(map(lambda x: "".join(x), board))
