from math import inf
from mechanics import *

def negascout(state, heuristic, alpha=-inf, beta=inf, depth_left=6):
    """
    Guess what a found. A negamax variant that OUTPERFORMS alpha-beta if there is good move ordering.
    Guess what? We seem to have good order movering :^)

    Pseudocode adapted from:
    https://en.wikipedia.org/wiki/Principal_variation_search

    function pvs(node, depth, α, β, color) is
        if depth = 0 or node is a terminal node then
            return color × the heuristic value of node
        for each child of node do
            if child is first child then
                score := −pvs(child, depth − 1, −β, −α, −color)
            else
                score := −pvs(child, depth − 1, −α − 1, −α, −color) (* search with a null window *)
                if α < score < β then
                    score := −pvs(child, depth − 1, −β, −score, −color) (* if it failed high, do a full re-search *)
            α := max(α, score)
            if α ≥ β then
                break (* beta cut-off *)
        return α
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