# Andrew Edwards -- almostimplemented.com
# =======================================
# A checkers agent implementaiton based
# on Arthur Samuel's historic program.
#
# Last updated: July 21, 2014

from utils import *

# Constants
BLACK, WHITE = 0, 1
VALID_SQUARES = 0x7FBFDFEFF

# Feature functions
def adv(board): # Advancement
    """
        The parameter is credited with 1 for each passive man in the
        fifth and sixth rows (counting in passive's direction) and
        debited with 1 for each passive man in the third and fourth
        rows.
    """
    passive = board.passive

    rows_3_and_4 =   0x1FE00
    rows_5_and_6 = 0x3FC0000
    if passive == WHITE:
        rows_3_and_4, rows_5_and_6 = rows_5_and_6, rows_3_and_4

    bits_3_and_4 = rows_3_and_4 & board.pieces[passive]
    bits_5_and_6 = rows_5_and_6 & board.pieces[passive]
    return bin(bits_5_and_6).count("1") - bin(bits_3_and_4).count("1")

def back(board): # Back Row Bridge
    """
        The parameter is credited with 1 if there are no active kings
        on the board and if the two bridge squares (1 and 3, or 30 and
        32) in the back row are occupied by passive pieces.
    """
    active = board.active
    passive = board.passive
    if active == BLACK:
        if board.backward[BLACK] != 0:
            return 0
        back_row_bridge = 0x480000000
    else:
        if board.forward[WHITE] != 0:
            return 0
        back_row_bridge = 0x5

    if bin(back_row_bridge & board.pieces[passive]).count('1') == 2:
        return 1
    return 0

def cent(board): # Center Control I
    """
        The parameter is credited with 1 for each of the following
        squares: 11, 12, 15, 16, 20, 21, 24, 25 which is occupied by
        a passive man.
    """
    passive = board.passive
    if passive == WHITE:
        center_pieces = 0xA619800
    else:
        center_pieces = 0xCC3280

    return bin(board.pieces[passive] & center_pieces).count("1")

def cntr(board): # Center Control II
    """
        The parameter is credited with 1 for each of the following
        squares: 11, 12, 15, 16, 20, 21, 24, 25 that is either
        currently occupied by an active piece or to which an active
        piece can move.
    """
    active = board.active
    if active == BLACK:
        center_pieces = 0xA619800
    else:
        center_pieces = 0xCC3280

    active_center_count = bin(board.pieces[active] & center_pieces).count("1")

    moves = board.get_moves()
    if moves[0] < 0:
        moves = map(lambda x: x*(-1), moves)
    destinations = reduce(lambda x, y: x|y,
                          [(m & (m ^ board.pieces[active])) for m in moves])

    active_near_center_count = bin(destinations & center_pieces).count("1")

    return active_center_count + active_near_center_count

def deny(board): # Denial of Occupancy
    """
        The parameter is credited 1 for each square defined in MOB if
        on the next move a piece occupying this square could be
        captured without exchange.
    """
    rf = board.right_forward()
    lf = board.left_forward()
    rb = board.right_backward()
    lb = board.left_backward()

    moves =  [0x11 << i for (i, bit) in enumerate(bin(rf)[::-1]) if bit == '1']
    moves += [0x21 << i for (i, bit) in enumerate(bin(lf)[::-1]) if bit == '1']
    moves += [0x11 << i - 4 for (i, bit) in enumerate(bin(rb)[::-1]) if bit == '1']
    moves += [0x21 << i - 5 for (i, bit) in enumerate(bin(lb)[::-1]) if bit == '1']

    destinations =  [0x10 << i for (i, bit) in enumerate(bin(rf)[::-1]) if bit == '1']
    destinations += [0x20 << i for (i, bit) in enumerate(bin(lf)[::-1]) if bit == '1']
    destinations += [0x1 << i - 4 for (i, bit) in enumerate(bin(rb)[::-1]) if bit == '1']
    destinations += [0x1 << i - 5 for (i, bit) in enumerate(bin(lb)[::-1]) if bit == '1']

    denials = []

    for move, dest in zip(moves, destinations):
        B = board.peek_move(move)
        active = B.active
        ms_taking = []
        ds = []
        if (B.forward[active] & (dest >> 4)) != 0 and (B.empty & (dest << 4)) != 0:
            ms_taking.append((-1)*((dest >> 4) | (dest << 4)))
            ds.append(dest << 4)
        if (B.forward[active] & (dest >> 5)) != 0 and (B.empty & (dest << 5)) != 0:
            ms_taking.append((-1)*((dest >> 5) | (dest << 5)))
            ds.append(dest << 5)
        if (B.backward[active] & (dest << 4)) != 0 and (B.empty & (dest >> 4)) != 0:
            ms_taking.append((-1)*((dest << 4) | (dest >> 4)))
            ds.append(dest >> 4)
        if (B.backward[active] & (dest << 5)) != 0 and (B.empty & (dest >> 5)) != 0:
            ms_taking.append((-1)*((dest << 5) | (dest >> 5)))
            ds.append(dest >> 5)

        if not ms_taking:
            continue
        else:
            for m, d in zip(ms_taking, ds):
                C = B.peek_move(m)
                if C.active == active:
                    if not dest in denials:
                        denials.append(dest)
                    continue
                if not C.takeable(d):
                    if not dest in denials:
                        denials.append(dest)

    return len(denials)


def kcent(board): # King Center Control
    """
        The parameter is credited with 1 for each of the following
        squares: 11, 12, 15, 16, 20, 21, 24, and 25 which is occupied
        by a passive king.
    """
    passive = board.passive
    if passive == WHITE:
        center_pieces = 0xA619800
        passive_kings = board.forward[WHITE]
    else:
        center_pieces = 0xCC3280
        passive_kings = board.backward[BLACK]

    return bin(passive_kings & center_pieces).count("1")


def mob(board): # Total Mobility
    """
        The parameter is credited with 1 for each square to which the
        active side could move one or more pieces in the normal fashion
        disregarding the fact that jump moves may or may not be
        available.
    """
    rf = board.right_forward()
    lf = board.left_forward()
    rb = board.right_backward()
    lb = board.left_backward()

    destinations =  [0x10 << i for (i, bit) in enumerate(bin(rf)[::-1]) if bit == '1']
    destinations += [0x20 << i for (i, bit) in enumerate(bin(lf)[::-1]) if bit == '1']
    destinations += [0x1 << i - 4 for (i, bit) in enumerate(bin(rb)[::-1]) if bit == '1']
    destinations += [0x1 << i - 5 for (i, bit) in enumerate(bin(lb)[::-1]) if bit == '1']

    return bin(reduce(lambda x, y: x|y, destinations)).count("1")

def mobil(board): # Undenied Mobility
    """
        The parameter is credited with the difference between MOB and
        DENY.
    """
    return mob(board) - deny(board)

def move(board): # Move
    """
        The parameter is credited with 1 if pieces are even with a
        total piece count (2 for men, and 3 for kings) of less than 24,
        and if an odd number of pieces are in the move system, defined
        as those vertical files starting with squares 1, 2, 3, and 4.
    """
    black_men = bin(board.forward[BLACK]).count("1")
    black_kings = bin(board.backward[BLACK]).count("1")
    black_score = 2*black_men + 3*black_kings
    white_men = bin(board.backward[WHITE]).count("1")
    white_kings = bin(board.forward[WHITE]).count("1")
    white_score = 2*white_men + 3*white_kings

    if white_score < 24 and black_score == white_score:
        pieces = board.pieces[BLACK] | board.pieces[WHITE]
        if board.active == BLACK:
            move_system =  0x783c1e0f
        else:
            move_system = 0x783c1e0f0
        if bin(move_system & pieces).count("1") % 2 == 1:
            return 1

    return 0

def thret(board): # Threat
    """
        The parameter is credited with 1 for each square to which an
        active piece may be moved and in doing so threaten to capture
        a passive piece on a subsequent move.
    """
    moves = board.get_moves()
    destinations = map(lambda x: (x ^ board.pieces[board.active]) & x, moves)
    origins = [x ^ y for (x, y) in zip(moves, destinations)]

    jumps = []
    for dest, orig in zip(destinations, origins):
        if board.active == BLACK:
            rfj = (board.empty >> 8) & (board.pieces[board.passive] >> 4) & dest
            lfj = (board.empty >> 10) & (board.pieces[board.passive] >> 5) & dest
            if orig & board.backward[board.active]: # piece is king
                rbj = (board.empty << 8) & (board.pieces[board.passive] << 4) & dest
                lbj = (board.empty << 10) & (board.pieces[board.passive] << 5) & dest
            else:
                rbj = 0
                lbj = 0
        else:
            rbj = (board.empty << 8) & (board.pieces[board.passive] << 4) & dest
            lbj = (board.empty << 10) & (board.pieces[board.passive] << 5) & dest
            if dest & board.forward[board.active]: # piece at square is a king
                rfj = (board.empty >> 8) & (board.pieces[board.passive] >> 4) & dest
                lfj = (board.empty >> 10) & (board.pieces[board.passive] >> 5) & dest
            else:
                rfj = 0
                lfj = 0

        if (rfj | lfj | rbj | lbj) != 0:
            jumps += [-0x101 << i for (i, bit) in enumerate(bin(rfj)[::-1]) if bit == '1']
            jumps += [-0x401 << i for (i, bit) in enumerate(bin(lfj)[::-1]) if bit == '1']
            jumps += [-0x101 << i - 8 for (i, bit) in enumerate(bin(rbj)[::-1]) if bit == '1']
            jumps += [-0x401 << i - 10 for (i, bit) in enumerate(bin(lbj)[::-1]) if bit == '1']

    return len(jumps)

def score(board):
    _adv = adv(board)
    _back = back(board)
    _cent = cent(board)
    _cntr = cntr(board)
    _deny = deny(board)
    _kcent = kcent(board)
    _mob = mob(board)
    _mobil = _mob - _deny
    _move = move(board)
    _thret = thret(board)

    undenied_mobility = 1 if _mobil >= 3 else 0
    total_mobility = 1 if _mob >= 6 else 0
    denial_of_occ = 1 if _deny >= 3 else 0
    _demmo = 1 if denial_of_occ and not total_mobility else 0
    _mode_2 = 1 if undenied_mobility and not denial_of_occ else 0
    _mode_3 = 1 if not undenied_mobility and denial_of_occ else 0
    control = 1 if _cent >= 4 else 0
    _moc_2 = 1 if not undenied_mobility and control else 0
    _moc_3 = 1 if undenied_mobility and not control else 0
    _moc_4 = 1 if not undenied_mobility and not control else 0

    board_score = _moc_2*(-1)*(2**18)  \
                + _kcent*(2**16)       \
                + _moc_4*(-1)*(2**14)  \
                + _mode_3*(-1)*(2**13) \
                + _demmo*(-1)*(2**11)  \
                + _move*(2**8)         \
                + _adv*(-1)*(2**8)     \
                + _mode_2*(-1)*(2**8)  \
                + _back*(-1)*(2**6)    \
                + _cntr*(2**5)         \
                + _thret*(2**5)        \
                + _moc_3*(2**4)

    return board_score



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


if __name__ == '__main__':
    import checkers
    B = checkers.CheckerBoard()
    for _ in range(10):
        B.make_move(B.get_moves()[0])
    for _ in range(4):
        print B
        print "Active player: " + ("white" if B.active else "black")
        print "adv(B): " + str(adv(B))
        print "back(B): " + str(back(B))
        print "cent(B): " + str(cent(B))
        print "cntr(B): " + str(cntr(B))
        print "deny(B): " + str(deny(B))
        print "kcent(B): " + str(kcent(B))
        print "mob(B): " + str(mob(B))
        print "mobil(B): " + str(mobil(B))
        print "move(B): " + str(move(B))
        print "thret(B): " + str(thret(B))
        print ""
        B.make_move(B.get_moves()[0])
