""" heuristics.py

Stores heuristics for use in Chexers, or any other game. (Callum is a keen boy)

"""

########################### IMPORTS ##########################
# Standard modules
from queue import PriorityQueue as PQ
from math import inf
# User-defined files
from mechanics import *

######################### INDEPENDENT ########################
def goal_eval_for_minimax(state):
    """Returns +1 if maximisingPlayer wins, -1 if other player, or 0 for draw"""
    if game_over(state):
        if is_winner(state, state['turn']):
            return +1
        else:
            return -1
    else:
        return 0

########################### CHEXERS ##########################
def exit_diff_2_player(state):
    """Calculates as exits(self) - exits(only_remaining_opponent)"""
    if not state[state['turn']]:
        print("this shouldn't be happening...")
        return -inf
    else:
        opponent = [i for i in PLAYER_NAMES if state[i] and i != state['turn']].pop()
        return state['exits'][state['turn']] - state['exits'][opponent]

def exit_diff_3_player(state, maximisingPlayer, minimisingPlayer):
    """Temporary 3 player mp-mix heuristic"""
    if not state[state['turn']]:
        print("this shouldn't be happening...")
        return -inf
    else:
        return state['exits'][maximisingPlayer] - state['exits'][minimisingPlayer]

#### TODO: heuristic = exit_diff_3_player + number_of_pieces_captured + number_of_pieces_lost + retrograde_dijkstra
####       if we have more than 4 pieces, number_of_pieces_lost can have the smallest weighting
####       if we have less than 4 pieces, number_of_pieces_captured has the max weighting
####       exit_diff_3_player probably won't be that useful
####       retrograde_dijkstra will have a high weighting

def retrograde_dijkstra(state):
    """Computes minimal traversal distance to exit for all N players"""
    return [sum([dijkstra_board(state)[piece] for piece in player(state)]) for player in PLAYER_NAMES]

def dijkstra_board(state, colour):
    """Evaluates minimum cost to exit for each non-block position"""
    #### TODO: need to define valid_goals. Should be
    ####       GOALS[colour].difference(occupied) where occupied is
    ####       union of all opponent pieces
    occupied = set() # Stores enemy pieces
    for player in PLAYER_NAMES:
         if player != colour:
            valid_goals.difference_update(set(state[player]))
    valid_goals = set(GOALS[colour]).difference(occupied) # Stores empty goal positions

    visited = set() # Flags if visited or not
    cost = {x: INF for x in VALID_COORDINATES} # Stores costs
    cost.update({x:1 for x in valid_goals}) # Sets goals cost
    queue = PQ()

    # Add exits to queue to get it started
    for goal in valid_goals:
        queue.put((cost[goal], goal))

    # Loop over queue (dijsktra)
    while not queue.empty():
        curr_cost, curr = queue.get()
        if curr not in visited:
            visited.add(curr)
            poss_neighbours = set(move_action(state, occupied)).union(set(jump_action(state, occupied)))
            for new in poss_neighbours:
                est_cost = curr_cost + 1
                if est_cost < cost[new]: # Better path than previous
                    cost[new] = est_cost
                queue.put((cost[new], new))
    return cost
