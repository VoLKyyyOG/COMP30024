""" mp_mix.py

Implements an amazing 3-player algorithm

"""

########################### IMPORTS ##########################
# Standard modules
from copy import deepcopy
from math import inf
from collections import OrderedDict
# User-defined files
from mechanics import *

"""
Concept adapted from:
The MP-MIX algorithm: Dynamic Search Strategy Selection in Multi-Player Adversarial Search

Authors:
Inon Zuckerman, Ariel Felner

Implemented by:
Akira Wang, Callum Holmes

MP-MIX LOGIC:
If we are leader:
1. if a player has 1 piece we can eliminate them
2. else we will paranoid

If not leader:
1. if a player has 2 or less pieces we can attempt to eliminate
2. else we attack leader

If offence or defence threshold not met:
1. revert to maxn strategy
"""

def mp_mix(state, heuristic):
    """
    Works under the assumption that there are 3 players - can be made to catch exceptions.
    """
    # Heuristic scores for each player
    raw_scores = heuristic(state) # 3-player heuristics should output vectors

    # List of opponents, irrespective of whether they are dead
    turn_player = player(state)
    opponents = get_opponents(state)

    # Defines tuples (colour/name, score) in an OrderedDict
    scores = {PLAYER_NAMES[i] : raw_scores[i] for i in N_PLAYERS}
    scores = OrderedDict(sorted(scores.items(),
        reverse=True, key=lambda x: sorted(x, reverse=True)))

    # Hierarchy
    leader, rival, loser = scores.keys()
    high, medium, low = scores.values()

    # Edges
    leader_edge = high - medium
    rival_edge = medium - low

    # Strategy. Consider functionalising choose_directed(), choose_offence()

    # STRAT IDEAS:
    # IF in surplus, do a runner
    if turn_player == leader:
        # Go DirectedO on any weak player (1 piece left)
        if len(state[loser]) == 1:
            return directed_offence(state, heuristic, loser)
        # Else, go paranoid if sufficiently threatening
        elif leader_edge >= defence_threshold:
            return paranoid(state, heuristic)
    elif turn_player == rival:
        if leader_edge > loser_edge:
            return directed_offence(state, heuristic, leader)
    # Default, look strictly after your own interests
    return maxn_search(state, heuristic)

def directed_offence(state, heuristic, target):
    return NotImplementedError

def paranoid(state, heuristic):
    return NotImplementedError

def maxn_search(state, heuristic):
    return NotImplementedError
