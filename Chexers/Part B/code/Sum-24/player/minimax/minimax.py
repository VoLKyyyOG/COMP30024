""" minimax.py

Implements standard minimax

"""

########################### IMPORTS ##########################
# Standard modules
from copy import deepcopy
from math import inf
# User-defined files
from mechanics import *

def evaluation(state, maximisingPlayer):
    """Returns +1 if maximisingPlayer wins, -1 if other player, or 0 for draw"""
    if game_over(state):
        if is_winner(state, maximisingPlayer):
            return +1
        else:
            return -1
    else:
        return 0

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
        new_state = apply_action(deepcopy(state), action)
        next_subtree = (action, minimax(new_state, heuristic, maximisingPlayer)[1])

        if player(state) == maximisingPlayer:
            if next_subtree[1] > result[1]:
                result = next_subtree
        else:
            if next_subtree[1] < result[1]:
                result = next_subtree
    return result
