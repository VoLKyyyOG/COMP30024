# Import libraries
import numpy as np
from collections import defaultdict

# Global Variables
MOVE, JUMP, EXIT = 0, 1, 2

GOAL = {
    "red": np.matrix([[3, -3], [3, -2], [3, -1], [3, 0]]),
    "green": np.matrix([[-3, 0],[-2, -1],[-1, -2],[0, -3]]),
    "blue": np.matrix([[-3, 3], [-2, 3], [-1, 3], [0, 3]])
} # Can test for membership -> [-3, 3] in GOAL["blue"] >>> True

POSSIBLE_DIRECTIONS = np.matrix([[0, 1], [1, 0], [1, -1], [0, -1], [-1, 0], [-1, 1]])

VALID_COORDINATES = np.array([
    [-3, 0], [-3, 1], [-3, 2], [-3, 3], 
    [-2, -1], [-2, 0], [-2, 1], [-2, 2], [-2, 3], 
    [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], [-1, 3], 
    [0, -3], [0, -2], [0, -1], [0, 0], [0, 1], [0, 2], [0, 3], 
    [1, -3], [1, -2], [1, -1], [1, 0], [1, 1], [1, 2], 
    [2, -3], [2, -2], [2, -1], [2, 0], [2, 1], 
    [3, -3], [3, -2], [3, -1], [3, 0]
])


# Move related functions -> to be called by agent for possible actions at the current stage
"""
Return values for the referee:
1. ("MOVE", ((q1, r1), (q2, r2)))
2. ("JUMP", ((q1, r1), (q2, r2)))
3. ("EXIT", (q1, q2))
4. ("PASS", None)
"""

def possible_actions(state, player_colour, debug_flag = False):
    """
    Function that finds all possible actions in a given state.
    :returns: list of possible actions.
    """
    result = list()

    possible_exit = [i for i in state["pieces"] if i in GOAL[player_colour]]

    for piece in state["pieces"]:
        result.extend([(piece, MOVE, dest) for dest in move(state, piece)])
        result.extend([(piece, JUMP, dest) for dest in jump(state, piece)])

    return result

def move(state, coordinate):
    """
    Function to see if a move action is possible.
    :returns: list of possible move directions.
    """
    # Non-movable pieces on board
    occupied = state["blocked"]

    possible_moves = list()

    for direction in POSSIBLE_DIRECTIONS:
        adjacent_hex = np.add(coordinate, direction)

        if adjacent_hex in VALID_COORDINATES: # Then it's not off-board
            if adjacent_hex not in occupied: # Then it's free for the taking
                possible_moves.append(adjacent_hex)

    return sorted(possible_moves)

def jump(state, coordinate):
    """
    Function to see if a jump action is possible.
    :returns: list of possible jump directions.
    """
    occupied = state["blocked"]

    possible_jumps = list()

    for direction in POSSIBLE_DIRECTIONS:
        adjacent_hex = np.add(coordinate, direction)
        target_hex = np.add(adjacent_hex, direction)

        if adjacent_hex in occupied: # Then you can jump over it
            if target_hex in VALID_COORDINATES: # Then not off-board
                if target_hex not in occupied: # Then actual place to land
                    possible_jumps.append(target_hex)

    return sorted(possible_jumps)

def exit_action(state, coordinate, player_colour):
    """
    Function to see if an exit is possible.
    :returns: True if coordinate is in goal
    """
    return coordinate in GOAL[state[player_colour]]