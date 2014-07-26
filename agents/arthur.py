# Andrew Edwards -- almostimplemented.com
# =======================================
# A checkers agent implementaiton based
# on Arthur Samuel's historic program.
#
# Last updated: July 21, 2014

# Feature functions
def adv(board): # Advancement
    """
        The parameter is credited with 1 for each passive man in the
        fifth and sixth rows (counting in passive's direction) and
        debited with 1 for each passive man in the third and fourth
        rows.
    """
    return 1

def apex(board): # Apex
    """
        The parameter is debited with 1 if there are no kings on the
        board, if either square 7 or 26 is occupied by an active man,
        and if neither of these squares is occupied by a passive man.
    """
    return 1

def back(board): # Back Row Bridge
    """
        The parameter is credited with 1 if there are no active kings
        on the board and if the two bridge squares (1 and 3, or 30 and
        32) in the back row are occupied by passive pieces.
    """
    return 1

def cent(board): # Center Control I
    """
        The parameter is credited with 1 for each of the following
        squares: 11, 12, 15, 16, 20, 21, 24, 25 which is occupied by
        a passive man.
    """
    return 1

def cntr(board): # Center Control II
    """
        The parameter is credited with 1 for each of the following
        squares: 11, 12, 15, 16, 20, 21, 24, 25 that is either
        currently occupied by an active piece or to which an active
        piece can move.
    """
    return 1

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
    return 1

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
    return 1

def mobile(board): # Undenied Mobility
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
                  dyke, exch, expos, fork, gap, guard, hole, kcent, mob, mobile,
                  move, node, oreo, pole, recap, thret]

def moveFunction(board):
    legal_moves = board.get_legal_moves(board.current_player)
    return legal_moves[0]
