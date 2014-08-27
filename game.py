"""
    This module implements the game playing harness.
"""
# Andrew Edwards -- almostimplemented.com
# =======================================
# Harness for running a checkers match.
#
# Last updated: July 21, 2014

import checkers
import agent
import sys

BLACK, WHITE = 0, 1

def main():
    print "***************************************************"
    print "*                    Checkers                     *"
    print "*                                                 *"
    print "*                 Andrew Edwards                  *"
    print "*            www.almostimplemented.com            *"
    print "***************************************************"
    print "\n"
    print "\n"

    n = -1
    while not n in [0, 1, 2]:
        n = raw_input("How many human players? (0, 1, 2): ")
        try:
            n = int(n)
        except ValueError:
            print "Please input 0, 1, or 2."

    if n == 2:
        B = checkers.CheckerBoard()
        print "Black moves first."
        turn = 1
        current_player = B.active
        while not game_over(B):
            print B

            legal_moves = B.get_moves()

            if B.jump:
                print "Make jump."
                print ""
            else:
                print "Turn %i" % turn
                print ""

            for (i, move) in enumerate(get_move_strings(B)):
                print "Move " + str(i) + ": " + move

            while True:
                move_idx = raw_input("Enter your move number: ")
                try:
                    move_idx = int(move_idx)
                except ValueError:
                    print "Please input a valid move number."
                    continue

                if move_idx in range(len(legal_moves)):
                    break
                else:
                    print "Please input a valid move number."
                    continue

            B.make_move(legal_moves[move_idx])

            # If jumps remain, then the board will not update current player
            if B.active == current_player:
                print "Jumps must be taken."
                continue
            else:
                current_player = B.active
                turn += 1

        print B
        if B.active == WHITE:
            print "Congrats Black, you win!"
        else:
            print "Congrats White, you win!"

        return 0


    elif n == 1:
        agent_module = raw_input("Enter name of agent module: ");
        __import__(agent_module)
        agent_module = sys.modules[agent_module]
        cpu = agent.CheckersAgent(agent_module.move_function)
        while True:
            choice = raw_input("Enter 0 to go first and 1 to go second: ")
            try:
                choice = int(choice)
                break
            except ValueError:
                print "Please input 0 or 1."
                continue
        turn = 0
        B = checkers.CheckerBoard()
        current_player = B.active
        print "Black moves first."
        while not B.is_over():
            print B
            if turn % 2 == choice:
                legal_moves = B.get_moves()
                if B.jump:
                    print "Make jump."
                    print ""
                else:
                    print "Turn %i" % (turn + 1)
                    print ""
                for (i, move) in enumerate(get_move_strings(B)):
                    print "Move " + str(i) + ": " + move
                while True:
                    move_idx = raw_input("Enter your move number: ")
                    try:
                        move_idx = int(move_idx)
                    except ValueError:
                        print "Please input a valid move number."
                        continue
                    if move_idx in range(len(legal_moves)):
                        break
                    else:
                        print "Please input a valid move number."
                        continue
                B.make_move(legal_moves[move_idx])
                # If jumps remain, then the board will not update current player
                if B.active == current_player:
                    print "Jumps must be taken."
                    continue
                else:
                    current_player = B.active
                    turn += 1
            else:
                B.make_move(cpu.make_move(B))
                if B.active == current_player:
                    print "Jumps must be taken."
                    continue
                else:
                    current_player = B.active
                    turn += 1
        print B
        if B.active == WHITE:
            print "Congrats Black, you win!"
        else:
            print "Congrats White, you win!"
        return 0
    else:
        agent_module = raw_input("Enter name of first agent module: ");
        __import__(agent_module)
        agent_module = sys.modules[agent_module]
        cpu_1 = agent.CheckersAgent(agent_module.move_function)
        agent_module = raw_input("Enter name of second agent module: ");
        __import__(agent_module)
        agent_module = sys.modules[agent_module]
        cpu_2 = agent.CheckersAgent(agent_module.move_function)
        debug = raw_input("Would you like to step through game play? [Y/N]: ")
        debug = 1 if debug.lower()[0] == 'y' else 0
        B = checkers.CheckerBoard()
        current_player = B.active
        if debug:
            print "sorry not ready"
            return 0
        else:
            while not B.is_over():
                B.make_move(cpu_1.make_move(B))
                if B.active == current_player:
                    continue
                current_player = B.active
                while B.active == current_player and not B.is_over():
                    B.make_move(cpu_2.make_move(B))
                current_player = B.active
            if B.active == WHITE:
                print "Congrats Black, you win!"
            else:
                print "Congrats White, you win!"
            return 0



def game_over(board):
    return len(board.get_moves()) == 0

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

if __name__ == '__main__':
    try:
        status = main()
        sys.exit(status)
    except KeyboardInterrupt:
        print ""
        print "Game terminated."
        sys.exit(1)
