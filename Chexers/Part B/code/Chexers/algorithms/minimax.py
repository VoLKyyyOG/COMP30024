""" minimax.py

Implements standard minimax

"""

########################### IMPORTS ##########################
# Standard modules
from copy import deepcopy
from math import inf
# User-defined files
from mechanics import *

def negamax_ab(state, heuristic, N_max=False, alpha=-inf, beta=inf, depth_left=6):
    """Efficient minimax with alpha-beta pruning
    Note that evaluations are with respect to the state turn, NOT a maximisingPlayer"""
    if not depth_left:
        return (heuristic(state), None) # Could be quiesence search, or simple eval
    best_action = None
    for action in possible_actions(state):
        new_state = apply_action(state, action, ignore_dead=not N_max)
        new_eval = -negamax_ab(new_state, heuristic, -beta, -alpha, depth_left - 1)[0]
        if new_eval >= beta:
            return (beta, best_action)    # You are worse than the worst case in previous subtree
        if new_eval > alpha:  # Strictly greater so that you trim subtrees that a beta-cutoff occurred in
            alpha, best_action = new_eval, action
    return (alpha, best_action)
