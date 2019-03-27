""" moves.py

Defines core game structure, globals, and actions
Currently formatted for Part A

"""

########################## IMPORTS ###########################
# Standard modules
from collections import defaultdict
from copy import copy

# User-defined files
from classes import Vector, PLAYER_CODE
from print_debug import *

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

FORWARD_DIRECTIONS = {
    "red" : [[1,-1],[1,0]],
    "green" : [[-1,1],[0,1]],
    "blue" : [[-1,0],[0,-1]]
}

# As point indices range from -3 to 3
MAX_COORDINATE_VAL = 3

# action_flags for use in action tuples
MOVE, JUMP, EXIT = 0, 1, 2

#################### CLASSES & FUNCTIONS #####################

def jump_optimal(p1, p2, player, state):
    """Checks if two pieces could jumphop and returns convergence point"""
    pass

def get_next(current, occupied, direction):
    """If can move/jump in given direction, returns next possible point"""
    point = Vector.add(current, direction)
    if point in VALID_COORDINATES and point not in occupied:
        return point    # Reachable by move
    else: # Maybe you can jump over it
        point = Vector.add(point, direction)
        if point in VALID_COORDINATES and point not in occupied:
            return point    # Jumpable
    return None     # No eligible position

def sight(piece, player, occupied):
    """Finds set of all positions optimally reachable by piece"""
    u, v = FORWARD_DIRECTIONS[player]
    sight_set = set()
    if not piece or piece not in VALID_COORDINATES:
        return sight_set
    # Find eligible spots in u, v direction
    next_u, next_v = (get_next(copy(piece), occupied, x) for x in (u,v))
    if next_u: sight_set.add(tuple(next_u))
    if next_v: sight_set.add(tuple(next_v))

    sight_set = sight_set.union(sight(next_u, player, occupied))
    sight_set = sight_set.union(sight(next_v, player, occupied))
    return sight_set

def within_sight(position, dest, player):
    """Calculates whether a destination is reachable by directly moving 'forward' towards it"""
    # Idea: movement without moving sideways or backwards is most optimal.
    # If the two 'forward' directions towards a destination are u and v,
    # Then you want two scalars a, b such that dest = au + bv.
    # If a or b are negative, then you had to move back/sideways
    # Else, you only moved a times 'left-forward' and b times 'right-forward' -- optimal!
    u, v = FORWARD_DIRECTIONS[player]
    displacement = Vector.sub(dest, position)
    scalars = Vector.solve(u,v,displacement)
    return (scalars[0] >= 0 and scalars[1] >= 0)

def possible_actions(state, debug_flag = False):
    """Possible actions from current location"""
    result = list()

    for piece in state["pieces"]:

        # if a piece can exit, great! Do that immediately for Part A
        possible_exit = exit_action(piece, state, debug_flag)
        if possible_exit:
            result.append((piece, EXIT, None))
            return(result)

        possible_moves = move(piece, state)
        result += [(piece, MOVE, dest) for dest in possible_moves]

        possible_jumps = jump(piece, state)
        result += [(piece, JUMP, dest) for dest in possible_jumps]

        if debug_flag:
            print(f"Player coordinate: {piece}\nMoves: {possible_moves}\n" + \
            f"Jumps: {possible_jumps}\nExits? : {possible_exit}\n{BANNER}")

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

    possible_moves.sort()
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

    possible_jumps.sort()
    return possible_jumps

# Determines if exit action possible
def exit_action(coordinate, state, debug_flag=False):
    possible_exit = coordinate in GOAL[state["colour"]]
    if debug_flag:
        print("Exit Action Possible? ", possible_exit)
    return possible_exit
