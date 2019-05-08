if two_players_left(state): # if it is two player
    evals = np.array([f(state) for f in [desperation, speed_demon, can_exit, exits]])
    weights = [2, 0.1, 1, 10]
else:
    evals = np.array([f(state) for f in [desperation, speed_demon, favourable_hexes, exits, no_pieces]])
    weights = [1, 0.1, 0.1, 2, 1]
return np.array(sum(map(lambda x,y: x*y, evals, weights)))


if two_players_left(state): # if it is two player
    evals = np.array([f(state) for f in [desperation, speed_demon, can_exit, exits]])
    weights = [2, 0.1, 1, 10]
else:
    evals = np.array([f(state) for f in [speed_demon, favourable_hexes, achilles_vector, no_pieces, exits]])
    weights = [1, 0.1, 0.5, 1, 10]
return np.array(sum(map(lambda x,y: x*y, evals, weights)))


if two_players_left(state): # if it is two player
    evals = np.array([f(state) for f in [troll, no_pieces]])
    weights = [5,1]
else:
    evals = np.array([f(state) for f in [speed_demon, favourable_hexes, achilles_vector, no_pieces, exits]])
    weights = [1, 0.1, 0.5, 1, 10]
return np.array(sum(map(lambda x,y: x*y, evals, weights)))

# BATTLEGROUND WIN x3
if two_players_left(state): # if it is two player
    evals = np.array([f(state) for f in [desperation, speed_demon, can_exit, exits]])
    weights = [1, 0.1, 2, 5]
else:
    evals = np.array([f(state) for f in [desperation, speed_demon, favourable_hexes, exits, no_pieces]])
    weights = [1, 0.1, 0.1, 0.5, 1]

return np.array(sum(map(lambda x,y: x*y, evals, weights)))