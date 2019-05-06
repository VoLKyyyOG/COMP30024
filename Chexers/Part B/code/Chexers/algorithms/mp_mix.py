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
from math import inf

# User-defined files
from mechanics import possible_actions, apply_action, get_remaining_opponent
from moves import exit_action
from algorithms.heuristics import desperation

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
    print(f"\n\t\t\t\t\t\t\t\t* ||| Initial Evaluations {raw_scores} using {heuristic}")

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

    """ TWO PLAYER
    1. If the opponent has less than 2 exits AND our evaluation is greater than the defence threshold, then do a runner.
    :else: Default to a alpha-beta algorithm (implemented via paranoid function)
    """
    if two_player:
        possible_exits = exit_action(state, max_player)
        if state['exits'][max_player] == 3 and bool(possible_exits):
            return possible_exits[0]

        alive_opponent = get_remaining_opponent(state)
        
        if state["exits"][alive_opponent] < 2 and leader_edge >= defence_threshold:
            print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| DOING A DIJKSTRA AGAINST REMAINING PLAYER ")
            return False
                
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| ALPHA-BETA AGAINST REMAINING PLAYER | DEPTH = {TWO_PLAYER_MAX_DEPTH}")
        return paranoid(state, heuristic, max_player, depth_left=TWO_PLAYER_MAX_DEPTH)[1]

    """ 3 PLAYER
    1. If we are not the leader AND the leader has 2 exits AND we are in excess of pieces, then run a greedy algorithm.
    2. If we are not leader AND leader has 3 exits, then attempt to kill this player.
    3. If we are the leader AND our evaluation is greater than the defence threshold, then run a paranoid algorithm.
    4. If we are the rival AND our evaluation is greater than the offence threshold, then attack the leader.
    5. If we are the loser AND our second edge is greater than the defence threshold, then run a paranoid algorithm.
    6. If we are not the loser AND the loser has one piece remaining, then attempt to kill this player.

    :else: Default to a Maxn algorithm
    """
    if max_player != leader and state['exits'][leader] == 2 and desperation(state)[PLAYER_HASH[max_player]] > 0:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| WE ARE WITHIN REASON TO ATTEMPT A GREEDY APPROACH")
        return True

    if max_player != leader and state['exits'][leader] == 3:
        print(f"\n\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST 3 EXIT PLAYER {leader} | DEPTH = {KILL_DEPTH}")
        return directed_offensive(state, heuristic, max_player, leader, depth_left=KILL_DEPTH)[1]

    if max_player == leader and leader_edge >= defence_threshold:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| LEADER - USING PARANOID | DEPTH = {PARANOID_MAX_DEPTH}")
        return paranoid(state, heuristic, max_player, depth_left=PARANOID_MAX_DEPTH)[1]

    if max_player == rival and second_edge >= offence_threshold:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST LEADER {leader} | DEPTH = {MAX_DEPTH}")
        return directed_offensive(state, heuristic, max_player, leader, depth_left=MAX_DEPTH)[1]

    if max_player == loser and second_edge >= defence_threshold:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| LOSER - USING PARANOID | DEPTH = {PARANOID_MAX_DEPTH}")
        return paranoid(state, heuristic, max_player, depth_left=PARANOID_MAX_DEPTH)[1]

    if max_player != loser and len(state[loser]) == 1:
        print(f"\n\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST LOSER {loser} | DEPTH = {KILL_DEPTH}")
        return directed_offensive(state, heuristic, max_player, loser, depth_left=KILL_DEPTH)[1]

    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| DEFAULTING USING MAX_N | DEPTH = {MAX_DEPTH}")
    return max_n(state, heuristic, depth_left=MAXN_MAX_DEPTH)[1]

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