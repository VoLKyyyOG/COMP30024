"""
Team: _blank_ 
player.py to hold our player class
"""
# Import Dependencies
from moves import *
from agent_early_game import *
from agent_mid_game import *
from agent_endgame import *

"""
Agent Early Game - Monte Carlo / Book Learning
Agent Mid Game - Max^n, Paranoid, Directed Offence
Agent Endgame - Minimax
"""

# Import Libraries
from math import inf

# Global Variables

# Functions

def agent_logic(player, opponent1, opponent2):
    """
    Function that returns a move and decides on a strategy.
    :parameters: (early, mid, end) game, player, ....
    :returns: an action in format ("MOVE", ((q1, r2), (q2, r2)))
    """
    



    return ("MOVE", ((0, 0), (0, 1)))





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