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

EMPTY, RED, RED_KING, BLUE, BLUE_KING = range(5)

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

    jumpFlag = 0
    if n == 2:
        B = checkers.CheckerBoard()
        print "Red moves first."
        turn = 1
        current_player = B.current_player
        while not B.game_over(current_player):
            print B

            legal_moves = B.get_legal_moves(current_player)

            if jumpFlag:
                print "Make jump."
                print ""
            else:
                print "Turn %i" % turn
                print ""

            for (i, move) in enumerate(legal_moves):
                print "Move " + str(i) + ": " + str(move[:2]) + " to " + str(move[2:])

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
            if B.current_player == current_player:
                jumpFlag = 1
                print "Jumps must be taken."
                continue
            else:
                current_player = B.current_player
                jumpFlag = 0
                turn += 1

        print B
        if B.current_player == RED:
            print "Congrats Blue, you win!"
        else:
            print "Congrats Red, you win!"

        return 0


    elif n == 1:
        agent_module = raw_input("Enter name of agent module: ");
        __import__("agents." + agent_module)
        agent_module = sys.modules["agents." + agent_module]
        cpu = agent.CheckersAgent(agent_module.moveFunction)
        # Error handle
        choice = raw_input("Enter 1 to go first and 2 to go second: ")
        # Error handle
        if (choice == '1'):
            human_color = RED
            cpu_color   = BLUE
        else:
            human_color = BLUE
            cpu_color   = RED

        B = checkers.CheckerBoard()
        print "Red moves first."
        turn = 1
        current_player = B.current_player
        while not B.game_over(current_player):
            print B

            if current_player == human_color:
                legal_moves = B.get_legal_moves(current_player)

                if jumpFlag:
                    print "Make jump."
                    print ""
                else:
                    print "Turn %i" % turn
                    print ""

                for (i, move) in enumerate(legal_moves):
                    print "Move " + str(i) + ": " + str(move[:2]) + " to " + str(move[2:])

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
                if B.current_player == current_player:
                    jumpFlag = 1
                    print "Jumps must be taken."
                    continue
                else:
                    current_player = B.current_player
                    jumpFlag = 0

            else:
                move = cpu.doMove(B)
                B.make_move(move)
                print "Turn %i" % turn
                print "CPU moved " + str(move[:2]) + " to " + str(move[2:])
                if B.current_player == current_player:
                    jumpFlag = 1
                    print "Jumps must be taken."
                    continue
                else:
                    current_player = B.current_player
                    jumpFlag = 0
                print ""

            turn += 1

        if B.current_player == RED:
            print "Congrats Blue, you win!"
        else:
            print "Congrats Red, you win!"

        return 0
        print "Sorry! Not implemented yet"
    else:
        print "Sorry! Not implemented yet"
        # red_agent = raw_input("Enter filename or path to first agent file:")

if __name__ == '__main__':
    try:
        status = main()
        sys.exit(status)
    except KeyboardInterrupt:
        print ""
        print "Game terminated."
        sys.exit(1)
