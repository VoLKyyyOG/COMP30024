""" 
:filename: mp_mix.py
:summary: Defines the core structure of an MP-MIX agent
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""

########################### IMPORTS ##########################
# Standard modules
from copy import deepcopy
from math import inf
from collections import OrderedDict

# User-defined files
from mechanics import *
from .negaparanoid import paranoid
from .max_n import max_n

"""
Concept adapted from:
The MP-MIX algorithm: Dynamic Search Strategy Selection in Multi-Player Adversarial Search

Authors:
Inon Zuckerman, Ariel Felner

Implemented by:
Akira Wang, Callum Holmes

Current Agent Strategy:
If we are leader:
1. if a player has 1 piece we can eliminate them (within a close radius and heuristic?)
2. else we will paranoid

If not leader:
1. if a player has 2 or less pieces we can attempt to eliminate
2. else we attack leader

If offence or defence threshold not met:
1. revert to maxn strategy
"""

def mp_mix(state, heuristic, defence_threshold = 0, offence_threshold = 0):
    """
    Works under the assumption that there are 3 players - can be made to catch exceptions.
    If defence_threshold = offence_threshold = 0, it will degenerate to:
    1. Paranoid when winning
    2. Offensive when losing
    """
    # Heuristic scores for each player
    raw_scores = heuristic(state) # 3-player heuristics should output vectors

    # List of opponents, irrespective of whether they are dead
    turn_player = player(state)
    opponents = get_opponents(state)

    # Defines tuples (colour/name, score) in an OrderedDict
    scores = {PLAYER_NAMES[i] : raw_scores[i] for i in range(N_PLAYERS)}
    """
    scores = OrderedDict(sorted(scores.items(),
        reverse=True, key=lambda x: sorted(x, reverse=True)))
    """

    # Hierarchy
    leader, rival, loser = scores.keys()
    high, medium, low = scores.values()

    # Edges
    leader_edge = high - medium
    rival_edge = medium - low

    # Strategy. Consider functionalising choose_directed(), choose_offence()

    # STRAT IDEAS:
    # IF in surplus, do a runner
    # IF not enough, get a piece 
    if len(state[turn_player]) < 4:
        pass
        # return directed_offence(state, heuristic, loser)
        # return max(directed_offence(state, heuristic, loser), directed_offence(state, heuristic, leader))

    if turn_player == leader:
        # Go DirectedO on any weak player (1 piece left)
        if len(state[loser]) == 1:
            print("ONE PIECE REMAINING")
            pass
            # return directed_offence(state, heuristic, loser)
        # Else, go paranoid if sufficiently threatening
        elif leader_edge >= defence_threshold:
            print(f"\n\t\t\t\t\t\t\t\tUSING PARANOID")
            return paranoid(state, heuristic)[1]
    elif turn_player == rival:
        if leader_edge > rival_edge:
            print("LEADER EDGE GREATER THAN RIVAL EDGE")
            pass
            # return directed_offence(state, heuristic, leader)
    # Default, look strictly after your own interests
    print(f"\n\t\t\t\t\t\t\t\tUSING MAX_N")
    return max_n(state, heuristic)[1]

def directed_offence(state, heuristic, target):
    return NotImplementedError
