""" neganoid.py

Implements negamax version of a paranoid algorithm.

"""
# Standard modules
from math import inf
# User-defined files
from mechanics import *

"""
Comp1, comp2 and fission have been made obsolete 
TODO: clean up paranoid and make it exit
"""


def nega(u):
    """
    Function that negates a vector.
    """
    return [-i for i in u]

def paranoid(state, heuristic, alpha=[-inf]*3, beta=[inf]*3, depth_left=6, print_debug=False):
    if not depth_left:
        if print_debug:
            print(f"\n\t\t\t\t\t\t\t\tReached max depth {depth_left}")
        return heuristic(state)
    
    best_action = None  

    for action in possible_actions(state, state["turn"], paranoid_play=True):
        new_state = apply_action(state, action) # apply the new state

        # new_eval is negaparanoid
        new_eval = -paranoid(new_state, heuristic, nega(beta), nega(alpha), depth_left - 1)[0]
            
        if print_debug:
            print(f"\n\t\t\t\t\t\t\t\tNew Evaluation is {new_eval}\n")

        if new_eval >= sum(beta):
            if print_debug:
                print(f"\n\t\t\t\t\t\t\t\tRETURNING BETA {beta, best_action}")
            return (beta, best_action)
        
        if len(alpha) == N_PLAYERS:
            alpha = -inf
            if new_eval > alpha:
                alpha, best_action = new_eval, action
        if print_debug:
            print(f"\n\t\t\t\t\t\t\t\tRETURNING ALPHA {alpha, best_action}")

        return (alpha, best_action)
        















def comp1(alpha, beta):
    """
    Function that compares new_eval against beta / beta (reduced opponents).
    :parameters: alpha is a single value after being "fissioned", beta is still a vector of opponent evaluations
    """
    return (alpha >= sum(beta)) - (sum(beta) < alpha)

def comp2(new_alpha, alpha):
    """
    Function that compares new_eval against alpha / beta (reduced opponents).
    :parameters: new_alpha is a single value after being "fissioned", alpha is the current maximum evaluation
    """
    return (new_alpha > alpha) - (alpha < new_alpha)

def fission(player_colour, new_eval):
    """
    Splits new_eval into alpha and beta particles given a player colour
    :input: your colour (state["turn"]) and a vector (new_eval -> alpha or beta)
    :returns: an integer alpha, a 1x2 vector beta
    """
    player = PLAYER_HASH[player_colour]
    opponents = [PLAYER_HASH[i] for i in PLAYER_NAMES if i != player_colour]

    alpha = new_eval[player]
    beta = sum([new_eval[i] for i in opponents]) # sums the beta (all opponent evals)
    print(f"Alpha {alpha}, Beta {beta}")
    return alpha, beta