""" minimax.py

Implements standard minimax

"""

########################### IMPORTS ##########################
# Standard modules
from copy import deepcopy
from math import inf
# User-defined files
from mechanics import (
    game_over, player, apply_action, possible_actions
)

# Adapted AIMA implementation
def alphabeta_search(state, heuristic, maximisingPlayer):
    """Search game to determine best action; use alpha-beta pruning.
    This version uses an evaluation function."""

    LIMIT = 2
    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if game_over(state) or depth > LIMIT:
            return heuristic(state, maximisingPlayer)
        current = -inf
        for action in possible_actions(state):
            new_state = apply_action(state, action, ignore_disqualified=True)
            current = max(current, min_value(new_state, alpha, beta, depth+1))
            if current >= beta:
                return current
            alpha = max(alpha, current)
        return current

    def min_value(state, alpha, beta, depth):
        if game_over(state) or depth > LIMIT:
            return heuristic(state, maximisingPlayer)
        current = inf
        for action in possible_actions(state):
            new_state = apply_action(state, action, ignore_disqualified=True)
            current = min(current, max_value(new_state, alpha, beta, depth+1))
            if current <= alpha:
                return current
            beta = min(beta, current)
        return current

    # Body of alphabeta_search:
    best_score = -inf
    beta = inf
    best_action = None
    for action in possible_actions(state):
        new_state = apply_action(state, action, ignore_disqualified=True)
        max_value(new_state, best_score, beta, 1)
        current = min_value(new_state, best_score, beta, 1)
        if current > best_score:
            best_score = current
            best_action = action
    return best_action

def minimax(state, heuristic, maximisingPlayer):
    """Game-independent minimax implementation"""
    if player(state) == maximisingPlayer: # Maximising player
        result = (None, -inf)
    else:
        result = (None, +inf)

    if game_over(state):
        return (None, heuristic(state, maximisingPlayer))

    for action in possible_actions(state):
        # Compute minimax value of that subtree
        new_state = apply_action(deepcopy(state), action, ignore_disqualified=True)
        next_subtree = (action, minimax(new_state, heuristic, maximisingPlayer)[1])

        if player(state) == maximisingPlayer:
            if next_subtree[1] > result[1]:
                result = next_subtree
        else:
            if next_subtree[1] < result[1]:
                result = next_subtree
    return result
