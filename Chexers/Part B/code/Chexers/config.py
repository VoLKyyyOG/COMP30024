"""
:filename: config.py
:summary: temporary file for keeping optimal weights for heuristics.
:authors: Akira Wang (913391), Callum Holmes (899251)
"""

def two_player_heuristics(state):
    evals = np.array([f(state) for f in [favourable_hexes, desperation]])
    weights = [1, 2]

    return np.array(sum(map(lambda x,y: x*y, evals, weights)))

def runner(state):
    evals = np.array([f(state) for f in [exit_hex, speed_demon, desperation, exits]])
    weights = [0.1, 0.5, 1, 10]

    return np.array(sum(map(lambda x,y: x*y, evals, weights)))

def killer(state):
    evals = np.array([f(state) for f in [no_pieces, achilles_vector]])
    weights = [1, 0.1]
    return np.array(sum(map(lambda x,y: x*y, evals, weights)))


##################################################################################################

def two_player_logic(state, heuristic, max_player, leader_edge, depth, defence_threshold=0):
    """
    MP-Mix 2 player strategy (no need to be offensive).
    :default: alpha_beta which will have a higher depth if sparse
    """
    alive_opponent = get_remaining_opponent(state)

    if desperation(state)[PLAYER_HASH[alive_opponent]] < 0 and leader_edge >= defence_threshold:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| WE ARE SIGNIFICANTLY AHEAD - DOING A RUNNER AGAINST OPPONENT")
        return False

    if sum(no_pieces(state)) < 8: # if more than 10 pieces on board
        depth = 4

    if sum(no_pieces(state)) < 6: # less than six pieces on board
        depth = 5

    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| ALPHA-BETA AGAINST REMAINING PLAYER USING TWO_PLAYER_HEURISTICS | DEPTH = {depth}")
    return alpha_beta(state, two_player_heuristics, max_player, depth_left=depth)[1]

def three_player_logic(state, max_player, heuristic, leader, rival, loser, defence_threshold=0, offence_threshold=0):
    global KILL_DEPTH, PARANOID_MAX_DEPTH

    # If we are the leader, we use a running heuristics which avoids conflict to the goal
    if max_player == leader:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| LEADER - USING PARANOID WITH RUNNER HEURISTICS | DEPTH = {PARANOID_MAX_DEPTH}")
        return paranoid(state, runner, max_player, depth_left=PARANOID_MAX_DEPTH)[1]

    # If we are the rival and the leader has excess pieces, we want to attack the leader
    if max_player == rival and desperation(state)[PLAYER_HASH[leader]] > 0:
        print(f"\n\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST LEADER USING KILLER HEURISTICS {leader} | DEPTH = {KILL_DEPTH}")
        return directed_offensive(state, killer , max_player, leader, depth_left=KILL_DEPTH)[1]

    # If we are the rival and we have excess pieces, we will attack the leader
    if max_player == rival and desperation(state)[PLAYER_HASH[max_player]] > 0:
        print(f"\n\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST LEADER USING KILLER HEURISTICS {leader} | DEPTH = {KILL_DEPTH}")
        return directed_offensive(state, killer , max_player, leader, depth_left=KILL_DEPTH)[1]

    # If we are the rival and we have just enough pieces to make do, we avoid conflict and run
    # NOTE: potential achilles + runner style heuristic
    if max_player == rival and desperation(state)[PLAYER_HASH[max_player]] > 0:
        print(f"\n\t\t\t\t\t\t\t\t* ||| USING DIRECTED OFFENSIVE AGAINST LEADER USING KILLER HEURISTICS {leader} | DEPTH = {KILL_DEPTH}")
        return directed_offensive(state, killer , max_player, leader, depth_left=KILL_DEPTH)[1]

    # If we are losing then we are desperate :^)
    if max_player == loser:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| LOSER - USING PARANOID USING DESPERATION HEURISTICS| DEPTH = {PARANOID_MAX_DEPTH}")
        return paranoid(state, desperation, max_player, depth_left=PARANOID_MAX_DEPTH)[1]

    # Otherwise, we will just use our default OP heuristic
    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| DEFAULTING TO PARANOID USING END_GAME_HEURISTICS | DEPTH = {PARANOID_MAX_DEPTH}")
    return paranoid(state, end_game_heuristic, max_player, depth_left=PARANOID_MAX_DEPTH)[1]
