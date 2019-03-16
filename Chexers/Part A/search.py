"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Akira and Callum
Team: _blank_
"""

import json
import sys
#################
from print_debug import debug, print_board
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
    print("Player Gaol: ",player_goal)
    print("**********************************************************")

    # Print possible moves and valid adjacent hexes
    possible_moves(data, player_goal)

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
