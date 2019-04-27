""" 
:filename: directed.py
:summary: Implementation of Directed Offensive. 
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""
# Standard modules
from math import inf

# User-defined files
from mechanics import *

MAX_DEPTH = 3

def directed_offensive(state, heuristic, us, target, depth_left=MAX_DEPTH):
    if not depth_left:
        cost = heuristic(state)
        return (cost, None)
    
    max_player_evals = [-inf, -inf, -inf]
    best_action = None
    p = state["turn"]

    generated_actions = possible_actions(state, p)

    for action in generated_actions:
        new_state = apply_action(state, action)

        player_eval = directed_offensive(new_state, heuristic, us, target, depth_left-1)[0]

        # If this is not us, then they will want to just maximise themselves
        if p != us:
            if player_eval[PLAYER_HASH[p]] > max_player_evals[PLAYER_HASH[p]]:
                max_player_evals, best_action = player_eval, action
        
        # If this is us:
        if p == us:
            # If this new eval lowers our target eval, then update our path with this action
            if player_eval[PLAYER_HASH[target]] < max_player_evals[PLAYER_HASH[target]]:
                max_player_evals, best_action = player_eval, action
            
            # Elif target eval was not lowered, then see if we can maximise our own path with this action
            elif player_eval[PLAYER_HASH[us]] > max_player_evals[PLAYER_HASH[us]]:
                max_player_evals, best_action = player_eval, action
            # Otherwise our current best action is whatever the first action is assuming good ordering
            else:
                best_action = generated_actions[0]

    return (max_player_evals, best_action)