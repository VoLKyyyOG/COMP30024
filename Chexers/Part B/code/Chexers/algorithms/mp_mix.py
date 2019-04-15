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

Our take on MP-MIX:
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

"""
minimisingPlayer = next_player(ignore_dead=True)

"""

def compare(u, v):
    """
    Function that compares new_eval (player) against alpha / beta (reduced opponents).
    :parameter v: a tuple of alpha / beta evaluations
    :parameter u: self evaluation
    :returns: alpha, the best action for the specified player
    """
    return (u > sum(v)) - (v < sum(u))

def fission(player_colour, vector):

    player = PLAYER_HASH[player_colour["turn"]]
    opponents = [PLAYER_HASH[i] for i in PLAYER_NAMES if i != player]
    alpha = vector[player]
    beta = [vector[i] for i in opponents]

    return alpha, beta


def negate(u):
    """
    Function that makes alpha / beta negative for the new evaluation.
    """
    return (-u[0], -u[1])


def paranoid(state, heuristic, alpha=[-inf]*3, beta=[inf]*3, depth_left=6):
    """Efficient minimax with alpha-beta pruning
    Note that evaluations are with respect to the state turn, NOT a maximisingPlayer"""
    if not depth_left:
        return (heuristic(state), None) # Could be quiesence search, or simple eval
    best_action = None


    for action in possible_actions(state):
        new_state = apply_action(state, action)

        # Initial: new alpha is vector of infs, new beta is a vector if -infs
        new_alpha = negate(beta)
        new_beta = negate(alpha)

        new_eval = -paranoid(new_state, heuristic, new_alpha, new_beta, depth_left - 1)[0]

        """
        alpha, beta = fission(state["turn"], vector)
        """

        if new_eval >= beta:
            return (beta, best_action)    # You are worse than the worst case in previous subtree
        if new_eval > alpha:  # Strictly greater so that you trim subtrees that a beta-cutoff occurred in
            alpha, best_action = new_eval, action
    return (alpha, best_action)

def maxn_search(state, heuristic):
    return NotImplementedError
