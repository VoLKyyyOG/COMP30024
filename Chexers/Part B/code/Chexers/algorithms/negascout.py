from math import inf
from mechanics import *

def negascout(state, heuristic, alpha=-inf, beta=inf, depth_left=20):
    best_action = None

    if not depth_left:
        return heuristic(state, two_player=True)

    generated_actions = possible_actions(state, state["turn"], force_exit=False, force_capture=False)
    
    for action in generated_actions:
        new_state = apply_action(state, action)

        if action is generated_actions[0]: # if child is first child (IMPORTANT ORDERING)
            score = -negascout(new_state, heuristic, -beta, -alpha, depth_left-1)[0]
        else:
            score = -negascout(new_state, heuristic, -alpha-1, -alpha, depth_left-1)[0]
            if score > alpha and score < beta:
                score = -negascout(new_state, heuristic, -beta, -score, depth_left-1)[0]
    
        if score >= beta:
            return (beta, best_action)
        if score > alpha:
            alpha, best_action = score, action
        
        return (alpha, best_action)