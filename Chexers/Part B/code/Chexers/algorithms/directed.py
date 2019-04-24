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

def directed_offensive(state, heuristic, prey, victim, depth_left=MAX_DEPTH):
    max_player_evals = [-inf]*N_PLAYERS
    best_action = None
    turn_player = state["turn"]

    if not depth_left:
        cost = heuristic(state)
        return (cost, None)

    if turn_player == prey:
        generated_actions = possible_actions(state, turn_player, force_exit=False, force_capture=True)
    else:
        generated_actions = possible_actions(state, turn_player, force_exit=True, force_capture=False)

    for action in generated_actions:
        new_state = apply_action(state, action)

        new_player_evals = directed_offensive(new_state, heuristic, prey, victim, depth_left-1)[0]

        # If this is not us, then they will want to just maximise themselves
        if turn_player != prey:

            if new_player_evals[PLAYER_HASH[turn_player]] > max_player_evals[PLAYER_HASH[turn_player]]:
                max_player_evals[PLAYER_HASH[turn_player]], best_action = new_player_evals[PLAYER_HASH[turn_player]], action
        
        # If this is us:
        if turn_player == prey:
            # If this new eval lowers our target eval, then update our path with this action
            if new_player_evals[PLAYER_HASH[victim]] < max_player_evals[PLAYER_HASH[victim]]:
                max_player_evals[PLAYER_HASH[prey]], best_action = new_player_evals[PLAYER_HASH[prey]], action
            
            # Elif target eval was not lowered, then see if we can maximise our own path with this action
            elif new_player_evals[PLAYER_HASH[prey]] > max_player_evals[PLAYER_HASH[prey]]:
                max_player_evals[PLAYER_HASH[prey]], best_action = new_player_evals[PLAYER_HASH[prey]], action
            # Otherwise our current best action is whatever the first action is
            else:
                best_action = generated_actions[0]

    return (max_player_evals, best_action)