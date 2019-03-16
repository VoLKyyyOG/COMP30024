"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching
Authors: Akira and Callum
Team: _blank_
"""

"""
Okay so
1. jump wasn't working (99% sure of this) due to logic, so that's been adjusted
2. Make valid_hex redundant by only needing coordinate and data to determine valid moves and jumps
3. Streamlined debugging (just adjust debug_flag in search.py)
4. Addition of classes.py to allow Vector addition, subtraction and scalar multiplication - see example syntax in the file.
5. Make a lot of things global e.g. valid_coordinates (see moves.py) to reduce memory usage in future

1. should find a way to add non-movable pieces to global as well then
2
"""

"""FOR DEBUGGING"""
DEBUG_FLAG = True

import json
import sys
#################
from print_debug import *
from classes import *
from moves import *
# Use command: python search.py test-files/test.json to run it via terminal

def main():
    # Read argv input
    with open(sys.argv[1]) as file:
        data = json.load(file)
        print("Data input:", data)

    # Print current state
    print_board(debug(data), message = "Test Board", debug=True)

    # Find the player goal
    player = data["colour"]
    player_goal = find_goal(player, data)
    print("Player Goal: ",player_goal)
    print("**********************************************************")

    # Print possible moves and valid adjacent hexes
    ### ADJUST #DEBUGGING PRINTING HERE
    possible_moves(data, player_goal, debug_flag = True)

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()