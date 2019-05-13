def favourable_hexes(state):
    """
    Favourable hex positions:
    1. Corner hexes
    2. Enemy exit hex positions
    """
    corner_hex = [len(set(state[player]).intersection(CORNER_SET)) for player in PLAYER_NAMES]
    block_exit_hex = [len(set(state[player]).intersection(OPPONENT_GOALS[player])) for player in PLAYER_NAMES]

    return sum([np.array(eval) for eval in [corner_hex, block_exit_hex]])
def end_game_heuristic(state):
    """
    Tribute to Marvel's End Game.
    A very well thought out heuristic after several simulations and runs.
    :eval: number of piece in excess + distance + favourable hex positions + number of exits + number of capturable pieces
    :priorities: number of pieces in excess and exits, but will lean towards a favourable hex over distance and attempt to minimise
                 the number of capturable pieces.
    """
    evals = np.array([f(state) for f in [desperation, speed_demon, favourable_hexes, exits, achilles_real]])
    weights = [1, 0.2, 0.1 , 2.5, 0.25]

    return np.array(sum(map(lambda x,y: x*y, evals, weights)))

def two_player_heuristics(state):
    evals = np.array([f(state) for f in [desperation, speed_demon, favourable_hexes, exits, achilles_real]])
    weights = [2, 0.4, 0.05, 5, 0.5]

    return np.array(sum(map(lambda x,y: x*y, evals, weights)))