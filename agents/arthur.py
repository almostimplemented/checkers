# Andrew Edwards -- almostimplemented.com
# =======================================
# A checkers agent implementaiton based
# on Arthur Samuel's historic program.
#
# Last updated: July 21, 2014

# Imports
import sys
import copy
import checkers

# Constants
EMPTY, RED, RED_KING, BLUE, BLUE_KING = range(5)

# Feature functions
def adv(board): # Advancement
    """
        The parameter is credited with 1 for each passive man in the
        fifth and sixth rows (counting in passive's direction) and
        debited with 1 for each passive man in the third and fourth
        rows.
    """
    active = board.current_player
    passive = RED if active == BLUE else BLUE

    if passive == BLUE:
        close_enemies = [board.state[4][j] for j in range(0, 8, 2)
                            if board.state[4][j] == passive]          \
                      + [board.state[5][j] for j in range(1, 8, 2)
                            if board.state[5][j] == passive]
        far_enemies = [board.state[3][j] for j in range(1, 8, 2)
                            if board.state[3][j] == passive]            \
                      + [board.state[2][j] for j in range(0, 8, 2)
                            if board.state[2][j] == passive]
    else:
        close_enemies = [board.state[2][j] for j in range(0, 8, 2)
                            if board.state[4][j] == passive]          \
                      + [board.state[3][j] for j in range(1, 8, 2)
                            if board.state[5][j] == passive]
        far_enemies = [board.state[5][j] for j in range(1, 8, 2)
                            if board.state[3][j] == passive]            \
                      + [board.state[4][j] for j in range(0, 8, 2)
                            if board.state[2][j] == passive]

    print close_enemies
    print far_enemies

    return len(close_enemies) - len(far_enemies)

def apex(board): # Apex
    """
        #The parameter is debited with 1 if there are no kings on the
        #board, if either square (1, 3) or (6, 4) is occupied by an
        #active man, and if neither of these squares is occupied by a
        #passive man.
    """
    return 1

def back(board): # Back Row Bridge
    """
        The parameter is credited with 1 if there are no active kings
        on the board and if the two bridge squares ((0, 2) and (0, 6),
        or (7, 1) and (7, 5)) in the back row are occupied by passive
        pieces.
    """
    active = board.current_player
    passive = RED if active == BLUE else BLUE
    active_king = active + 1

    if passive == RED:
        back_row_flag = board.state[7][1] in [RED, RED_KING] \
                        and board.state[7][5] in [RED, RED_KING]
    else:
        back_row_flag = board.state[0][2] in [BLUE, BLUE_KING] \
                        and board.state[0][4] in [BLUE, BLUE_KING]

    active_king_flag = all(map(lambda x: x != active_king, board.state))

    return 1 if active_king_flag and back_row_flag else 0

def cent(board): # Center Control I
    """
        The parameter is credited with 1 for each of the following
        squares: 11, 12, 15, 16, 20, 21, 24, 25 which is occupied by
        a passive man.
    """
    active = board.current_player
    passive = RED if active == BLUE else BLUE

    if active == BLUE:
        control_squares = [(2, 0), (2, 2), (3, 1), (3, 3), (4, 0), (5, 1),
                           (5, 7), (6, 6)]
    else:
        control_squares = [(5, 5), (5, 7), (4, 4), (4, 6), (3, 7), (2, 6),
                           (2, 0), (1, 1)]

    control_squares = map(lambda x: board.state[x[0]][x[1]], control_squares)
    return len(filter(lambda x: x in [passive, passive + 1], control_squares))

def cntr(board): # Center Control II
    """
        The parameter is credited with 1 for each of the following
        squares: 11, 12, 15, 16, 20, 21, 24, 25 that is either
        currently occupied by an active piece or to which an active
        piece can move.
    """
    active = board.current_player
    passive = RED if active == BLUE else BLUE

    if active == BLUE:
        control_squares = [(2, 0), (2, 2), (3, 1), (3, 3), (4, 0), (5, 1),
                           (5, 7), (6, 6)]
    else:
        control_squares = [(5, 5), (5, 7), (4, 4), (4, 6), (3, 7), (2, 6),
                           (2, 0), (1, 1)]

    control_squares = map(lambda x: board.state[x[0]][x[1]], control_squares)
    return len(filter(lambda x: x in [active, active + 1], control_squares))

def corn(board): # Double-Corner Credit
    """
        The parameter is credited with 1 if the material credit value
        for the active side is 6 or less, if the passive side is ahead
        in matrerial credit, and if the active side can move into one
        of the double-corner squares.
    """
    return 1

def cramp(board): # Cramp
    """
        The parameter is credited with 2 if the passive side occupies
        the cramping square (13 for Black, and 20 for White) and at
        least one other nearby square (9 or 14 for Black and 19 or 20
        for White), while
    """
    return 1

def deny(board): # Denial of Occupancy
    """
        The parameter is credited 1 for each square defined in MOB if
        on the next move a piece occupying this square could be
        captured without exchange.
    """
    active = board.current_player
    passive = RED if active == BLUE else BLUE

    normal_moves = [(row_old, col_old, row_old + i, col_old + j)
                  for row_old in range(8)
                  for col_old in range(8)
                  for i in (-1, 1)
                  for j in (-1, 1)
                    if piece(row_old, col_old, board.state) in [active, active + 1]
                   and board.can_move(active, (row_old, col_old, row_old + i, col_old + j))]

    denied_moves = [move for move in normal_moves if takeable(move[2:], board.peek_move(move)) \
                                         and not takebackable(move[2:], board.peek_move(move))]

    return len(denied_moves)

def dia(board): # Double Diagonal File
    """
        This parameter is credited with 1 for each passive piece
        located in the diagonal files terminating in the double-
        corner squares.
    """
    return 1

def diav(board): # Diagonal Movement Value
    """
        The parameter is credited with 0.5 for each passive piece
        located on squares 2 removed from the double-corner diagonal
        files, with 1 for each passive located on squares 1 removed
        from the double-corner files, and 1.5 for each passive piece
        in the double-corner files.
    """
    return 1

def dyke(board): # Dyke
    """
        The parameter is credited with 1 for each string of passive
        pieces that occupy three adjacent diagonal squares.
    """
    return 1

def exch(board): # Exchange
    """
        The parameter is credited with 1 for each square to which the
        active side may advance a piece to force an exchange.
    """
    return 1

def expos(board): # Exposure
    """
        The parameter is credited with 1 for each passive piece that is
        flanked along one or the other diagonal by two empty squares.
    """
    return 1

def fork(board): # Threat of Fork
    """
        The parameter is credited with 1 for each situation in which
        passive pieces occupy two adjacent squares in one row and in
        which there are three empty squares so disposed that the active
        side could, by occupying one of them, threaten a sure capture
        of one or the other of the two pieces.
    """
    return 1

def gap(board): # Gap
    """
        The paremter is credited with 1 for each single empty square
        that separates two passive pieces along a diagonal, or that
        separates a passive piece from the edge of the board.
    """
    return 1

def guard(board): # Back Row Control
    """
        The parameter is credited with 1 if there are no active kings
        and if either the Bridge or the Triangle of Oreo is occupied
        by passive pieces.
    """
    return 1

def hole(board): # Hole
    """
        The parameter is credited with 1 for each empty square that is
        surrounded by three or more passive pieces.
    """
    return 1

def kcent(board): # King Center Control
    """
        The parameter is credited with 1 for each of the following
        squares: 11, 12, 15, 16, 20, 21, 24, and 25 which is occupied
        by a passive king.
    """
    return 1

def mob(board): # Total Mobility
    """
        The parameter is credited with 1 for each square to which the
        active side could move one or more pieces in the normal fashion
        disregarding the fact that jump moves may or may not be
        available.
    """
    active = board.current_player
    passive = RED if active == BLUE else BLUE

    normal_moves = [(row_old, col_old, row_old + i, col_old + j)
                  for row_old in range(8)
                  for col_old in range(8)
                  for i in (-1, 1)
                  for j in (-1, 1)
                   if piece(row_old, col_old, board.state) in [active, active + 1]
                   and board.can_move(active, (row_old, col_old, row_old + i, col_old + j))]

    return len(normal_moves)

def mobil(board): # Undenied Mobility
    """
        The parameter is credited with the difference between MOB and
        DENY.
    """
    return 1

def move(board): # Move
    """
        The parameter is credited with 1 if pieces are even with a
        total piece count (2 for men, and 3 for kings) of less than 24,
        and if an odd number of pieces are in the move system, defined
        as those vertical files starting with squares 1, 2, 3, and 4.
    """
    return 1

def node(board): # Node
    """
        The parameter is credited with 1 for each passive piece that
        is surrounded by at least three empty squares.
    """
    return 1

def oreo(board): # Triangle of Oreo
    """
        The parameter is credited with 1 if there are no passive kings
        and if the Triangle of Oreo (squares 2, 3, and 7 for Black, and
        squares 26, 30, and 31 for White) is occupied by passive
        pieces.
    """
    return 1

def pole(board): # Pole
    """
        The parameter is credited with 1 for each passive man that is
        completely surrounded by empty squares.
    """
    return 1

def recap(board): # Recapture
    """
        The parameter is identical with Exchange, as defined above.
    """
    return 1

def thret(board): # Threat
    """
        The parameter is credited with 1 for each square to which an
        active piece may be moved and in doing so threaten to capture
        a passive piece on a subsequent move.
    """
    return 1

parameter_list = [adv, apex, back, cent, cntr, corn, cramp, deny, dia, diav,
                  dyke, exch, expos, fork, gap, guard, hole, kcent, mob, mobil,
                  move, node, oreo, pole, recap, thret]

def moveFunction(board):
    legal_moves = board.get_legal_moves(board.current_player)
    return legal_moves[0]


# Utility Functions
def piece(row, col, state):
    try:
        return state[row][col]
    except IndexError:
        return -1

def can_jump(player, move, state):
    """
        Boolean function to determine of the player, move pair is legal.
        Has precondition that the move is of the form:
                    (x, y, x +/- 2, y +/- 2)
    """
    print move
    row_old, col_old, row_new, col_new = move

    row_jumped = (row_old + row_new) / 2
    col_jumped = (col_old + col_new) / 2

    if row_new < 0 or row_new > 7 or col_new < 0 or col_new > 7:
        return False

    if state[row_new][col_new] != EMPTY:
        return False

    if player == RED:
        if state[row_old][col_old] == RED and row_new > row_old:
            return False
        if state[row_jumped][col_jumped] != BLUE and \
           state[row_jumped][col_jumped] != BLUE_KING:
            return False
        return True

    if player == BLUE:
        if state[row_old][col_old] == BLUE and row_new < row_old:
            return False
        if state[row_jumped][col_jumped] != RED and \
           state[row_jumped][col_jumped] != RED_KING:
            return False
        return True


def takeable(cell, state):
    row, col = cell
    if state[row][col] in [RED, RED_KING]:
        player = BLUE
    else:
        player = RED
    return any(map(lambda x: can_jump(player, x, state), [(row - i, col - j, row + i, col + j)
                                                             for i in [-1, 1] for j in [-1, 1]
                                                             if piece(row - i, col - j, state)
                                                                    in [player, player + 1]]))


# This is the most complicated function in the module, because it has
# to perform a case by case analysis.

def takebackable(cell, state):
    """
        Assumes cell is takeable and that the opponent plays optimally.
        Checks if there is a chance to win a piece back after losing the
        piece at cell.
    """
    row, col = cell
    if state[row][col] in [RED, RED_KING]:
        victim = RED
    else:
        victim = BLUE

    attacker = RED if victim == BLUE else BLUE

    direction = -1 if victim == RED else 1

    threat_1 = piece(row + direction, col - 1, state) == attacker
    threat_2 = piece(row + direction, col + 1, state) == attacker
    king_threat_1 = piece(row + direction, col - 1, state) == attacker + 1
    king_threat_2 = piece(row + direction, col + 1, state) == attacker + 1
    king_threat_3 = piece(row - direction, col - 1, state) == attacker + 1
    king_threat_4 = piece(row - direction, col + 1, state) == attacker + 1

    if threat_1:
        plan_1 = piece(row - 2*direction, col + 2, state) in [victim, victim + 1] \
                 and piece(row - 3*direction, col + 3, state) != EMPTY \
                 and (piece(row - 2*direction, col, state) not in [victim, victim + 1] \
                      or piece(row - 3*direction, col - 1, state) != EMPTY)
        plan_2 = piece(row - 2*direction, col, state) in [victim, victim + 1] \
                 and piece(row, col+2, state) == EMPTY \
                 and piece(row - 3*direction, col - 1, state) != EMPTY \
                 and (piece(row - 2*direction, col + 2, state) not in [victim, victim + 1] \
                      or piece(row - 3*direction, col + 3, state) != EMPTY)
        plan_3 = piece(row, col+2, state) == victim + 1 \
                 and piece(row - 2*direction, col, state) == EMPTY \
                 and (piece(row - 2*direction, col + 2, state) not in [victim, victim + 1] \
                      or piece(row - 3*direction, col + 3, state) != EMPTY)
        if not (plan_1 or plan_2 or plan_3): return False

    if threat_2:
        plan_1 = piece(row - 2*direction, col - 2, state) in [victim, victim + 1] \
                 and piece(row - 3*direction, col - 3, state) != EMPTY \
                 and (piece(row - 2*direction, col, state) not in [victim, victim + 1] \
                      or piece(row - 3*direction, col + 1, state) != EMPTY)
        plan_2 = piece(row - 2*direction, col, state) in [victim, victim + 1] \
                 and piece(row, col-2, state) == EMPTY \
                 and piece(row - 3*direction, col + 1, state) != EMPTY \
                 and (piece(row - 2*direction, col - 2, state) not in [victim, victim + 1] \
                      or piece(row - 3*direction, col - 3, state) != EMPTY)
        plan_3 = piece(row, col+2, state) == victim + 1 \
                 and piece(row - 2*direction, col, state) == EMPTY \
                 and (piece(row - 2*direction, col + 2, state) not in [victim, victim + 1] \
                      or piece(row - 3*direction, col - 3, state) != EMPTY)
        if not (plan_1 or plan_2 or plan_3): return False

    if king_threat_1:
        plan_1 = piece(row - 2*direction, col + 2, state) in [victim, victim + 1] \
                 and piece(row - 3*direction, col + 3, state) != EMPTY \
                 and (piece(row - 2*direction, col, state) not in [victim, victim + 1] \
                      or piece(row - 3*direction, col - 1, state) != EMPTY) \
                 and (piece(row, col + 2, state) not in [victim, victim + 1] \
                      or piece(row + direction, col + 3, state) != EMPTY)
        plan_2 = piece(row - 2*direction, col, state) in [victim, victim + 1] \
                 and piece(row, col+2, state) == EMPTY \
                 and piece(row - 3*direction, col - 1, state) != EMPTY \
                 and (piece(row - 2*direction, col + 2, state) not in [victim, victim + 1] \
                      or piece(row - 3*direction, col + 3, state) != EMPTY) \
                 and (piece(row, col + 2, state) not in [victim, victim + 1] \
                      or piece(row + direction, col + 3, state) != EMPTY)
        plan_3 = piece(row, col+2, state) == victim + 1 \
                 and piece(row - 2*direction, col, state) == EMPTY \
                 and (piece(row - 2*direction, col + 2, state) not in [victim, victim + 1] \
                      or piece(row - 3*direction, col + 3, state) != EMPTY) \
                 and piece(row + direction, col + 3, state) != EMPTY
        if not (plan_1 or plan_2 or plan_3): return False

    if king_threat_2:
        plan_1 = piece(row - 2*direction, col - 2, state) in [victim, victim + 1] \
                 and piece(row - 3*direction, col - 3, state) != EMPTY \
                 and (piece(row - 2*direction, col, state) not in [victim, victim + 1] \
                      or piece(row - 3*direction, col + 1, state) != EMPTY) \
                 and (piece(row, col - 2, state) not in [victim, victim + 1] \
                      or piece(row + direction, col - 3, state) != EMPTY)
        plan_2 = piece(row - 2*direction, col, state) in [victim, victim + 1] \
                 and piece(row, col-2, state) == EMPTY \
                 and piece(row - 3*direction, col + 1, state) != EMPTY \
                 and (piece(row - 2*direction, col - 2, state) not in [victim, victim + 1] \
                      or piece(row - 3*direction, col - 3, state) != EMPTY) \
                 and (piece(row, col - 2, state) not in [victim, victim + 1] \
                      or piece(row + direction, col - 3, state) != EMPTY)
        plan_3 = piece(row, col+2, state) == victim + 1 \
                 and piece(row - 2*direction, col, state) == EMPTY \
                 and (piece(row - 2*direction, col + 2, state) not in [victim, victim + 1] \
                      or piece(row - 3*direction, col - 3, state) != EMPTY) \
                 and piece(row + direction, col - 3, state) != EMPTY
        if not (plan_1 or plan_2 or plan_3): return False

    if king_threat_3:
        plan_1 = piece(row + 2*direction, col + 2, state) == victim + 1 \
                 and piece(row + 3*direction, col + 3, state) != EMPTY \
                 and (piece(row + 2*direction, col, state) not in [victim, victim + 1] \
                      or piece(row + 3*direction, col - 1, state) != EMPTY) \
                 and (piece(row, col + 2, state) not in [victim, victim + 1] \
                      or piece(row - direction, col + 3, state) != EMPTY)
        plan_2 = piece(row + 2*direction, col, state) == victim + 1 \
                 and piece(row, col + 2, state) == EMPTY \
                 and piece(row + 3*direction, col - 1, state) != EMPTY \
                 and (piece(row + 2*direction, col + 2, state) not in [victim, victim + 1] \
                      or piece(row + 3*direction, col + 3, state) != EMPTY)
        plan_3 = piece(row, col + 2, state) in [victim, victim + 1] \
                 and piece(row + 2*direction, col, state) == EMPTY \
                 and piece(row - direction, col + 3, state) != EMPTY \
                 and (piece(row + 2*direction, col + 2, state) not in [victim, victim + 1] \
                      or piece(row + 3*direction, col + 3, state) != EMPTY)
        if not (plan_1 or plan_2 or plan_3): return False

    if king_threat_4:
        plan_1 = piece(row + 2*direction, col - 2, state) == victim + 1 \
                 and piece(row + 3*direction, col - 3, state) != EMPTY \
                 and (piece(row + 2*direction, col, state) not in [victim, victim + 1] \
                      or piece(row + 3*direction, col + 1, state) != EMPTY) \
                 and (piece(row, col - 2, state) not in [victim, victim + 1] \
                      or piece(row - direction, col - 3, state) != EMPTY)
        plan_2 = piece(row + 2*direction, col, state) == victim + 1 \
                 and piece(row, col - 2, state) == EMPTY \
                 and piece(row + 3*direction, col + 1, state) != EMPTY \
                 and (piece(row + 2*direction, col - 2, state) not in [victim, victim + 1] \
                      or piece(row + 3*direction, col - 3, state) != EMPTY)
        plan_3 = piece(row, col - 2, state) in [victim, victim + 1] \
                 and piece(row + 2*direction, col, state) == EMPTY \
                 and piece(row - direction, col - 3, state) != EMPTY \
                 and (piece(row + 2*direction, col - 2, state) not in [victim, victim + 1] \
                      or piece(row + 3*direction, col - 3, state) != EMPTY)
        if not (plan_1 or plan_2 or plan_3): return False
    return True


# Testing

if __name__ == '__main__':
    board = checkers.CheckerBoard()
    print 'Testing adv'
    print '-----------'
    print board
    print 'Call on new game: ' + str(adv(board))
    print ''
    print 'Shifting blue pieces closer'
    for i in range(0, 8, 2):
        board.make_move((2, i, 3, i + 1))
        board.make_move((1, i + 1, 2, i))
    print board
    print 'Call on resulting board: ' + str(adv(board))
    print ''
    print 'Shifting closest row of blue pieces closer'
    for i in range(1, 8, 2):
        board.make_move((3, i, 4, i - 1))
    print board
    print 'Call on resulting board: ' + str(adv(board))
    print ''
    print 'Testing back'
    print '------------'
    board.new_game()
    print 'Call on new game: ' + str(back(board))
    for i in range(0, 8, 2):
        board.make_move((2, i, 3, i + 1))
        board.make_move((1, i + 1, 2, i))
        board.make_move((0, i, 1, i + 1))
    print board
    print 'Call on resulting board: ' + str(back(board))
    print ''
    print 'Testing cent'
    print '------------'
    board.new_game()
    print 'Call on new game: ' + str(cent(board))
    print ''
    print 'Testing cntr'
    print '------------'
    board.new_game()
    print 'Call on new game: ' + str(cntr(board))
