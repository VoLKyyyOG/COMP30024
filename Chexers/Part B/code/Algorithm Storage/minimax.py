""" minimax.py

Implements standard minimax

"""

########################### IMPORTS ##########################
# Standard modules
from copy import deepcopy
from math import inf
# User-defined files
from mechanics import (
    game_over, player, apply_action, possible_actions
)

def negamax_ab(state, heuristic, a=-inf, b=inf, depth_left=4):
    """Efficient minimax with alpha-beta pruning
    Note that evaluations are with respect to the state turn, NOT a maximisingPlayer"""
    if not depth_left:
        return heuristic(state, a, b) # Could be quiesence search, or simple eval
    for action in possible_actions(state):
        new_state = apply_action(state, action, ignore_disqualified=True)
        new_eval = -negamax_ab(new_state, heuristic, -b, -a, depth_left - 1)
        if new_eval >= b:
            return b    # You are worse than the worst case in previous subtree
        if new_eval > a:  # Strictly greater so that you trim subtrees that a beta-cutoff occurred in
            a = new_eval  # a is effectively the 'best so far', but remember it maps to b in children
    return a
