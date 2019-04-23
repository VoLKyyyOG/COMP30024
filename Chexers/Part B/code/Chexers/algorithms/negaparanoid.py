""" 
:filename: negaparanoid.py
:summary: Implementation of Paranoid using Negamax as its basis.
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""
# Standard modules
from math import inf

# User-defined files
from mechanics import *

MAX_DEPTH = 12
CODES = {
    "red": 0,
    "green": 1,
    "blue": 2
}

def nega(u):
    """
    Function that negates a vector.
    """
    return [-i for i in u]

def paranoid(state, heuristic, alpha=[-inf]*N_PLAYERS, beta=[inf]*N_PLAYERS, depth_left=MAX_DEPTH, print_debug=False):
    best_action = None
    if not depth_left:
        if print_debug:
            print(f"\n\t\t\t\t\t\t\t\tReached max depth {depth_left}")
        cost = heuristic(state)
        return (cost, best_action)

    for action in possible_actions(state, state["turn"], paranoid_play=True):
        new_state = apply_action(state, action) # apply the new state

        score, move = paranoid(new_state, heuristic, nega(beta), nega(alpha), depth_left - 1)
        new_eval = nega(score)

        player_eval = new_eval[CODES[state["turn"]]]

        if print_debug:
            print(f"\n\t\t\t\t\t\t\t\tNew Evaluation is {new_eval}\n")

        if player_eval >= sum(beta): # check if new_alpha >= beta
            if print_debug:
                print(f"\n\t\t\t\t\t\t\t\tRETURNING BETA {beta , best_action} (sum of beta is {sum(beta)})")
            return (beta, best_action)
        
        if player_eval > sum(alpha): # check if new_alpha > current_max_alpha
            alpha, best_action = new_eval, action

        if print_debug:
            print(f"\n\t\t\t\t\t\t\t\tRETURNING ALPHA {alpha, best_action} (sum of alpha is {sum(alpha)})")

        return (alpha, best_action)