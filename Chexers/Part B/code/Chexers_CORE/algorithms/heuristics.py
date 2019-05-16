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
from mechanics import (
    get_occupied, is_capture, is_dead, get_remaining_opponent,
    apply_action, possible_actions
)

# Global Imports
from moves import (
    POSSIBLE_DIRECTIONS, VALID_COORDINATES, CORNER_SET, OPPONENT_GOALS, GOALS
)
from mechanics import (
    PLAYER_NAMES, PLAYER_HASH, MAX_COORDINATE_VAL, MAX_EXITS
)

########################## FUNCTIONS #########################

def exits(state):
    """
    :summary: Returns raw # exits achieved. Absolute benchmark heuristic.
    :returns: [red_eval, green_eval, blue_eval]
    """
    return np.array([state['exits'][player] for player in PLAYER_NAMES])

def desperation(state):
    """
    :summary: Returns # pieces possessed - # pieces needed to exit to win
    Hence a high evaluation means one is in surplus, and low in shortage.
    :returns: [red_eval, green_eval, blue_eval]
    """
    # How many pieces available - how many pieces needed to win
    margin = lambda state, player: len(state[player]) - (MAX_EXITS - state['exits'][player])
    return np.array([margin(state, player) for player in PLAYER_NAMES])

def displacement(state):
    """
    :summary: Calculates raw displacement of all pieces from 'starting point'.
    E.g. a player with 4 pieces about to exit has displacement 6*4 = 24.
    :returns: sum of displacements for each player in numpy array
    """
    total_disp = lambda player: sum([get_cubic_ordered(piece)[PLAYER_HASH[player]] +
        MAX_COORDINATE_VAL for piece in state[player]])
    dead = np.array([-inf if is_dead(state, player) else 0 for player in PLAYER_NAMES])
    return dead + np.array([total_disp(player) for player in PLAYER_NAMES])

def achilles(state, reality=False):
    """
    :summary: Evaluates number of attackable angles on your pieces.
    :FLAG reality: True only returns actual about-to-kill-you opponents
    Ranges from 0 (all pieces in corners) to 6*N (all N pieces are isolated and not on an edge)
    :returns: numpy array of counts
    """
    threat_set = defaultdict(set)
    possible_axes = POSSIBLE_DIRECTIONS[:3] # Three directions
    for player in PLAYER_NAMES:
        if reality:
            # All pieces
            occupied = get_occupied(state, PLAYER_NAMES)

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

def achilles_real(state):
    """
    achilles_real returns the actual number of threats (i.e. immediately capturable) for each player.
    :returns: [val_red, val_green, val_blue]
    """
    raw = achilles(state, reality=True)
    return -np.array([len(raw[player]) for player in PLAYER_NAMES])

def speed_demon(state):
    """
    :summary: Average piece progression is measured - allows progression comparison
    :approach: uses a relaxed version of the game board by assuming a piece can always jump with or without a piece.
    :returns: numpy array, -inf if dead
    """
    return np.array(displacement(state)) / (np.array(no_pieces(state)))

def no_pieces(state):
    """
    :summary: Computes number of pieces we currently own.
    :return: numpy array
    """
    return np.array([len(state[player]) for player in PLAYER_NAMES])

def favourable_hexes(state):
    """
    :summary: Promotes favourable hex positions:
    1. Corner hexes
    2. Enemy exit hex positions
    :returns: numpy array
    """
    corner_hex = [len(set(state[player]).intersection(CORNER_SET)) for player in PLAYER_NAMES]
    block_exit_hex = [len(set(state[player]).intersection(OPPONENT_GOALS[player])) for player in PLAYER_NAMES]

    return sum([np.array(eval) for eval in [corner_hex, block_exit_hex]])

def block(state):
    """
    :summary: Promotes favourable hex positions with the possibility of two-player games.
    1. Corner hexes
    2. Enemy exit hex positions
    :returns: numpy array
    """
    try:
        alive_opponent = get_remaining_opponent(state)
        corner_hex = [len(set(state[alive_opponent]).intersection(CORNER_SET))]
        block_exit_hex = [len(set(state[alive_opponent]).intersection(OPPONENT_GOALS[alive_opponent]))]
        return sum([np.array(eval) for eval in [corner_hex, block_exit_hex]])
    except:
        return np.array([0,0,0])

def end_game_heuristic(state):
    """
    :summary: Tribute to Marvel's End Game.
    A heuristic resulting from several simulations and corresponding adjustments.
    :eval: (no. pieces in excess) + (average distance)
           + (favourable hex positions) + (no. exits) + (no. capturable pieces)
    :priorities: no. pieces in excess & exits
    However, will lean towards a favourable hex over distance,
    whilst minimising potential captures.
    :returns: numpy array
    """
    evals = np.array([f(state) for f in [desperation, speed_demon, favourable_hexes, exits, achilles_real]])
    weights = [1.2, 0.2, 0.1 , 2.5, 0.25]

    return np.array(sum(map(lambda x,y: x*y, evals, weights)))

def two_player_heuristics(state):
    """
    :summary: end_game but for 2-player scenarios
    :priorities: higher weighting on desperation, exits and speed_demon,
    the most exit-weighting heuristics.
    :returns: numpy array
    """
    evals = np.array([f(state) for f in [desperation, speed_demon, block, exits, achilles_real]])
    weights = [2, 0.4, 0.1, 5, 0.5]

    return np.array(sum(map(lambda x,y: x*y, evals, weights)))

def runner(state):
    """
    :summary: Simple Paranoid Heuristic.
    :eval: distance + number of pieces + number of exits
    :priorities: number of pieces over distance, but will always exit if possible.
    :returns: numpy array
    """
    evals = np.array([f(state) for f in [speed_demon, no_pieces, exits]])
    weights = [0.75, 1, 15]

    return np.array(sum(map(lambda x,y: x*y, evals, weights)))
