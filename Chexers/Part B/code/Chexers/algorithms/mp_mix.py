""" 
:filename: mp_mix.py
:summary: Defines the core structure of an MP-MIX agent
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""

########################### IMPORTS ##########################
# Standard modules
from copy import deepcopy
from math import inf
from collections import OrderedDict

# User-defined files
from mechanics import *
from .heuristics import *
from .negascoutanoid import negascoutanoid
from .directed import directed_offensive
from .max_n import max_n

"""
Concept adapted from:
The MP-MIX algorithm: Dynamic Search Strategy Selection in Multi-Player Adversarial Search

Authors:
Inon Zuckerman, Ariel Felner

Implemented by:
Akira Wang, Callum Holmes

Current Agent Strategy:
If we are leader:
1. if a player has 1 piece we can eliminate them (within a close radius and heuristic?)
2. else we will paranoid

If not leader:
1. if a player has 2 or less pieces we can attempt to eliminate
2. else we attack leader

If offence or defence threshold not met:
1. revert to maxn strategy
"""

def mp_mix(state, heuristic, defence_threshold = 0, offence_threshold = 0):
    """
    If defence_threshold = offence_threshold = 0, it will degenerate to:
    1. Paranoid when winning
    2. Offensive when losing
    """
    # Heuristic scores for each player
    raw_scores = heuristic(state) # 3-player heuristics should output vectors
    print(f"\n\t\t\t\t\t\t\t\t* ||| Initial Evaluations {raw_scores}")

    # List of opponents, irrespective of whether they are dead
    turn_player = player(state)
    opponents = get_opponents(state)

    all_dead = sum([is_dead(state,i) for i in opponents]) == 2

    # Defines tuples (colour/name, score) in an OrderedDict
    scores = {PLAYER_NAMES[i] : raw_scores[i] for i in range(N_PLAYERS)}
    """ # this is broken
    scores = OrderedDict(sorted(scores.items(),
        reverse=True, key=lambda x: sorted(x, reverse=True)))
    """

    # Hierarchy
    leader, rival, loser = scores.keys()
    high, medium, low = scores.values()

    # Edges
    leader_edge = high - medium
    rival_edge = medium - low

    # Strategy. Consider functionalising choose_directed(), choose_offence()
    # AI is just if statements change my mind.
    # Defaults. max_n = directed offensive = 3, negascoutanoid = 16

    # If we don't have enough pieces to exit 4 overall
    if all_dead:
        print("\n\t\t\t\t\t\t\t\t* ||| ALL DEAD. GOTTA MAKE IT TO THE GOAL NOW")
        # return dijkstra

    if len(state[turn_player]) < desperation(state, turn_player):
        print("\n\t\t\t\t\t\t\t\t* ||| TIME TO CAPTURE A PIECE")
        print(turn_player, desperation(state, turn_player))
        op1 = directed_offensive(state, heuristic, turn_player, opponents[0], depth_left=2)
        op2 = directed_offensive(state, heuristic, turn_player, opponents[1], depth_left=2)
        # Check which one maximises us more
        return op1[1] if op1[0] > op2[0] else op2[1]

    # If we are not the loser, then attempt to capture with a slightly higher threshold
    if turn_player != leader and len(state[loser]) == 1 and len(state[loser]) > 0:
        print("\n\t\t\t\t\t\t\t\t* ||| A TARGET HAS ONE PIECE REMAINING")
        return directed_offensive(state, heuristic, turn_player, loser, depth_left=4)[1]

    # If we are the leader, then we can paranoid our way out (runner)
    if turn_player == leader and leader_edge >= defence_threshold:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| USING PARANOID")
        return negascoutanoid(state, heuristic, depth_left=20)[1]
    
    # If we are the rival player against the leader then attack them
    if turn_player == rival and leader_edge > rival_edge:
        print("\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE")
        return directed_offensive(state, heuristic, turn_player, leader)[1]

    # Otherwise, we just default to using max_n
    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| USING MAX_N")
    return max_n(state, heuristic, depth_left=4)[1]
