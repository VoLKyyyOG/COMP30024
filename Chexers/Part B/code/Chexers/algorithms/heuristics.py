"""
:filename: heuristics.py
:summary: Stores all heuristic and evaluation function related functions.
:authors: Akira Wang (913391), Callum Holmes (899251)
"""

########################### IMPORTS ##########################

# Standard modules
from math import inf
from copy import deepcopy
from collections import defaultdict
from queue import PriorityQueue as PQ
import numpy as np

# User-defined functions
from moves import add, sub, get_cubic_ordered, exit_action, jump_action
from mechanics import two_players_left, function_occupied, is_capture, is_dead

# Global Imports
from moves import POSSIBLE_DIRECTIONS, VALID_COORDINATES, CORNER_SET
from mechanics import PLAYER_NAMES, PLAYER_HASH, MAX_COORDINATE_VAL, MAX_EXITS

##############################################################

####: TODO: How benefifical is a -inf anyway?
def exclude_dead(heuristic):
    """
    Overwrites heuristic evaluation to -inf for any dead players if you want
    :returns: adjusted heuristic
    """
    def evaluate(state):
        output = heuristic(state)
        dead = np.array([-inf if is_dead(state, player) else 0 for player in PLAYER_NAMES])
        return dead + output

    return evaluate

def exits(state):
    """
    Returns raw exit count as a tuple
    :returns: [red_eval, green_eval, blue_eval]
    """
    return np.array([state['exits'][player] for player in PLAYER_NAMES])

def desperation(state):
    """
    Returns deficit/surplus in pieces vs exit
    :returns: [red_eval, green_eval, blue_eval]
    """
    # How many pieces available - how many pieces needed to win
    margin = lambda state, player: len(state[player]) - (MAX_EXITS - state['exits'][player])
    return np.array([margin(state, player) for player in PLAYER_NAMES])

@exclude_dead
def displacement(state):
    """
    Attempts to fix the exiting problem associated with the daemon by removing n from calculations.
    This has the virtue of d/dn(daemon) = 0, which (among other factors) means it is unimpacted by exits.
    """
    total_disp = lambda player: sum([get_cubic_ordered(piece)[PLAYER_HASH[player]] -
        MAX_COORDINATE_VAL for piece in state[player]])
    return np.array([total_disp(player) for player in PLAYER_NAMES])

def nerfed_desperation(state):
    """
    :summary: Nerfs desperation so that it gets no gain from having more than 2 pieces in surplus
    E.g. surplus -inf to 2 will be unaffected but values 3 and above map to 2.
    Note that this doesn't interfere with exiting as desperation unaffected by exit actions
    :returns: list of valuations
    """
    return np.minimum(np.array(desperation(state)), 2)

def paris(state):
    """
    Evaluates captures that each player could perform
    :shortfall: cannot tell which piece captures what, nor the capturable player
    :returns: {player: list_of_capturing_actions for each player}
    """
    captures = defaultdict(list)
    occupied_hexes = function_occupied(state, PLAYER_NAMES)
    for player in PLAYER_NAMES:
        for action in jump_action(state, occupied_hexes, player):
            if is_capture(state, action, player):
                captures[player].append(action)
    return captures

def paris_vector(state):
    """
    Returns the number of capturing actions possible for each player.
    :returns: [val_red, val_green, val_blue]
    """
    return np.array([len(paris(state)[player]) for player in PLAYER_NAMES])

def achilles_vector(state, reality=False):
    """
    achilles_vector returns the number of threats for each player.
    :FLAG reality: if True, counts actual opponents that could capture
    :returns: [val_red, val_green, val_blue]
    """
    raw = achilles(state, reality)
    return np.array([len(raw[player]) for player in PLAYER_NAMES])

def achilles(state, reality=False):
    """
    Evaluates number of attackable angles on your pieces.
    :FLAG reality: True only returns actual about-to-kill-you opponents
    Ranges from 0 (all pieces in corners) to 6*N (all N pieces are isolated and not on an edge)
    """

    threat_set = defaultdict(set)
    possible_axes = POSSIBLE_DIRECTIONS[:3] # Three directions
    for player in PLAYER_NAMES:
        if reality:
            # All pieces
            occupied = function_occupied(state, PLAYER_NAMES)

        for piece in state[player]:
            for diagonal in possible_axes:
                potential_threats = set([add(piece, diagonal), sub(piece, diagonal)])
                if potential_threats.issubset(VALID_COORDINATES) and not bool(potential_threats.intersection(set(state[player]))):
                    if reality:
                        # Only add threats that could actually capture
                        potential_attackers = potential_threats.intersection(occupied)
                        if len(potential_attackers) == 1:
                            threat_set[player].update(potential_attackers)
                    else:
                        threat_set[player].update(potential_threats)
    return threat_set

def speed_demon(state):
    """
    Heuristic that uses uses a relaxed version of the game board by assuming a piece can always jump with or without a piece.
    The average is taken so that the player progression can be compared

    TODO: Coordinates must be then transformed so that changes in displacement
    evaluation do not outweigh the benefit of having exited a piece.
    """
    # Return average displacement, -inf if dead
    #return [total_disp(player) / len(state[player])  if len(state[player]) > 0 else -inf for player in PLAYER_NAMES]

    # Since displacement is -inf wrapped, +1 will preserve -inf
    return np.array(displacement(state)) / (np.array(no_pieces(state)) + 0.001)

def no_pieces(state):
    """
    What number of pieces do we currently own.
    :return: vector of piece counts
    """
    return np.array([len(state[player]) for player in PLAYER_NAMES])

# NOTE MIGHT BE REDUNDANT AFTER FAVOURABLE HEXES
def can_exit(state):
    """
    Returns number of possible exit actions for each player.
    :returns: vector of results
    """
    return np.array([len(exit_action(state, colour)) for colour in PLAYER_NAMES])

def utility(state):
    """
    Measures strictly aspects of a state that relate to goal acquisition:
    1. How many exits? -- raw utility: encourages exiting
    2. Are your pieces in surplus/deficit to what you need? -- controls attack/defence
    3. Are your pieces (on average) close to goal? -- progression: encourages forward
    :returns: vector of valuations
    """
    evals = np.array([f(state) for f in [exits, nerfed_desperation, speed_demon]])
    weights = np.array([1, 1, 1.0 / 12]) # Displacement ranges up to 24
    return sum(map(lambda x,y: x*y, evals, weights))

def corner_hexes(state):
    """
    See if a piece is in a corner hex (untakeable)
    TODO: MAKE IT ENEMY GOAL HEX POSITION
    """
    return np.array([len(set(state[player]).intersection(CORNER_SET)) for player in PLAYER_NAMES])

def favourable_hexes(state):
    """
    Favourable hex positions:
    1. Corner hexes
    2. Our own exit hexes
    3. Enemy exit hex positions
    """
    corner_hex = [len(set(state[player]).intersection(CORNER_SET)) for player in PLAYER_NAMES]
    exit_hex = [len(exit_action(state, player)) for player in PLAYER_NAMES]
    block_exit_hex = [len(set(state[player]).intersection(OPPONENT_GOALS[player])) for player in PLAYER_NAMES]

    return sum([np.array(eval) for eval in [corner_hex, exit_hex, block_exit_hex]])

def end_game_heuristic(state):
    """
    Tribute to Marvel's End Game. This is the heuristic used for our mp-mix algorithm and holds a very high win rate on battlegrounds.
    MID:
    [desperation, speed_demon, no_pieces, exits, can_exit] with [1, 0.1, 2, 2, 0.1]
    END:
    [desperation, speed_demon, can_exit, exits] with [2, 0.1, 1, 10]
    """

    if two_players_left(state): # if it is two player
        evals = np.array([f(state) for f in [nerfed_desperation, speed_demon, exits]])
        weights = [2, 0.1, 10]
    else:
        evals = np.array([f(state) for f in [nerfed_desperation, speed_demon, exits]])
        weights = [1, 0.1, 2]
    return np.array(sum(map(lambda x,y: x*y, evals, weights)))

def retrograde_dijkstra(state):
    """
    Computes minimal traversal distance to exit for all N players
    :returns: vector of distances
    """
    cost = np.array([sum(dijkstra_board(state, state["turn"])[piece] for piece in state[player]) for player in PLAYER_NAMES])
    print(f"Retro-D: {cost}")
    return cost

def dijkstra_board(state, colour):
    """Evaluates minimum cost to exit for each non-block position"""
    #### TODO: Given dynamic board, forcing 'moves only' i.e. jump_heuristic may be more accurate
    #### Otherwise this is a forward unto death greedy heuristic

    valid_goals = set(GOALS[colour])
    #occupied = set()

    for player in get_opponents(state, player):
        valid_goals.difference_update(set(state[player]))

    visited = set() # Flags if visited or not
    cost = {x: inf for x in VALID_SET} # Stores costs
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
