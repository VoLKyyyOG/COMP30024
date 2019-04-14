""" mp_mix.py

Implements an amazing 3-player algorithm

"""

########################### IMPORTS ##########################
# Standard modules
from copy import deepcopy
from math import inf
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

def mp_mix(state, heuristic, defenceThreshold, offenceThreshold, maximisingPlayer):
    """
    Works under the assumption that there are 3 players - can be made to catch exceptions.
    defenceThreshold and offenceThreshold is a value we need to assign given heuristic evaluation.
    """
    H = list()
    
    max_evaluation = -inf
    min_evaluation = inf

    opponent_name = [i for i in PLAYER_NAMES if i != maximisingPlayer]
    opponent1 = state[opponent_name[0]]
    opponent2 = state[opponent_name[1]]

    leader = None
    loser = None

    for player in PLAYER_NAMES:
        evaluation = heuristic(state, maximisingPlayer, player)
        if evaluation > max_evaluation:
            max_evaluation = evaluation
            leader = player
        if evaluation < min_evaluation:
            min_evaluation = evaluation
            loser = player

        H.append(evaluation)

    H.sort(reversed=True)
    leadingEdge = H[0] - H[1]

    if leader == maximisingPlayer:
        if loser != maximisingPlayer and len(state[loser]) == 1:
            best_action = directed_offence(state, heuristic, maximisingPlayer, loser)
            return best_action

        if leadingEdge >= defenceThreshold:
            # TODO
            enemy = state[opponent1] + state[opponent2]
            # TODO
            best_action = paranoid(state, heuristic, maximisingPlayer, enemy)
            return best_action
    else:
        if (loser != maximisingPlayer) and (len(state[loser]) == 2 or len(state[loser]) == 1):
            best_action = directed_offence(state, heuristic, maximisingPlayer, loser)
            return best_action

        if leadingEdge >= offenceThreshold:
            best_action = directed_offence(state, heuristic, maximisingPlayer, leader)
            return best_action

    best_action = maxn_search(state, heuristic, maximisingPlayer, opponent1, opponent2)

    return best_action

def directed_offence(state, heuristic, maximisingPlayer, targetPlayer):
    return AlgorithmRequiredError

def paranoid(state, heuristic, maximisingPlayer, enemy):
    return AlgorithmRequiredError

def maxn_search(state, heuristic, maximisingPlayer, opponent1, opponent2):
    return AlgorithmRequiredError