# Andrew Edwards -- almostimplemented.com
# =======================================
# A checkers agent implementaiton based
# on Arthur Samuel's historic program.
#
# Last updated: July 21, 2014

import sys

# Constants
BLACK, WHITE = 0, 1
VALID_SQUARES = 0x7FBFDFEFF

INFINITY = sys.maxsize

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

    if not destinations:
        return 0
    return bin(reduce(lambda x, y: x|y, destinations)).count("1")

def mobil(board): # Undenied Mobility
    """
        The parameter is credited with the difference between MOB and
        DENY.
    """
    return mob(board) - deny(board)

def mov(board): # Move
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

def piece_score_diff(board, player):
    black_men = bin(board.forward[BLACK]).count("1")
    black_kings = bin(board.backward[BLACK]).count("1")
    black_score = 2*black_men + 3*black_kings
    white_men = bin(board.backward[WHITE]).count("1")
    white_kings = bin(board.forward[WHITE]).count("1")
    white_score = 2*white_men + 3*white_kings

    return black_score - white_score if player == BLACK else white_score - black_score

def position_score(board, player):
    scores = [0x88000, 0x1904c00, 0x3A0502E0, 0x7C060301F]
    i = 1
    total = 0
    for s in scores:
        total = i*bin(board.pieces[player] & s).count("1")
        i += 1
    return total

def score(board_old, board_new):
    if board_old.is_over():
        return -INFINITY
    if board_new.is_over():
        return INFINITY
    _adv   = adv(board_new) - adv(board_old)
    _back  = adv(board_new) - back(board_old)
    _cent  = cent(board_new) - cent(board_old)
    _cntr  = cntr(board_new) - cntr(board_old)
    _deny  = deny(board_new) - deny(board_old)
    _kcent = kcent(board_new) - kcent(board_old)
    _mob   = mob(board_new) - mob(board_old)
    _mobil = _mob - _deny
    _mov   = mov(board_new) - mov(board_old)
    _thret = thret(board_new) - thret(board_old)

    undenied_mobility = 1 if _mobil > 0 else 0
    total_mobility = 1 if _mob > 0 else 0
    denial_of_occ = 1 if _deny > 0 else 0
    control = 1 if _cent > 0 else 0

    _demmo = 1 if denial_of_occ and not total_mobility else 0
    _mode_2 = 1 if undenied_mobility and not denial_of_occ else 0
    _mode_3 = 1 if not undenied_mobility and denial_of_occ else 0
    _moc_2 = 1 if not undenied_mobility and control else 0
    _moc_3 = 1 if undenied_mobility and not control else 0
    _moc_4 = 1 if not undenied_mobility and not control else 0

    board_score = _moc_2*(-1)*(2**18)  \
                + _kcent*(2**16)       \
                + _moc_4*(-1)*(2**14)  \
                + _mode_3*(-1)*(2**13) \
                + _demmo*(-1)*(2**11)  \
                + _mov*(2**8)          \
                + _adv*(-1)*(2**8)     \
                + _mode_2*(-1)*(2**8)  \
                + _back*(-1)*(2**6)    \
                + _cntr*(2**5)         \
                + _thret*(2**5)        \
                + _moc_3*(2**4)        \
                + piece_score_diff(board_new, board_old.active)*(2**20) \
                + position_score(board_new, board_old.active)*(2**14)

    return board_score

def negamax(board_old, board_new, depth, alpha, beta, color):
    if depth == 0 or board_new.is_over():
        return score(board_old, board_new)*color
    best_value = -INFINITY
    for move in board_new.get_moves():
        B = board_new.peek_move(move)
        if B.active != board_new.active:
            val = -negamax(board_new, B, depth - 1, -beta, -alpha, -color)
        else:
            val = negamax(board_new, B, depth, alpha, beta, color)
        best_value = max(best_value, val)
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return best_value

def move_function(board, depth=7):
    def search(move):
        B = board.peek_move(move)
        if B.active == board.active:
            return negamax(board, B, depth, -INFINITY, INFINITY, 1)
        else:
            return negamax(board, B, depth, -INFINITY, INFINITY, -1)

    return max(board.get_moves(), key=search)
    #pairs = zip(zip(board.get_moves(), get_move_strings(board)),
                #map(search, board.get_moves()))
    #print "Moves and ratings"
    #for pair in pairs:
        #print pair[0][1] + " with a rating of " + str(pair[1])
    #print ""
    #best_pair = max(pairs, key=lambda x: x[1])
    #return best_pair[0][0]

def get_move_strings(board):
    rfj = board.right_forward_jumps()
    lfj = board.left_forward_jumps()
    rbj = board.right_backward_jumps()
    lbj = board.left_backward_jumps()

    if (rfj | lfj | rbj | lbj) != 0:
        rfj = [(1 + i - i//9, 1 + (i + 8) - (i + 8)//9)
                    for (i, bit) in enumerate(bin(rfj)[::-1]) if bit == '1']
        lfj = [(1 + i - i//9, 1 + (i + 10) - (i + 8)//9)
                    for (i, bit) in enumerate(bin(lfj)[::-1]) if bit == '1']
        rbj = [(1 + i - i//9, 1 + (i - 8) - (i - 8)//9)
                    for (i, bit) in enumerate(bin(rbj)[::-1]) if bit ==  '1']
        lbj = [(1 + i - i//9, 1 + (i - 10) - (i - 10)//9)
                    for (i, bit) in enumerate(bin(lbj)[::-1]) if bit == '1']

        if board.active == BLACK:
            regular_moves = ["%i to %i" % (orig, dest) for (orig, dest) in rfj + lfj]
            reverse_moves = ["%i to %i" % (orig, dest) for (orig, dest) in rbj + lbj]
            return regular_moves + reverse_moves
        else:
            reverse_moves = ["%i to %i" % (orig, dest) for (orig, dest) in rfj + lfj]
            regular_moves = ["%i to %i" % (orig, dest) for (orig, dest) in rbj + lbj]
            return reverse_moves + regular_moves


    rf = board.right_forward()
    lf = board.left_forward()
    rb = board.right_backward()
    lb = board.left_backward()

    rf = [(1 + i - i//9, 1 + (i + 4) - (i + 4)//9)
                for (i, bit) in enumerate(bin(rf)[::-1]) if bit == '1']
    lf = [(1 + i - i//9, 1 + (i + 5) - (i + 5)//9)
                for (i, bit) in enumerate(bin(lf)[::-1]) if bit == '1']
    rb = [(1 + i - i//9, 1 + (i - 4) - (i - 4)//9)
                for (i, bit) in enumerate(bin(rb)[::-1]) if bit ==  '1']
    lb = [(1 + i - i//9, 1 + (i - 5) - (i - 5)//9)
                for (i, bit) in enumerate(bin(lb)[::-1]) if bit == '1']

    if board.active == BLACK:
        regular_moves = ["%i to %i" % (orig, dest) for (orig, dest) in rf + lf]
        reverse_moves = ["%i to %i" % (orig, dest) for (orig, dest) in rb + lb]
        return regular_moves + reverse_moves
    else:
        regular_moves = ["%i to %i" % (orig, dest) for (orig, dest) in rb + lb]
        reverse_moves = ["%i to %i" % (orig, dest) for (orig, dest) in rf + lf]
        return reverse_moves + regular_moves
