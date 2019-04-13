""" Minimax.py

Implements standard minimax

Notes:
- Import of game_mechanics may be redundant... check this

"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files
from game_mechanics import *

def evaluation(state, maximisingPlayer):
    """Returns +1 if maximisingPlayer wins, -1 if other player, or 0 for draw"""
    if state.game_over():
        if state.game_status() == maximisingPlayer:
            return +1
        else:
            return -1
    else:
        return 0

def minimax(state, heuristic, maximisingPlayer):
    """Game-independent minimax implementation"""
    if state.player() == maximisingPlayer: # Maximising player
        result = (None, -inf)
    else:
        result = (None, +inf)

    if state.game_over():
        return (None, heuristic(state, maximisingPlayer))

    for action in state.possible_actions():
        # Compute minimax value of that subtree
        new_state = deepcopy(state)
        new_state.apply_action(action)
        next_subtree = (action, minimax(new_state)[1])

        if state.player() == maximisingPlayer:
            if next_subtree[1] > result[1]:
                result = score
        else:
            if next_subtree[1] < result[1]:
                result = score
    return result
