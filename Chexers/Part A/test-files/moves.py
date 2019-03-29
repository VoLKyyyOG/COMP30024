""" moves.py

Defines core game structure, globals, and actions
Currently formatted for Part A

"""

########################## IMPORTS ###########################
# Standard modules
from collections import defaultdict
from copy import copy
from queue import PriorityQueue as PQ

# User-defined files
from classes import Vector, PLAYER_CODE
from print_debug import *

########################## GLOBALS ###########################
INF = float('inf')

# Goals for each player
GOAL = {
    "red": ((3, -3), (3, -2), (3, -1), (3, 0)),
    "blue": ((-3,0),(-2,-1),(-1,-2),(0,-3)),
    "green": ((-3, 3), (-2, 3), (-1, 3), (0, 3))
}

# Game valid coordinate positions (taken from the test generator script)
VALID_COORDINATES = ((-3, 0), (-3, 1), (-3, 2), (-3, 3),
                    (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-2, 3),
                    (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3),
                    (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3),
                    (1, -3), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
                    (2, -3), (2, -2), (2, -1), (2, 0), (2, 1),
                    (3, -3), (3, -2), (3, -1), (3, 0))

POSSIBLE_DIRECTIONS = ((0,1),(1,0),(1,-1),(0,-1),(-1,0),(-1,1))

FORWARD_DIRECTIONS = {
    "red" : ((1,-1),(1,0)),
    "green" : ((-1,1),(0,1)),
    "blue" : ((-1,0),(0,-1))
}

# As point indices range from -3 to 3
MAX_COORDINATE_VAL = 3

# action_flags for use in action tuples
MOVE, JUMP, EXIT = 0, 1, 2

#################### CLASSES & FUNCTIONS #####################

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
    if next_u: sight_set.add(next_u)
    if next_v: sight_set.add(next_v)

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

def move(coordinate, state, relaxed=False):
    """Finds possible move actions given a coordinate"""
    # Non-movable pieces on board
    occupied = state["blocks"]
    if not relaxed: occupied = state["blocks"] + state["pieces"]
    possible_moves = list()

    for direction in POSSIBLE_DIRECTIONS:
        adjacent_hex = Vector.add(coordinate, direction)

        if adjacent_hex in VALID_COORDINATES: # Then it's not off-board
            if adjacent_hex not in occupied: # Then it's free for the taking
                possible_moves.append(adjacent_hex)

    possible_moves.sort()
    return possible_moves

def jump(coordinate, state, relaxed=False):
    """Finds possible jump actions given a coordinate"""
    occupied = state["blocks"]
    if not relaxed: occupied = state["blocks"] + state["pieces"]
    possible_jumps = list()

    for direction in POSSIBLE_DIRECTIONS:
        adjacent_hex = Vector.add(coordinate, direction)
        target_hex = Vector.add(adjacent_hex, direction)

        if relaxed or adjacent_hex in occupied: # Then you can jump over it
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

def memoize(f):
    memo = []
    def helper(x):
        if not len(memo):
            memo.append(f(x))
        return memo[0]
    return helper

@memoize
def dijkstra_board(state):
    """Evaluates minimum cost to exit for each non-block position"""
    # NOTE: The dijkstra board is CONSTANT (memoizable) iff blocks/colour don't change
    valid_goals = set(GOAL[state['colour']]).difference(set(state['blocks']))

    #prev = {x:None for x in VALID_COORDINATES} # Stores optimal source.
    visited = set() # Flags if visited or not
    cost = {x:INF for x in VALID_COORDINATES} # Stores costs
    cost.update({x:1 for x in valid_goals}) # Sets goals cost
    queue = PQ()

    # Add exits to queue to get it started
    for goal in valid_goals:
        queue.put((cost[goal], goal))

    # Loop over queue (dijsktra)
    while not queue.empty():
        curr_cost, curr = queue.get()
        if curr not in visited:
            visited.add(curr)
            poss_neighbours = set(move(curr, state, True)).union(set(jump(curr, state, True)))
            for new in poss_neighbours:
                est_cost = curr_cost + 1
                if est_cost < cost[new]: # Better path than previous
                    cost[new] = est_cost
                    #prev[new] = curr
                queue.put((cost[new], new))
    return cost
