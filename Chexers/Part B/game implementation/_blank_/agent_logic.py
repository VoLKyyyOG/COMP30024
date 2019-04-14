"""
Team: _blank_ 
player.py to hold our player class
"""
# Import Dependencies
from .moves import *
# from .agent_early_game import *
# from .agent_mid_game import *
# from .agent_endgame import *

"""
Agent Random - Picks a random move
??? Agent Runner - Uses IDA* to go to the goal as fast as possible
Agent Early Game - Monte Carlo / Book Learning
Agent Mid Game - Max^n, Paranoid, Directed Offence
Agent Endgame - Minimax
"""

# Import Libraries
from random import choice

# Global Variables

# Functions

def agent_logic(player, random=False):
    """
    Function that returns a move and decides on a strategy.
    :parameters: (early, mid, end) game, player, ....
    :returns: an action in format ("MOVE", ((q1, r2), (q2, r2)))
    """
    two_player = False
    early_game = True
    mid_game = False

    if random:
        possible_actions = find_possible_actions(player)
        action = choice(possible_actions)
    elif not two_player and early_game:
        actions = book_learning(player)
        action = choice(actions)
    elif not two_player and mid_game:
        action = mp_mix(player)
    else:
        action = minimax(player)
        
    return action