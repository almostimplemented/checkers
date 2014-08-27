Checkers AI: a look at Arthur Samuel's ideas
=====================================

Usage
---
Download project. Navigate to directory. Do `python game.py`, and type in `arthur` when prompted for agent module.

(Note: to adjust how long the computer player "thinks" about its next move, you can vary the default depth parameter of the look ahead search. Go into `arthur.py` and change `depth=x` parameter of the function `move_function`.)

Files
---

 
 `checkers.py`
 
     This file contains the definition of the CheckerBoard class. Its methods include new game
     initialization, ASCII printed output, and getting legal moves from a given state.
 
 `agent.py`
 
     This file contains the implementation of the AI CheckersAgent class. All that is required
     of a CheckersAgent is that it have a function move_function() that takes in a game state and
     returns a legal move.
 
 `arthur.py`
 
     This file contains the implementation of an agent that is inspired by Arthur Samuel's 
     historic machine learning checkers program.
 
 `game.py`
 
     This file contains the harness for running an actual game of checkers.

> Written with [StackEdit](https://stackedit.io/).
