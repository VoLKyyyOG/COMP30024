from collections import defaultdict
from classes import *

# GLOBALS #########################

# Goals for each player
goals = defaultdict(list)
goals["red"].append([[3,r] for r in range(-3, 1)])
goals["blue"].append([[-3,0],[-2,1],[-1,2],[0,3]])
goals["green"].append([[q,3] for q in range(-3, 1)])

# Game valid coordinate positions
## Taken from the test generator script
valid_coordinates = [[-3, 0], [-3, 1], [-3, 2], [-3, 3],
                    [-2, -1], [-2, 0], [-2, 1], [-2, 2], [-2, 3],
                    [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], [-1, 3],
                    [0, -3], [0, -2], [0, -1], [0, 0], [0, 1], [0, 2], [0, 3],
                    [1, -3], [1, -2], [1, -1], [1, 0], [1, 1], [1, 2],
                    [2, -3], [2, -2], [2, -1], [2, 0], [2, 1],
                    [3, -3], [3, -2], [3, -1], [3, 0]]

# Partly adapted from https://www.redblobgames.com/grids/hexagons/#neighbors-axial
possible_directions = [[0,1],[1,0],[1,-1],[0,-1],[-1,0],[-1,1]]

# FUNCTIONS ######################

# Returns goals given player colour
def find_goal(player, data):
    # TEMPORARY # Default player goal
    player_goal = goals[player][0]

    # Check if goal not blocked by piece
    player_goal = [i for i in player_goal if i not in data["blocks"]]

    return player_goal

# Possible moves from current location
def possible_moves(data, player_goal, debug_flag= False):
    player_pos = data["pieces"]
    for i in player_pos:
        # All possible move actions to a coordinate in nested list form
        possible_moves = move(i, data, debug_flag)

        # All possible jump actions to a coordinate in nested list form
        possible_jumps = jump(i, data, debug_flag)

        # Checks if the current hex is eligible for an exit action
        exit_possible = exit_move(i, player_goal, debug_flag)

        if (debug_flag):
            print("Player coordinate: ", i)
            print("Possible Move Action to:",possible_moves)
            print("Possible Jump Action to:",possible_jumps)
            print("*" * 40)

# Retrieves adj hexes that are in valid coordinates
def adj_hex(coordinate):
    return [Vector.add(coordinate, x) for x in possible_directions if
        Vector.add(coordinate, x) in valid_coordinates]

# Finds possible move actions given a coordinate
def move(coordinate, data, debug_flag = False):
    # Non-movable pieces on board
    non_movable = data["blocks"] + data["pieces"]
    possible_moves = list()

    for direction in possible_directions:
        adjacent_hex = Vector.add(coordinate, direction)
        if adjacent_hex in valid_coordinates: # Then it's not off-board
            if adjacent_hex not in non_movable: # Then it's free for the taking
                possible_moves.append(adjacent_hex)
            elif (debug_flag):
                print("OCCUPIED - CANNOT MOVE")
        elif (debug_flag):
            print("OFF-BOARD - CANNOT MOVE")

    return possible_moves

# Finds possible jump actions given a coordinate
def jump(coordinate, data, debug_flag = False):
    # Jumpable pieces / blocks
    jumpable = data["blocks"] + data["pieces"]
    possible_jumps = list()

    for direction in possible_directions:
        adjacent_hex = Vector.add(coordinate, direction)
        target_hex = Vector.add(adjacent_hex, direction)
        # ONLY NESTED FOR DEBUGGING PURPOSES
        if adjacent_hex in jumpable: # Then you can jump over it
            if target_hex in valid_coordinates: # Then not off-board
                if target_hex not in jumpable: # Then actual place to land
                    possible_jumps.append(target_hex)
                elif (debug_flag):
                    print("HEX OCCUPIED - CANNOT JUMP")
            elif (debug_flag):
                print("OFF BOARD - CANNOT JUMP")

    return possible_jumps

# Determines if exit action possible
def exit_move(coordinate, player_goal, debug_flag = False):
    exit_possible = (coordinate in player_goal)
    if (debug_flag): print("Exit Action Possible? ", exit_possible)

    return exit_possible
