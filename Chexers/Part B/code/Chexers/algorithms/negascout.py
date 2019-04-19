from math import inf
from mechanics import *

def negascout(state, heuristic, alpha=-inf, beta=inf, depth_left=6):
    """
    Guess what a found. A negamax variant that OUTPERFORMS alpha-beta if there is good move ordering.
    Guess what? We seem to have good order movering :^)

    Pseudocode adapted from:
    https://en.wikipedia.org/wiki/Principal_variation_search
    """
    if not depth_left: # terminal node or depth == 0
        return heuristic(state)
    generated_actions = possible_actions(state, state["turn"]) # possible actions
    for action in generated_actions:
        new_state = apply_action(state, action)

        if action is generated_actions[0]: # if child is first child (IMPORTANT ORDERING)
            score = -negascout(new_state, heuristic, -beta, -alpha, depth_left-1)
        else:
            score = -negascout(new_state, heuristic, -alpha-1, -alpha, depth_left-1) # search with a null window
            if score > alpha and score < beta:
                score = -negascout(new_state, heuristic, -beta, -score, depth_left-1) # if it failed high, do a full re-search
        alpha = max(alpha, score)
        if alpha >= beta:
            return beta
        return alpha