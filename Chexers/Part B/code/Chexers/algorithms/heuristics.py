"""
:filename: heuristics.py
:summary: Stores all heuristic and evaluation function related functions.
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""

########################### IMPORTS ##########################

# Standard modules
from math import inf
from copy import deepcopy
from collections import defaultdict
from queue import PriorityQueue as PQ

# User-defined files
from moves import add, sub, get_cubic_ordered, exit_action
from mechanics import num_opponents_dead

# Global Imports
from moves import POSSIBLE_DIRECTIONS, VALID_COORDINATES
from mechanics import PLAYER_NAMES, PLAYER_HASH, MAX_COORDINATE_VAL, MAX_EXITS

##############################################################

def exits(state):
    """
    Returns raw exit count as a tuple
    """
    return [state['exits'][player] for player in PLAYER_NAMES]

def desperation(state):
    """
    Returns deficit/surplus in pieces vs exit
    """
    # How many pieces available - how many pieces needed to win
    return [len(state[player]) - (MAX_EXITS - state['exits'][player]) for player in PLAYER_NAMES]

def paris_vector(state):
    """
    paris_heuristic returns the number of capturing actions possible for each player.
    :returns: [val_red, val_green, val_blue]
    """
    raw = paris(state)
    capturable = [len(raw[player]) for player in PLAYER_NAMES]
    return capturable

def paris(state):
    """
    Evaluates captures that each player could perform
    :returns: {player: list_of_capturing_actions for each player}
    """
    captures = defaultdict(list)
    occupied_hexes = function_occupied(state, PLAYER_NAMES)
    for player in PLAYER_NAMES:
        for action in jump_action(state, occupied_hexes, player):
            if is_capture(state, action, player):
                captures[player].append(action)
    return captures

def achilles_vector(state, reality=True):
    """
    achilles_vector returns the number of threats for each player.
    :FLAG reality: if True, counts actual opponents that could capture
    :returns: [val_red, val_green, val_blue]
    """
    raw = achilles(state, reality)
    return [len(raw[player]) for player in PLAYER_NAMES]

def achilles(state, reality=False):
    """
    Evaluates number of attackable angles on your pieces.
    :FLAG reality: True only returns actual about-to-kill-you opponents
    Ranges from 0 (all pieces in corners) to 6*N (all N pieces are isolated and not on an edge)
    """
    #### TODO: Make sure it works - it does not work (returned [0,0,0] even though it our piece was capturable!!!!)

    threats = defaultdict(set)
    for player in PLAYER_NAMES:
        # All opponent pieces
        if reality:
            occupied = set()
            for player in PLAYER_NAMES:
                occupied.union(set(state[player]))

        for piece in state[player]:
            possible_axes = POSSIBLE_DIRECTIONS[:3] # Three directions
            for diagonal in possible_axes:
                threat_1, threat_2 = add(piece, diagonal), sub(piece, diagonal)
                # Only a threat if the diagonal is fully empty, and does not have your own pieces
                if (threat_1, threat_2) in VALID_COORDINATES and (threat_1, threat_2) not in state[player]:
                    if reality:
                        if threat_1 in occupied:
                            threats[player].add(threat_1)
                        if threat_2 in occupied:
                            threats[player].add(threat_2)
                    else:
                        threats[player].update(set(threat_1, threat_2))
    return threats

def speed_demon(state):
    """
    Heuristic that uses uses a relaxed version of the game board by assuming a piece can always jump with or without a piece.
    The average is taken so that the player progression can be compared

    TODO: Coordinates must be then transformed so that changes in displacement
    evaluation do not outweigh the benefit of having exited a piece.
    """

    total_disp = lambda player: sum([get_cubic_ordered(piece)[PLAYER_HASH[player]] -
        MAX_COORDINATE_VAL for piece in state[player]])

    # Return average displacement, adding 0.5 to deal with dead players
    return [total_disp(player) / len(state[player])  if len(state[player]) > 0 else inf for player in PLAYER_NAMES]

def no_pieces(state):
    """
    What proportion of pieces do we currently own.
    """
    num_pieces = [len(state[player]) for player in PLAYER_NAMES]
    return num_pieces

def can_exit(state):
    """
    If we can exit, return the number of possible exit pieces.
    """
    return [len(exit_action(state, colour)) for colour in PLAYER_NAMES]

def corner_hexes(state):
    """
    See if a piece is in a corner hex (untakeable)
    TODO: MAKE IT ENEMY GOAL HEX POSITION
    """
    return [len([i for i in state[player] if i in CORNER_HEXES]) for player in PLAYER_NAMES]

def end_game_heuristic(state):
    """
    Tribute to Marvel's End Game. This is the heuristic used for our mp-mix algorithm and holds a very high win rate on battlegrounds.
    The commented code below ALWAYS wins against a greedy / random algorithm. The actual one is being adjusted manually for battlegrounds.
    """ """
        if num_opponents_dead(state) == 1: # if it is two player
        evals = [desperation(state), speed_demon(state), can_exit(state), exits(state)]
        weighted_evals = [2*h1 + 0.1*h2 + h3 + 10*h4 for h1,h2,h3,h4 in zip(evals[0], evals[1], evals[2], evals[3])]

    else:
        evals = [desperation(state), speed_demon(state), no_pieces(state), exits(state), can_exit(state)]
        weighted_evals = [h1 + 0.1*h2 + 2*h3 + 2*h4 + 0.1*h5 for h1,h2,h3,h4,h5 in zip(evals[0], evals[1], evals[2], evals[3], evals[4])]

    return [i if i < inf else -inf for i in weighted_evals] # speed demon is inf if dead
    """
    if num_opponents_dead(state) == 1: # if it is two player
        evals = [desperation(state), speed_demon(state), can_exit(state), exits(state)]
        weighted_evals = [2*h1 + 0.1*h2 + h3 + 10*h4 for h1,h2,h3,h4 in zip(evals[0], evals[1], evals[2], evals[3])]

    else:
        evals = [desperation(state), speed_demon(state), no_pieces(state), exits(state), can_exit(state)]
        weighted_evals = [h1 + 0.1*h2 + 2*h3 + 2*h4 + 0.1*h5 for h1,h2,h3,h4,h5 in zip(evals[0], evals[1], evals[2], evals[3], evals[4])]

    return [i if i < inf else -inf for i in weighted_evals] # speed demon is inf if dead

def retrograde_dijkstra(state):
    """Computes minimal traversal distance to exit for all N players"""
    cost = [sum(dijkstra_board(state, state["turn"])[piece] for piece in state[colour]) for colour in PLAYER_NAMES]
    print(cost)
    return cost

def dijkstra_board(state, colour):
    """Evaluates minimum cost to exit for each non-block position"""
    #### TODO: Given dynamic board, forcing 'moves only' i.e. jump_heuristic may be more accurate
    #### Otherwise this is a forward unto death greedy heuristic

    valid_goals = set(GOALS[colour])
    occupied = set()

    for player in [i for i in PLAYER_NAMES if i != colour]:
        valid_goals.difference_update(set(state[player]))

    visited = set() # Flags if visited or not
    cost = {x: inf for x in VALID_COORDINATES} # Stores costs
    cost.update({x: 1 for x in valid_goals}) # Sets goals cost
    queue = PQ()

    # Add exits to queue to get it started
    for goal in valid_goals:
        queue.put((cost[goal], goal))

    # Loop over queue (dijsktra)
    while not queue.empty():
        curr_cost, curr = queue.get()
        if curr not in visited:
            visited.add(curr)
            poss_neighbours = set(move_action(state, occupied, colour)).union(set(jump_action(state, occupied, colour)))
            for flag, coord in poss_neighbours:
                if flag != "EXIT":
                    current, destination = coord[0], coord[1]
                else:
                    current = coord
                est_cost = curr_cost + 1
                if est_cost < cost[current]: # Better path than previous
                    cost[current] = est_cost
                queue.put((cost[current], current))
    return cost
