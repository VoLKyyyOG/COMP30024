"""
:filename: logic.py
:summary: Defines the core structure of an MP-MIX agent
:authors: Akira Wang (913391), Callum Holmes (899251)

Concept adapted from:
The MP-MIX algorithm: Dynamic Search Strategy Selection in Multi-Player Adversarial Search

Authors:
Inon Zuckerman, Ariel Felner

:thresholds: If defence_threshold or offence_threshold are 0, it will degenerate to:
             1. Paranoid when winning
             2. Offensive when losing
:strategy: Determine whether the agent should be paranoid (1 vs all), maxn (everyone will maximise themself), offence (minimise a target)
"""

# TODO NOTE: potential custom eval functions that are fixed given mp-mix logic (rather than passing a single heuristic)

########################### IMPORTS ##########################

# Standard modules
from math import inf
from pprint import pprint

# User-defined files
from mechanics import get_remaining_opponent, function_occupied
from moves import exit_action, capture_jumps

from algorithms.heuristics import *
from algorithms.adversarial_algorithms import alpha_beta, paranoid, directed_offensive, max_n

# Global Imports
from mechanics import PLAYER_NAMES, PLAYER_HASH, N_PLAYERS

########################### GLOBALS ##########################

KILL_DEPTH = 3
PARANOID_MAX_DEPTH = 3
TWO_PLAYER_MAX_DEPTH = 5
MAX_UTIL_VAL = 10 # TODO: Calculate a max utility value! For now, this is the equivalent of a "free" exit (worth 10 points)

##############################################################
"""
MP-Mix Core Implementation
"""
def mp_mix(state, heuristic, defence_threshold=0, offence_threshold=0, two_player=False):
    """
    Main function for MP-Mix.
    :strategy: Always returns exits if we are way ahead (force_exit)
                Otherwise pulls logic of 2/3 player game depending on state
    :return: vector of valuations
    """
    
    # The max_player (us)
    max_player = state["turn"]

    leader, rival, loser, leader_edge, second_edge = score(state, heuristic)

    move, possible = winning_move(state, max_player, two_player)
    if possible:
        print("\t\t\t\t\t\t\t\t\t\t\t\t* ||| FREE WIN!")
        return move

    if two_player:
        return two_player_logic(state, heuristic, max_player, leader_edge, depth=TWO_PLAYER_MAX_DEPTH, defence_threshold=MAX_UTIL_VAL)
    else:
        return three_player_logic(state, max_player, heuristic, leader, rival, loser, defence_threshold, offence_threshold)

def score(state, heuristic):
    """
    Function which ranks players by their initial heuristic evaluation
    :return: best, mid and worst scores, as well as margins
    """
    evals = heuristic(state)
    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| Initial Evaluations {evals}")

    scores = {PLAYER_NAMES[i] : evals[i] for i in range(N_PLAYERS)}
    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    leader, rival, loser = scores[0][0], scores[1][0], scores[2][0]
    high, medium, low = scores[0][1], scores[1][1], scores[2][1]

    leader_edge = high - medium
    second_edge = medium - low

    return leader, rival, loser, leader_edge, second_edge

def winning_move(state, max_player, two_player=False):
    possible_exits = exit_action(state, max_player)
    if state['exits'][max_player] == 3 and len(possible_exits) > 0:
        return (possible_exits[0], True)
    
    if two_player:
        alive_opponent = get_remaining_opponent(state)
        occupied_hexes = function_occupied(state, PLAYER_NAMES)
        print(occupied_hexes)
        captures = capture_jumps(state, occupied_hexes, max_player)
        if len(state[alive_opponent]) == 1 and len(captures) > 0:
            return (captures[0], True)
    return (None, False)

def two_player_logic(state, heuristic, max_player, leader_edge, depth, defence_threshold=0):
    """
    MP-Mix 2 player strategy (no need to be offensive).
    :default: alpha_beta which will have a higher depth if sparse
    """
    alive_opponent = get_remaining_opponent(state)

    if desperation(state)[PLAYER_HASH[alive_opponent]] < 0 and leader_edge >= defence_threshold:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| WE ARE SIGNIFICANTLY AHEAD - DOING A RUNNER AGAINST OPPONENT")
        return False

    if sum(no_pieces(state)) >= 10: # if more than 10 pieces on board
        depth = 3

    if sum(no_pieces(state)) < 6: # less than six pieces on board
        depth = 7

    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| ALPHA-BETA AGAINST REMAINING PLAYER | DEPTH = {depth}")
    pprint([i(state) for i in [desperation, speed_demon, favourable_hexes, exits, no_pieces]])
    return alpha_beta(state, heuristic, max_player, depth_left=depth)[1]

def three_player_logic(state, max_player, heuristic, leader, rival, loser, defence_threshold=0, offence_threshold=0):
    global KILL_DEPTH, PARANOID_MAX_DEPTH

    if max_player != leader and desperation(state)[PLAYER_HASH[leader]] > 0:
        print(f"\n\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST 2+ EXIT PLAYER {leader} | DEPTH = {KILL_DEPTH}")
        pprint([i(state) for i in [no_pieces, achilles_vector]])
        return directed_offensive(state, killer , max_player, leader, depth_left=KILL_DEPTH)[1]
        # value capturing leader pieces

    if max_player == leader:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| LEADER - USING PARANOID | DEPTH = {PARANOID_MAX_DEPTH}")
        pprint([i(state) for i in [can_exit, speed_demon, no_pieces]])
        return paranoid(state, runner, max_player, depth_left=PARANOID_MAX_DEPTH)[1]
        # value running to goal and not losing pieces

    if max_player == rival and desperation(state)[PLAYER_HASH[max_player]] > 0:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST LEADER {leader} | DEPTH = {KILL_DEPTH}")
        return directed_offensive(state, end_game_heuristic, max_player, leader, depth_left=KILL_DEPTH)[1]
        # value minimising leader pieces

    if max_player == loser:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| LOSER - USING PARANOID | DEPTH = {PARANOID_MAX_DEPTH}")
        pprint(desperation)
        return paranoid(state, desperation, max_player, depth_left=PARANOID_MAX_DEPTH)[1]
        # value getting desperation back up to 0 (so directed_offensive rather than paranoid)

    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| DEFAULTING TO PARANOID | DEPTH = {PARANOID_MAX_DEPTH}")
    return paranoid(state, end_game_heuristic, max_player, depth_left=PARANOID_MAX_DEPTH)[1]
    # default to end_game_heuristics