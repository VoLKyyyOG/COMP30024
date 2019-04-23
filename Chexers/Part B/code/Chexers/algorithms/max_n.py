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

def max_n(state, heuristic, depth_left=MAX_DEPTH, print_debug=False):
    max_player_evals = {name: -inf for name in PLAYER_NAMES}
    best_action = None
    turn_player = state["turn"]

    if not depth_left:
        if print_debug:
            print(f"\n\t\t\t\t\t\t\t\tReached max depth {depth_left}")
        cost = heuristic(state)[PLAYER_HASH[turn_player]]
        return (cost, None)
    
    for action in possible_actions(state, turn_player, paranoid_play=False):
        # If action is exit just exit...
        if action[0] == "EXIT":
            max_player_evals[turn_player] = inf
            return (max_player_evals[turn_player], action)
        ################################

        new_state = apply_action(state, action)

        new_player_eval = max_n(new_state, heuristic, depth_left-1)[0]

        if new_player_eval > max_player_evals[turn_player]:
            max_player_evals[turn_player], best_action = new_player_eval, action

    return (max_player_evals[turn_player], best_action)