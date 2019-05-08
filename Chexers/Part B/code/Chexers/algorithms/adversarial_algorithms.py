"""
:filename: adversarial_algorithms.py
:summary: Defines all adversarial search algorithms
:authors: Akira Wang (913391), Callum Holmes (899251)

ADVERSARIAL SEARCH ALGORITHMS:
1. Negamax - for 2 player states
2. Paranoid - for 3 player states
3. Directed Offensive - for 3 player states
4. Max^n - the most useless algorithm ever
"""
########################### IMPORTS ##########################

# Standard modules
from math import inf

# User-defined files
from mechanics import possible_actions, apply_action

# Global Imports
from mechanics import PLAYER_HASH, N_PLAYERS

MAX_DEPTH = 3

##############################################################

def alpha_beta(state, heuristic, max_player, alpha=-inf, beta=inf, depth_left=MAX_DEPTH):

    if not depth_left:
        evals = heuristic(state)
        return (evals, None)

    best_action = None
    player = state["turn"]
    index = PLAYER_HASH[player]

    generated_actions = possible_actions(state, player)
    for action in generated_actions:
        new_state = apply_action(state, action, ignore_dead=True)
        player_eval = alpha_beta(new_state, heuristic, max_player, alpha, beta, depth_left-1)[0]

        if (player == max_player):
            # MaximisingPlayer wants to maximise alpha
            if player_eval[index] > alpha:
                alpha, best_action = player_eval[index], action

        # MinimisingPlayer wants to worsen beta
        elif player_eval[index] < beta:
            beta, best_action = player_eval[index], action

        if alpha >= beta:
            return (player_eval, best_action)
    return (player_eval, best_action)

def paranoid(state, heuristic, max_player, alpha=-inf, beta=inf, depth_left=MAX_DEPTH):
    """
    Paranoid assuming a 1 vs rest scenario. Used when winning / losing given a certain threshold.
    The implementation also uses alpha-beta pruning, with the assumption of good ordering.
    """
    if not depth_left:
        evals = heuristic(state)
        return (evals, None)

    best_action = None
    player = state["turn"]
    index = PLAYER_HASH[player]

    generated_actions = possible_actions(state, player)
    for action in generated_actions:
        new_state = apply_action(state, action)
        player_eval = paranoid(new_state, heuristic, max_player, alpha, beta, depth_left-1)[0]

        if (player == max_player):
            # MaximisingPlayer wants to maximise alpha
            if player_eval[index] > alpha:
                alpha, best_action = player_eval[index], action

        # MinimisingPlayer wants to worsen beta
        elif player_eval[index] < beta:
            beta, best_action = player_eval[index], action

        if alpha >= beta:
            return (player_eval, best_action)
    return (player_eval, best_action)

def directed_offensive(state, heuristic, max_player, target, min_eval=inf, depth_left=MAX_DEPTH):
    """
    An algorithm aimed to MINIMISE a target player used in a 3 player scenario with no good pruning techniques possible.
    It will assume that all players will wish to maximise themselves (like a typical Max^n algorithm) but if we find an evaluation
    that minimises a target's evaluation and it is still beneficial to us, that becomes our "best action".
    """
    if not depth_left:
        evals = heuristic(state)
        return (evals, None)

    max_player_evals = [-inf]*N_PLAYERS
    best_action = None
    player = state["turn"]
    index = PLAYER_HASH[player]
    target_index = PLAYER_HASH[target]

    generated_actions = possible_actions(state, player, sort=(player==max_player))
    for action in generated_actions:
        new_state = apply_action(state, action)
        player_eval = directed_offensive(new_state, heuristic, max_player, target, min_eval, depth_left-1)[0]

        if player != max_player:

            # We are NOT the max_player 
            # If this is not us, we assume they will want to just maximise themselves
            if player_eval[index] > max_player_evals[index]:
                max_player_evals, best_action = player_eval, action
        else:
            # If this new eval LOWERS our target eval and our eval is NOT WORSE, then update our path with this action
            if player_eval[target_index] < min_eval and player_eval[index] >= max_player_evals[index]:
                max_player_evals, best_action, min_eval = player_eval, action, player_eval[target_index]

    return (max_player_evals, best_action)

#### DEPRECIAITED
def negamax(state, heuristic, max_player, alpha=-inf, beta=inf, depth_left=MAX_DEPTH):
    raise NotImplementedError
    """
    Simple yet effective implementation of Negamax with alpha-beta pruning.
    The possible moves functions will always return good ordering for optimal pruning.
    Assumes a player is dead - hence the game is merely 2-player.
    """

    if not depth_left:
        evals = heuristic(state)[PLAYER_HASH[max_player]]
        return (-evals, None)

    best_action = None
    p = state["turn"]

    for action in possible_actions(state, p):
        new_state = apply_action(state, action, ignore_dead=True)

        new_eval = -negamax(new_state, heuristic, max_player, -beta, -alpha, depth_left - 1)[0]

        if new_eval >= beta:
            return (beta, best_action)

        if new_eval > alpha:
            alpha, best_action = new_eval, action

    return (alpha, best_action)

def max_n(state, heuristic, depth_left=MAX_DEPTH):
    raise NotImplementedError
    """
    Max^N. A 3 player variant of minimax with no good pruning techniques available.
    Pretty useless and it isn't really called at all during our game.
    """
    if not depth_left:
        evals = heuristic(state)
        return (evals, None)

    max_player_evals = [-inf]*N_PLAYERS
    best_action = None
    player = state["turn"]
    index = PLAYER_HASH[player]

    generated_actions = possible_actions(state, player)

    for action in generated_actions:
        new_state = apply_action(state, action)
        player_eval = max_n(new_state, heuristic, depth_left-1)[0] # only take the vector of evaluations

        """ IMMEDIATE PRUNING (need to specify MAX_UTIL_VAL)
        if player_eval[PLAYER_HASH[p]] > MAX_UTIL_VAL:
            max_player_evals, best_action = player_eval, action
            return (max_player_evals, best_action)
        """

        if player_eval[index] > max_player_evals[index]:
            max_player_evals, best_action = player_eval, action

    return (max_player_evals, best_action)
