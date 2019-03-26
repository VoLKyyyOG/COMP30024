""" moves.py

Defines core game structure, globals, and actions
Currently formatted for Part A

"""

########################## IMPORTS ###########################
# Standard modules
from collections import defaultdict

# User-defined files
from classes import *

########################## GLOBALS ###########################
# Goals for each player
GOAL = {
    "red": [[3, -3], [3, -2], [3, -1], [3, 0]],
    "blue": [[-3,0],[-2,-1],[-1,-2],[0,-3]],
    "green": [[-3, 3], [-2, 3], [-1, 3], [0, 3]]
}

# Game valid coordinate positions (taken from the test generator script)
VALID_COORDINATES = [[-3, 0], [-3, 1], [-3, 2], [-3, 3],
                    [-2, -1], [-2, 0], [-2, 1], [-2, 2], [-2, 3],
                    [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], [-1, 3],
                    [0, -3], [0, -2], [0, -1], [0, 0], [0, 1], [0, 2], [0, 3],
                    [1, -3], [1, -2], [1, -1], [1, 0], [1, 1], [1, 2],
                    [2, -3], [2, -2], [2, -1], [2, 0], [2, 1],
                    [3, -3], [3, -2], [3, -1], [3, 0]]

POSSIBLE_DIRECTIONS = [[0,1],[1,0],[1,-1],[0,-1],[-1,0],[-1,1]]

# As point indices range from -3 to 3
MAX_COORDINATE_VAL = 3

# action_flags for use in action tuples
MOVE, JUMP, EXIT = 0,1,2

#################### CLASSES & FUNCTIONS #####################

def possible_actions(state, debug_flag = False):
    """Possible actions from current location"""
    result = list()

    MAX_MOVES = 3
    no_moves = 1

    for piece in state["pieces"]:
        
        # Always check if EXIT possible
        possible_exit = exit_action(piece, state, debug_flag)
        if possible_exit: # If so, ONLY do this action
            result.append((piece, EXIT, None))
            break

        # Next, we prefer jump moves so check these 
        possible_jumps = jump(piece, state)
        result += [(piece, JUMP, dest) for dest in possible_jumps]

        # Otherwise, we will move
        possible_moves = move(piece, state)
        result += [(piece, MOVE, dest) for dest in possible_moves]

        if debug_flag:
            print(f"Player coordinate: {piece}\nMoves: {possible_moves}\n" + \
            f"Jumps: {possible_jumps}\nExits? : {possible_exit}\n{BANNER}")
        
        # Only check a max of MAX_MOVES moves. This should allow going forward, sideways or backwards
        if no_moves == MAX_MOVES:
            break
        
        no_moves += 1

    return result

def move(coordinate, state):
    """Finds possible move actions given a coordinate"""
    # Non-movable pieces on board
    occupied = state["blocks"] + state["pieces"]
    possible_moves = list()

    for direction in POSSIBLE_DIRECTIONS:
        adjacent_hex = Vector.add(coordinate, direction)

        if adjacent_hex in VALID_COORDINATES: # Then it's not off-board
            if adjacent_hex not in occupied: # Then it's free for the taking
                possible_moves.append(adjacent_hex)

    return possible_moves

def jump(coordinate, state):
    """Finds possible jump actions given a coordinate"""
    occupied = state["blocks"] + state["pieces"]
    possible_jumps = list()

    for direction in POSSIBLE_DIRECTIONS:
        adjacent_hex = Vector.add(coordinate, direction)
        target_hex = Vector.add(adjacent_hex, direction)

        if adjacent_hex in occupied: # Then you can jump over it
            if target_hex in VALID_COORDINATES: # Then not off-board
                if target_hex not in occupied: # Then actual place to land
                    possible_jumps.append(target_hex)

    return possible_jumps

# Determines if exit action possible
def exit_action(coordinate, state, debug_flag=False):
    possible_exit = coordinate in GOAL[state["colour"]]
    if debug_flag:
        print("Exit Action Possible? ", possible_exit)
    return possible_exit
