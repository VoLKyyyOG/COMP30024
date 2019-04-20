""" heuristics.py

Stores heuristics for use in Chexers, or any other game. (Callum is a keen boy)

"""

########################### IMPORTS ##########################
# Standard modules
from queue import PriorityQueue as PQ
from collections import defaultdict
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

def exits(state):
    """Returns raw exit count as a tuple"""
    return [state['exits'][player] for player in PLAYER_NAMES]

def desperation(state):
    """Returns deficit/surplus in pieces vs exit"""
    # How many pieces available - how many pieces needed to win
    return [len(state[player]) - (MAX_EXITS - state['exits'][player]) for player in PLAYER_NAMES]

def paris_vector(state):
    """
    paris_heuristic returns the number of capturing actions possible for each player.
    :returns: [val_red, val_green, val_blue]
    """
    raw = paris(state)
    return [len(raw[player]) for player in PLAYER_NAMES]

def paris(state):
    """
    Evaluates captures that each player could perform
    :returns: {player: list_of_capturing_actions for each player}
    """
    captures = defaultdict(list)
    for player in PLAYER_NAMES:
        for action in possible_actions(state):
            flag, pieces = action
            if flag == "JUMP" and is_capture(state, action, player):
                captures[player].append(action)
    return captures

def achilles_vector(state, reality=False):
    """
    achilles_vector returns the number of threats for each player.
    :FLAG reality: if True, counts actual opponents that could capture
    :returns: [val_red, val_green, val_blue]
    """
    raw = achilles(state, reality)
    return [len(raw[player]) for player in PLAYER_NAMES]

def achilles(state, reality=False):
    """
    Evaluates number of attackable angles on your pieces.
    :FLAG reality: True only returns actual about-to-kill-you opponents
    Ranges from 0 (all pieces in corners) to 6*N (all N pieces are isolated and not on an edge)
    """
    #### TODO: Make sure it works

    threats = defaultdict(set)
    for player in PLAYER_NAMES:
        # All opponent pieces
        if reality:
            occupied = occupied(state, get_opponents(player))

        for piece in state[player]:
            possible_axes = POSSIBLE_DIRECTIONS[:3] # Three directions
            for diagonal in possible_axes:
                threat_1, threat_2 = add(piece, diagonal), sub(piece, diagonal)
                # Only a threat if the diagonal is fully empty, and does not have your own pieces
                if (threat_1, threat_2) in VALID_COORDINATES and (threat_1, threat_2) not in state[player]:
                    if reality:
                        if threat_1 in occupied:
                            threats[player].add(threat_1)
                        if threat_2 in occupied:
                            threats[player].add(threat_2)
                    else:
                        threats[player].update(set(threat_1, threat_2))
    return threats

def speed_demon(state):
    """
    Heuristic that uses uses a relaxed version of the game board by assuming a piece can always jump with or without a piece.
    The average is taken so that the player progression can be compared

    TODO: Coordinates must be then transformed so that changes in displacement
    evaluation do not outweigh the benefit of having exited a piece.

    TODO: Breaks when there is a dead player and it is used as a heuristic. 
    """

    total_disp = lambda player: sum([get_cubic(piece)[PLAYER_HASH[player]] -
        MAX_COORDINATE_VAL for piece in state[player]])

    # Return average displacement, adding 0.5 to deal with dead players
    return [total_disp(player) / (len(state[player]) + 0.5) for player in PLAYER_NAMES]

def exit_diff_2_player(state):
    """Calculates as exits(self) - exits(only_remaining_opponent)"""
    if not state[state['turn']]: # Checks if you are dead already
        return -inf
    else:
        opponent = get_opponents(state).pop()
        return state['exits'][state['turn']] - state['exits'][opponent]

def exit_diff_3_player(state, maximisingPlayer, minimisingPlayer):
    """Temporary 3 player mp-mix heuristic"""
    if not state[state['turn']]:
        print(f"EXIT_DIFF_3_PLAYER ERROR: I, {state['turn']} am dead - I have {state[state['turn']]} pieces..")
        return -inf
    else:
        if maximisingPlayer == minimisingPlayer: # this is us so return number of exits
            return state['exits'][maximisingPlayer]
        return state['exits'][maximisingPlayer] - state['exits'][minimisingPlayer]

#### TODO: heuristic = exit_diff_3_player + number_of_pieces_captured + number_of_pieces_lost + retrograde_dijkstra
####       if we have more than 4 pieces, number_of_pieces_lost can have the smallest weighting
####       if we have less than 4 pieces, number_of_pieces_captured has the max weighting
####       exit_diff_3_player probably won't be that useful
####       retrograde_dijkstra will have a high weighting

# def retrograde_dijkstra(state):
#     """Computes minimal traversal distance to exit for all N players"""
#     return [sum([dijkstra_board(state, player(state))[piece] for piece in player(state)]) for player in PLAYER_NAMES]

def dijkstra_board(state, colour):
    """Evaluates minimum cost to exit for each non-block position"""
    #### TODO: Given dynamic board, forcing 'moves only' i.e. jump_heuristic may be more accurate
    #### Otherwise this is a forward unto death greedy heuristic
    occupied = set() # Stores enemy pieces
    for player in PLAYER_NAMES:
         if player != colour:
            valid_goals.difference_update(set(state[player]))
    valid_goals = set(GOALS[colour]).difference(occupied) # Stores empty goal positions

    visited = set() # Flags if visited or not
    cost = {x: inf for x in VALID_COORDINATES} # Stores costs
    cost.update({x: 1 for x in valid_goals}) # Sets goals cost
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
