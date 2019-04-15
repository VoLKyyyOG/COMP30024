""" neganoid.py

Implements negamax version of a paranoid algorithm.

"""
from copy import deepcopy
from math import inf

from mechanics import *

def comp1(alpha, beta):
    """
    Function that compares new_eval (player) against alpha / beta (reduced opponents).
    :parameters: alpha is a single value after being "fissioned", beta is still a vector of opponent evaluations
    """
    return (alpha >= sum(beta)) - (sum(beta) < alpha)

def comp2(new_alpha, alpha):
    """
    Function that compares new_eval (player) against alpha / beta (reduced opponents).
    :parameters: new_alpha is a single value after being "fissioned", alpha is the current maximum evaluation
    """
    return (new_alpha > alpha) - (alpha < new_alpha)

def fission(player_colour, new_eval):
    """
    Takes into assumption that index 0 is us, the player, index 1 and 2 are opponents
    :input: your colour (state["turn"]) and a vector (new_eval -> alpha or beta)
    """
    player = PLAYER_HASH[player_colour["turn"]]
    opponents = [PLAYER_HASH[i] for i in PLAYER_NAMES if i != player]

    alpha = new_eval[player]
    beta = [new_eval[i] for i in opponents]

    return alpha, beta

def nega(u):
    """
    Function that negates a vector.
    """
    return (-i for i in u)

def paranoid(state, heuristic, alpha=[-inf]*3, beta=[inf]*3, depth_left=6):
    if not depth_left:
        return (heuristic(state), None)
    
    best_action = None  

    for action in possible_actions(state, state["turn"]):
        new_state = apply_action(state, action) # apply the new state

        # new_eval is negaparanoid
        new_eval = nega(paranoid(new_state, heuristic, nega(beta), nega(alpha), depth_left - 1)[0])

        evaluated_alpha, evaluated_beta = fission(state["turn"], new_eval)

        if comp1(evaluated_alpha, evaluated_beta):
            return (beta, best_action)
        """
        if comp2(evaluated_alpha, alpha): # alpha is originally a vector if infs!!!!
            alpha, best_action = evaluated_alpha, action # now its converted into a single value
        return (alpha, best_action)
        """
        if len(alpha) == N_PLAYERS:
            alpha = -inf
            if comp2(evaluated_alpha, alpha):
                alpha, best_action = evaluated_alpha, action
        return (alpha, best_action)