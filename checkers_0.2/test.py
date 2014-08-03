import checkers
import agent
import arthur
import random_agent

BLACK, WHITE = 0, 1

for i in range(100):
    print "game: " + str(i)
    B = checkers.CheckerBoard()
    cpu_1 = agent.CheckersAgent(arthur.move_function)
    cpu_2 = agent.CheckersAgent(random_agent.move_function)
    current_player = B.active
    turn = 1
    while not B.is_over():
        if turn % 100 == 0:
            print "# of turns: " + str(turn)
        B.make_move(cpu_1.make_move(B))
        if B.active == current_player:
            continue
        current_player = B.active
        turn += 1
        while not B.is_over() and B.active == current_player:
            B.make_move(cpu_2.make_move(B))
        current_player = B.active
    if B.active == WHITE:
        print "Congrats Black, you win!"
    else:
        print "Congrats White, you win!"
