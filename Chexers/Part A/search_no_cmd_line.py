"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching
Authors: Akira and Callum
Team: _blank_
"""

########################## IMPORTS ###########################
import json
import sys
#################
from print_debug import *
from classes import *
from moves import *
# Use command: python search.py test-files/test.json to run it via terminal

########################## GLOBALS ###########################
"""FOR DEBUGGING"""
DEBUG_FLAG = True

def main():
    data = {
    "colour": "red",
    "pieces": [[0,0],[0,3],[3,-3]],
    "blocks": [[-1,0],[-1,1],[1,1],[3,-1],[-2,0]]
    }

    print_board(debug(data), message = "Test Board", debug=True)
    # Print current state

    # Find the player goal
    player = data["colour"]
    player_goal = find_goal(player, data)
    print("Player Goal: ",player_goal)
    print("**********************************************************")

    # Print possible actions and valid adjacent hexes
    ### ADJUST #DEBUGGING PRINTING HERE
    possible_actions(data, debug_flag = True)

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
