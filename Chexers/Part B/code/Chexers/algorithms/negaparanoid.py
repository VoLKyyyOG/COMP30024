""" 
:filename: negaparanoid.py
:summary: Implementation of Paranoid using Negamax as its basis.
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""
# Standard modules
from math import inf

# User-defined files
from mechanics import *

def nega(u):
    """
    Function that negates a vector.
    """
    return [-i for i in u]

def paranoid(state, heuristic, alpha=[-inf]*3, beta=[inf]*3, depth_left=12, print_debug=False):
    if not depth_left:
        if print_debug:
            print(f"\n\t\t\t\t\t\t\t\tReached max depth {depth_left}")
        cost = heuristic(state)
        print(cost)
        return cost
    
    best_action = None  

    for action in possible_actions(state, state["turn"], paranoid_play=True):
        new_state = apply_action(state, action) # apply the new state

        # new_eval is negaparanoid
        new_eval = -paranoid(new_state, heuristic, nega(beta), nega(alpha), depth_left - 1)[0]
            
        if print_debug:
            print(f"\n\t\t\t\t\t\t\t\tNew Evaluation is {new_eval}\n")

        if new_eval >= sum(beta):
            if print_debug:
                print(f"\n\t\t\t\t\t\t\t\tRETURNING BETA {sum(beta), best_action}")
            return (sum(beta), best_action)
        
        if len(alpha) == N_PLAYERS:
            alpha = -inf
            if new_eval > alpha:
                alpha, best_action = new_eval, action
        if print_debug:
            print(f"\n\t\t\t\t\t\t\t\tRETURNING ALPHA {alpha, best_action}")

        return (alpha, best_action)