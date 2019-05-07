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

KILL_DEPTH = 4
MAXN_MAX_DEPTH = 3
PARANOID_MAX_DEPTH = 5
TWO_PLAYER_MAX_DEPTH = 5
MAX_UTIL_VAL = 10 # TODO: Calculate a max utility value! For now, this is the equivalent of a "free" exit (worth 10 points)

##############################################################
"""
MP-Mix Core Implementation
"""
def mp_mix(state, heuristic, defence_threshold = 0, offence_threshold = 0, two_player = False):
    # The max_player (us)
    max_player = state["turn"]

    leader, rival, loser, leader_edge, second_edge = score(state, heuristic)

    exit_action, possible = force_exit(state, max_player)
    if possible:
        return exit_action

    if two_player:
        return two_player_logic(state, heuristic, max_player, leader_edge, depth=TWO_PLAYER_MAX_DEPTH, defence_threshold=MAX_UTIL_VAL)
    else:
        return three_player_logic(state, max_player, heuristic, leader, rival, loser, defence_threshold, offence_threshold)

def score(state, heuristic):
    """
    Function which ranks players by their initial heuristic evaluation
    """
    evals = heuristic(state)
    print(f"\n\t\t\t\t\t\t\t\t* ||| Initial Evaluations {evals}")
        
    scores = {PLAYER_NAMES[i] : evals[i] for i in range(N_PLAYERS)}
    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    leader, rival, loser = scores[0][0], scores[1][0], scores[2][0]
    high, medium, low = scores[0][1], scores[1][1], scores[2][1]   

    leader_edge = high - medium
    second_edge = medium - low

    return leader, rival, loser, leader_edge, second_edge

def force_exit(state, max_player):
    """
    Forces our algorithm to exit if we have 3 pieces and we have an exit piece!
    """
    possible_exits = exit_action(state, max_player)

    if state['exits'][max_player] < len(possible_exits) or state['exits'][max_player] == 3 and len(possible_exits) > 0:
        return (possible_exits[0], True)
    return (None, False)

def two_player_logic(state, heuristic, max_player, leader_edge, depth, defence_threshold=0):
    """
    MP-Mix 2 player strategy (no need to be offensive).
    :default: negamax which will have a higher depth if sparse
    """
    alive_opponent = get_remaining_opponent(state)

    if desperation(state)[PLAYER_HASH[alive_opponent]] < 0 and leader_edge >= defence_threshold:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| WE ARE SIGNIFICANTLY AHEAD - DOING A RUNNER AGAINST OPPONENT")
        return False

    if sum([len([i for i in state[player]]) for player in PLAYER_NAMES]) < 6: # less than six pieces on board
        depth = 7

    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| NEGAMAX AGAINST REMAINING PLAYER | DEPTH = {depth}")
    return negamax(state, heuristic, max_player, depth_left=depth)[1]

def three_player_logic(state, max_player, heuristic, leader, rival, loser, defence_threshold = 0, offence_threshold = 0):
    global KILL_DEPTH, PARANOID_MAX_DEPTH, MAXN_MAX_DEPTH

    if max_player != leader and state['exits'][leader] >= 2:
        print(f"\n\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST 2+ EXIT PLAYER {leader} | DEPTH = {KILL_DEPTH}")
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

    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| DEFAULTING TO MAX_N | DEPTH = {MAXN_MAX_DEPTH}")
    return max_n(state, heuristic, depth_left=MAXN_MAX_DEPTH)[1]