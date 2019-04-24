""" 
:filename: negaparanoid.py
:summary: A negascout variant of negaparanoid.
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""
# Standard modules
from math import inf

# User-defined files
from mechanics import *

MAX_DEPTH = 12

def nega(u):
    """
    Function that negates a vector.
    """
    return [-i for i in u]

def null_window(alpha):
    """
    Functions that subtracts one off alpha for a null window.
    """
    return [-i-1 for i in alpha]

def negascoutanoid(state, heuristic, alpha=[-inf]*N_PLAYERS, beta=[inf]*N_PLAYERS, depth_left=MAX_DEPTH):
    """
    Paranoid implmenetation that uses negascout, a variant of negamax, which is a variant of minimax.
    """
    best_action = None

    if not depth_left:
        cost = heuristic(state)
        return (cost, best_action)

    generated_actions = possible_actions(state, state["turn"], force_exit=True)

    for action in generated_actions:
        new_state = apply_action(state, action) # apply the new state

        if action is generated_actions[0]: # given ordering of exit -> jump -> move, if action is the first action:
            score, move = negascoutanoid(new_state, heuristic, nega(beta), nega(alpha), depth_left - 1) # default negaparanoid
            new_eval = nega(score)
            player_eval = new_eval[PLAYER_HASH[state["turn"]]]
        else:
            score, move = negascoutanoid(new_state, heuristic, null_window(alpha), nega(alpha), depth_left - 1) # search with a null window (-alpha-1)
            new_eval = nega(score)
            player_eval = new_eval[PLAYER_HASH[state["turn"]]]
            
            if player_eval > alpha and player_eval < beta: # if null window failed, do a full re-search
                player_eval, move = negascoutanoid(new_state, heuristic, nega(beta), nega([player_eval*N_PLAYERS]), depth_left - 1)
        
        if player_eval > sum(alpha): # check if score > alpha
            alpha, best_action = new_eval, action

        if sum(alpha) >= sum(beta): # check if alpha >= beta
            return (beta, best_action)

        return (alpha, best_action)