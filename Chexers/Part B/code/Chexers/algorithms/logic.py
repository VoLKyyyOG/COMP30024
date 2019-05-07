""" 
:filename: logic.py
:summary: Defines the core structure of an MP-MIX agent
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)

Concept adapted from:
The MP-MIX algorithm: Dynamic Search Strategy Selection in Multi-Player Adversarial Search

Authors:
Inon Zuckerman, Ariel Felner

:thresholds: If defence_threshold or offence_threshold are 0, it will degenerate to:
             1. Paranoid when winning
             2. Offensive when losing
:strategy: Determine whether the agent should be paranoid (1 vs all), maxn (everyone will maximise themself), offence (minimise a target)
"""

"""BATTLEGROUND LOSS LOGS
1. we are close to goal and neglect a piece that is far out. opponent then captures that piece and wins the game
2. AGAINST THIS SUPER BEAST PLAYER "3" - we have a W/L of 1/5
"""
########################### IMPORTS ##########################

# Standard modules
from math import inf

# User-defined files
from mechanics import get_remaining_opponent
from moves import exit_action

from algorithms.heuristics import desperation, can_exit
from algorithms.adversarial_algorithms import negamax, paranoid, directed_offensive, max_n

# Global Imports
from mechanics import PLAYER_NAMES, PLAYER_HASH, N_PLAYERS

########################### GLOBALS ##########################

MAX_DEPTH = 3
KILL_DEPTH = 4
MAXN_MAX_DEPTH = 3
PARANOID_MAX_DEPTH = 5
TWO_PLAYER_MAX_DEPTH = 5
MAX_UTIL_VAL = 6 # TODO: Calculate a max utility value!

##############################################################
"""
MP-Mix Core Implementation
"""
def mp_mix(state, heuristic, defence_threshold = 0, offence_threshold = 0, two_player = False):
    # Heuristic scores for each player
    raw_scores = heuristic(state) # 3-player heuristics should output vectors
    print(f"\n\t\t\t\t\t\t\t\t* ||| Initial Evaluations {raw_scores}")

    # List of opponents, irrespective of whether they are dead
    max_player = state["turn"]

    scores = {PLAYER_NAMES[i] : raw_scores[i] for i in range(N_PLAYERS)}
    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Hierarchy (colour, score)
    leader, rival, loser = scores[0][0], scores[1][0], scores[2][0]
    high, medium, low = scores[0][1], scores[1][1], scores[2][1]

    # Edges
    leader_edge = high - medium
    second_edge = medium - low

    possible_exits = exit_action(state, max_player)
    if state['exits'][max_player] < len(possible_exits) or state['exits'][max_player] == 3 and len(possible_exits) > 0:
        return possible_exits[0]

    """ TWO PLAYER
    :else: Default to a alpha-beta algorithm (implemented via paranoid function)
    """
    if two_player:
        alive_opponent = get_remaining_opponent(state)

        if desperation(state)[PLAYER_HASH[alive_opponent]]  < 0 and leader_edge >= 10: # defence_threshold (threshold=10 is very large)
            print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| DOING A DIJKSTRA AGAINST REMAINING PLAYER ")
            return False
        if sum([len([i for i in state[player]]) for player in PLAYER_NAMES]) < 6:
            global TWO_PLAYER_MAX_DEPTH
            TWO_PLAYER_MAX_DEPTH = 7
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| NEGAMAX AGAINST REMAINING PLAYER | DEPTH = {TWO_PLAYER_MAX_DEPTH}")
        return negamax(state, heuristic, max_player, depth_left=TWO_PLAYER_MAX_DEPTH)[1]

    """ 3 PLAYER
    :else: Default to a Maxn algorithm
    """

    if max_player != leader and state['exits'][leader] == 3:
        print(f"\n\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST 3 EXIT PLAYER {leader} | DEPTH = {KILL_DEPTH}")
        return directed_offensive(state, heuristic, max_player, leader, depth_left=KILL_DEPTH)[1]

    if max_player == leader:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| LEADER - USING PARANOID | DEPTH = {PARANOID_MAX_DEPTH}")
        return paranoid(state, heuristic, max_player, depth_left=PARANOID_MAX_DEPTH)[1]

    if max_player == rival and desperation(state)[PLAYER_HASH[max_player]] > 0:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST LEADER {leader} | DEPTH = {KILL_DEPTH}")
        return directed_offensive(state, heuristic, max_player, leader, depth_left=KILL_DEPTH)[1]

    if max_player == loser:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| LOSER - USING PARANOID | DEPTH = {PARANOID_MAX_DEPTH}")
        return paranoid(state, heuristic, max_player, depth_left=PARANOID_MAX_DEPTH)[1]

    if max_player == rival and len(state[loser]) == 1 and state['exits'][leader] < 3:
        print(f"\n\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST 1 PIECE LOSER {loser} | DEPTH = {KILL_DEPTH}")
        return directed_offensive(state, heuristic, max_player, loser, depth_left=KILL_DEPTH)[1]

    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| DEFAULTING USING MAX_N | DEPTH = {MAXN_MAX_DEPTH}")
    return max_n(state, heuristic, depth_left=MAXN_MAX_DEPTH)[1]