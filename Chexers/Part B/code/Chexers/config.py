def end_game_heuristic(state):
    """
    Tribute to Marvel's End Game. This is the heuristic used for our mp-mix algorithm and holds a very high win rate on battlegrounds.
    """
    evals = np.array([f(state) for f in [desperation, speed_demon, favourable_hexes, exits]])
    weights = [1, 0.1, 1, 1.5]

    return np.array(sum(map(lambda x,y: x*y, evals, weights)))

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