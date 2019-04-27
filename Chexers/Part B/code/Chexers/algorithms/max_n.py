""" 
:filename: max_n.py
:summary: Implementation of Max^n
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""
# Standard modules
from math import inf

# User-defined files
from mechanics import *

MAX_DEPTH = 3
MAX_UTIL_VAL = 6 # Assume like 4 pieces + 2 exits, 3 pieces + 3 exits, 2 pieces + 4 exits GG

def max_n(state, heuristic, depth_left=MAX_DEPTH):
    if not depth_left:
        evals = heuristic(state) # vector of evaluations for r,g,b
        return (evals, None) # evals, no-action

    max_player_evals = [-inf, -inf, -inf]
    best_action = None
    p = state["turn"]
    
    generated_actions = possible_actions(state, p)

    for action in generated_actions:
        new_state = apply_action(state, action)

        player_eval = max_n(new_state, heuristic, depth_left-1)[0] # only take the vector of evaluations

        """ IMMEDIATE PRUNING (need to specify MAX_UTIL_VAL)
        if player_eval[PLAYER_HASH[p]] > MAX_UTIL_VAL:
            max_player_evals, best_action = player_eval, action
            return (max_player_evals, best_action)
        """

        if player_eval[PLAYER_HASH[p]] > max_player_evals[PLAYER_HASH[p]]:
            max_player_evals, best_action = player_eval, action
            

    return (max_player_evals, best_action)