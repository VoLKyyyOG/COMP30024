""" 
:filename: negaparanoid.py
:summary: Implementation of Paranoid using Negamax as its basis.
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""
# Standard modules
from math import inf

# User-defined files
from mechanics import *

MAX_DEPTH = 4

def paranoid(state, heuristic, max_player, alpha=-inf, beta=inf, depth_left=MAX_DEPTH):
    
    if not depth_left:
        cost = heuristic(state, runner=True)
        return (cost, None)

    best_action = None
    p = state["turn"]
    
    if p == max_player:
        generated_actions = possible_actions(state, p)

        for action in generated_actions:
            new_state = apply_action(state, action, ignore_dead=True)
            next_player = new_state["turn"]

            player_eval = paranoid(new_state, heuristic, max_player, alpha, beta, depth_left-1)[0]

            if action[0] == "EXIT":
                alpha, best_action = inf, action

            if player_eval[PLAYER_HASH[p]] > alpha:
                alpha, best_action = player_eval[PLAYER_HASH[p]], action

            if alpha >= beta:
                return (player_eval, best_action)

        return (player_eval, best_action)
    else:
        generated_actions = possible_actions(state, p)

        for action in generated_actions:
            
            new_state = apply_action(state, action, ignore_dead=True)
            next_player = new_state["turn"]
            
            player_eval = paranoid(new_state, heuristic, max_player, alpha, beta, depth_left-1)[0]

            if player_eval[PLAYER_HASH[p]] < beta:
                beta, best_action = player_eval[PLAYER_HASH[p]], action

            if alpha >= beta:
                return (player_eval, best_action)
            
        return (player_eval, best_action)