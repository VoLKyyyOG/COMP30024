""" 
:filename: mp_mix.py
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
from copy import deepcopy
from math import inf

# User-defined files
from mechanics import *
from .heuristics import *
########################### GLOBALS ##########################
MAX_DEPTH = 3
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
    opponents = get_opponents(state)

    scores = {PLAYER_NAMES[i] : raw_scores[i] for i in range(N_PLAYERS)}
    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Hierarchy (colour, score)
    leader, rival, loser = scores[0][0], scores[1][0], scores[2][0]
    high, medium, low = scores[0][1], scores[1][1], scores[2][1]

    # Edges
    leader_edge = high - medium
    second_edge = medium - low

    if two_player:
        alive_opponent = [i for i in opponents if not is_dead(state, i)][0]
        if state["exits"][alive_opponent] < 2 and leader_edge >= 6: # at least 6 utility value ahead
            return False
                
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| ALPHA-BETA AGAINST REMAINING PLAYER | DEPTH = {MAX_DEPTH + 3}")
        return paranoid(state, heuristic, max_player, depth_left=MAX_DEPTH + 3)[1]

    """
    1. If we are the leader -> Paranoid given Defence Threshold
    2. If we are the rival -> Directed Offensive against the Leader given Offensive Threshold

    a) If a player has 3 exits -> Directed Offensive against that player
    b) If a player has 1 piece remaining -> Directed Offensive against that player

    :else: Default to a Maxn algorithm
    """
    if max_player == leader and leader_edge >= defence_threshold:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| USING PARANOID | DEPTH = {MAX_DEPTH}")
        return paranoid(state, heuristic, max_player, depth_left=MAX_DEPTH)[1]

    if max_player == rival and leader_edge > second_edge and leader_edge >= offence_threshold:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST LEADER {leader} | DEPTH = {MAX_DEPTH}")
        return directed_offensive(state, heuristic, max_player, leader, depth_left=MAX_DEPTH)[1]

    if len(state[loser]) == 1:
        print(f"\n\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST LOSER {loser} | DEPTH = {MAX_DEPTH}")
        return directed_offensive(state, heuristic, max_player, loser, depth_left=MAX_DEPTH)[1]
    
    if state["exits"][leader] == 3 and max_player != leader:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST PLAYER {leader} WITH 3 EXITS | DEPTH = {MAX_DEPTH}")
        return directed_offensive(state, heuristic, max_player, leader, depth_left=MAX_DEPTH)[1]

    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| USING MAX_N | DEPTH = {MAX_DEPTH}")
    return max_n(state, heuristic, depth_left=MAX_DEPTH)[1]

"""
Paranoid Implementation using Alpha-Beta Pruning
"""
def paranoid(state, heuristic, max_player, alpha=-inf, beta=inf, depth_left=MAX_DEPTH):
    if not depth_left:
        evals = heuristic(state)
        return (evals, None)

    best_action = None
    p = state["turn"]
    
    if p == max_player:
        generated_actions = possible_actions(state, p)

        for action in generated_actions:
            new_state = apply_action(state, action, ignore_dead=True)

            player_eval = paranoid(new_state, heuristic, max_player, alpha, beta, depth_left-1)[0]

            if player_eval[PLAYER_HASH[p]] > alpha:
                alpha, best_action = player_eval[PLAYER_HASH[p]], action

            if alpha >= beta:
                return (player_eval, best_action)

        return (player_eval, best_action)
    else:
        generated_actions = possible_actions(state, p)

        for action in generated_actions:
            
            new_state = apply_action(state, action, ignore_dead=True)
            
            player_eval = paranoid(new_state, heuristic, max_player, alpha, beta, depth_left-1)[0]

            if player_eval[PLAYER_HASH[p]] < beta:
                beta, best_action = player_eval[PLAYER_HASH[p]], action

            if alpha >= beta:
                return (player_eval, best_action)
            
        return (player_eval, best_action)

"""
Directed Offensive Implementation
"""
def directed_offensive(state, heuristic, max_player, target, depth_left=MAX_DEPTH):
    if not depth_left:
        evals = heuristic(state)
        return (evals, None)
    
    max_player_evals = [-inf]*N_PLAYERS
    best_action = None
    p = state["turn"]

    generated_actions = possible_actions(state, p)

    for action in generated_actions:
        new_state = apply_action(state, action, ignore_dead=True)

        player_eval = directed_offensive(new_state, heuristic, max_player, target, depth_left-1)[0]

        # If this is not us, we assume they will want to just maximise themselves
        if player_eval[PLAYER_HASH[p]] > max_player_evals[PLAYER_HASH[p]]:
            max_player_evals, best_action = player_eval, action
        
        # If this is us:
        if p == max_player:
            # If this new eval lowers our target eval, then update our path with this action
            # TODO: if -inf rip
            if player_eval[PLAYER_HASH[target]] < max_player_evals[PLAYER_HASH[target]]:
                max_player_evals, best_action = player_eval, action

    return (max_player_evals, best_action)

"""
Maxn (3-Player Minimax) Implementation
"""
def max_n(state, heuristic, depth_left=MAX_DEPTH):
    if not depth_left:
        evals = heuristic(state)
        return (evals, None)

    max_player_evals = [-inf]*N_PLAYERS
    best_action = None
    p = state["turn"]
    
    generated_actions = possible_actions(state, p)

    for action in generated_actions:
        new_state = apply_action(state, action, ignore_dead=True)

        player_eval = max_n(new_state, heuristic, depth_left-1)[0] # only take the vector of evaluations

        """ IMMEDIATE PRUNING (need to specify MAX_UTIL_VAL)
        if player_eval[PLAYER_HASH[p]] > MAX_UTIL_VAL:
            max_player_evals, best_action = player_eval, action
            return (max_player_evals, best_action)
        """

        if player_eval[PLAYER_HASH[p]] > max_player_evals[PLAYER_HASH[p]]:
            max_player_evals, best_action = player_eval, action
            
    return (max_player_evals, best_action)