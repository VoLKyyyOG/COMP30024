""" 
:filename: max_n.py
:summary: Implementation of Max^n
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""
from math import inf
from mechanics import *

def max_n(state, heuristic, colour, depth_left=6):
    # uses PLAYER_HASH to get index (r -> g -> b)
    if not depth_left:
        return (heuristic, None)

    player_evals = [-inf*N_PLAYERS]
    current_player = state["turn"]
    
    best_action = None


    for action in possible_actions(state, current_player):
        new_state = apply_action(state, action)
        next_player = next_player(state)

        new_eval = max_n(new_state, heuristic, next_player, depth_left-1)

        if new_eval[current_player] > player_evals[current_player]:
            player_evals, best_action = new_eval[0], new_eval[1]
    
    return (player_evals, best_action)
