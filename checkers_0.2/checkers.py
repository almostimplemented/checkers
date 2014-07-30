"""
    This module defines the CheckerBoard class.
"""
# Andrew Edwards -- almostimplemented.com
# =======================================
# A simple and efficient checker board class.
#
# Created July 29, 2014

### CONSTANTS

# Black moves "forward", white moves "backward"
BLACK, WHITE = 0, 1

# The IBM704 had 36-bit words. Arthur Samuel used the extra bits to
# ensure that every normal move could be performed by flipping the
# original bit and the bit either 4 or 5 bits away, in the cases of
# moving right and left respectively.
#
# If we use a 32-bit word, we need to know which row our piece is in
# in order to tell whether the "right forward" move is 4 or
UNUSED_BITS = int('0b100000000100000000100000000100000000', 2)

### CLASSES

class CheckerBoard:
    def __init__(self):
        """
            Initiates board via new_game().
        """
        self.forward = [None, None]
        self.backward = [None, None]
        self.pieces = [None, None]
        self.new_game()

    def new_game(self):
        """
            Resets current state to new game.
        """
        self.active = BLACK
        self.passive = WHITE

        self.forward[BLACK] = 0x1eff
        self.backward[BLACK] = 0
        self.pieces[BLACK] = self.forward[BLACK] | self.backward[BLACK]

        self.forward[WHITE] = 0
        self.backward[WHITE] = 0x7fbc00000
        self.pieces[WHITE] = self.forward[WHITE] | self.backward[WHITE]

        self.empty = UNUSED_BITS ^ (2**36 - 1) ^ (self.pieces[BLACK] | self.pieces[WHITE])

    def make_move(self, move):
        """
            Updates the game state to reflect the effects of the input
            move.

            A legal move is represented by an integer with exactly two
            bits turned on: the old position and the new position.
        """
        active = self.active
        passive = self.passive
        if move < 0:
            taken_piece = int(1 << sum(i for (i, b) in enumerate(bin(move)[::-1]) if b == '1')/2)
            self.pieces[passive] ^= taken_piece
            if self.forward[passive] & taken_piece:
                self.forward[passve] ^= taken_piece
            if self.backward[passive] & taken_piece:
                self.backward[passive] ^= taken_piece

        self.pieces[active] ^= move
        if self.forward[active] & move:
            self.forward[active] ^= move
        if self.backward[active] & move:
            self.backward[active] ^= move

        self.active, self.passive = self.passive, self.active
        self.empty = UNUSED_BITS ^ (2**36 - 1) ^ (self.pieces[BLACK] | self.pieces[WHITE])

    # These methods return an integer whose active bits are those squares
    # that can make the move indicated by the method name.
    def right_forward(self):
        return (self.empty >> 4) & self.forward[self.active]
    def left_forward(self):
        return (self.empty >> 5) & self.forward[self.active]
    def right_backward(self):
        return (self.empty << 4) & self.backward[self.active]
    def left_backward(self):
        return (self.empty << 5) & self.backward[self.active]
    def right_forward_jumps(self):
        return (self.empty >> 8) & (self.pieces[self.passive] >> 4) & self.forward[self.active]
    def left_forward_jumps(self):
        return (self.empty >> 10) & (self.pieces[self.passive] >> 5) & self.forward[self.active]
    def right_backward_jumps(self):
        return (self.empty << 8) & (self.pieces[self.passive] << 4) & self.backward[self.active]
    def left_backward_jumps(self):
        return (self.empty << 10) & (self.pieces[self.passive] << 5) & self.backward[self.active]

    def get_moves(self):
        """
            Returns a list of all possible moves.

            A legal move is represented by an integer with exactly two
            bits turned on: the old position and the new position.

            Jumps are indicated with a negative sign.
        """
        # First check if there are jumps
        rfj = self.right_forward_jumps()
        lfj = self.left_forward_jumps()
        rbj = self.right_backward_jumps()
        lbj = self.left_backward_jumps()

        if (rfj | lfj | rbj | lbj) != 0:
            moves =  [-0x101 << i for (i, bit) in enumerate(bin(rfj)[::-1]) if bit == '1']
            moves += [-0x401 << i for (i, bit) in enumerate(bin(lfj)[::-1]) if bit == '1']
            moves += [-0x101 << i - 4 for (i, bit) in enumerate(bin(rbj)[::-1]) if bit == '1']
            moves += [-0x401 << i - 5 i for (i, bit) in enumerate(bin(lbj)[::-1]) if bit == '1']
            return moves

        # If not, then find normal moves
        else:
            rf = self.right_forward()
            lf = self.left_forward()
            rb = self.right_backward()
            lb = self.left_backward()

            moves =  [0x11 << i for (i, bit) in enumerate(bin(rf)[::-1]) if bit == '1']
            moves += [0x21 << i for (i, bit) in enumerate(bin(lf)[::-1]) if bit == '1']
            moves += [0x11 << i - 4 for (i, bit) in enumerate(bin(rb)[::-1]) if bit == '1']
            moves += [0x21 << i - 5 for (i, bit) in enumerate(bin(lb)[::-1]) if bit == '1']
            return moves

    def __str__(self):
        """
            Prints out ASCII art representation of board.
            Uses ANSI color codes. If not compatible with your configurations,
            set color constants at top of module to null strings.
        """

        EMPTY = -1
        BLACK_KING = 2
        WHITE_KING = 3

        if self.active == BLACK:
            black_kings = self.backward[self.active]
            black_men = self.forward[self.active] ^ black_kings
            white_kings = self.forward[self.passive]
            white_men = self.backward[self.passive] ^ white_kings
        else:
            black_kings = self.backward[self.passive]
            black_men = self.forward[self.passive] ^ black_kings
            white_kings = self.forward[self.active]
            white_men = self.backward[self.active] ^ white_kings

        state = [[None for _ in range(8)] for _ in range(4)]
        for i in range(4):
            for j in range(8):
                cell = 1 << (9*i + j)
                if cell & black_men:
                    state[i][j] = BLACK
                elif cell & white_men:
                    state[i][j] = WHITE
                elif cell & black_kings:
                    state[i][j] = BLACK_KING
                elif cell & white_kings:
                    state[i][j] = WHITE_KING
                else:
                    state[i][j] = EMPTY

        board = [None] * 17
        for i in range(9):
            board[2*i] = ["+", " - "] + ["+", " - "]*7 + ["+", "\n"]
            if i < 8:
              board[2*i + 1] = ["|", "   "] \
                             + [a for subl in [["|", "   "] for _ in range(7)] for a in subl] \
                             + ["|", "\n"]

        for i, chunk in enumerate(state):
            for j, cell in enumerate(chunk):
                if j < 4:
                    if cell == BLACK:
                        board[2*(7 - 2*i) + 1][2*(6 - 2*j) + 1] = \
                                "b" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    elif cell == WHITE:
                        board[2*(7 - 2*i) + 1][2*(6 - 2*j) + 1] = \
                                "w" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    elif cell == BLACK_KING:
                        board[2*(7 - 2*i) + 1][2*(6 - 2*j) + 1] = \
                                "B" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    elif cell == WHITE_KING:
                        board[2*(7 - 2*i) + 1][2*(6 - 2*j) + 1] = \
                                "W" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                else:
                    if cell == BLACK:
                        board[2*(6 - 2*i) + 1][2*(7 - 2*j) - 1] = \
                                "b" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    elif cell == WHITE:
                        board[2*(6 - 2*i) + 1][2*(7 - 2*j) - 1] = \
                                "w" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    elif cell == BLACK_KING:
                        board[2*(6 - 2*i) + 1][2*(7 - 2*j) - 1] = \
                                "B" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    elif cell == WHITE_KING:
                        board[2*(6 - 2*i) + 1][2*(7 - 2*j) - 1] = \
                                "W" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')

        return "".join(map(lambda x: "".join(x), board))
