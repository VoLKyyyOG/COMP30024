import sys
sys.path.append("..")
#from mechanics import
from moves import *
from algorithms.heuristics import speed_demon, desperation, favourable_hexes, exits, achilles_real, end_game_heuristic, end_game_proportion
from algorithms.PARTA.formatting import print_board

test1 = {
    "turn" : "red", "depth": 142,
    "exits": {"red":0, "green": 1, "blue": 0},
    "red": [(-1,-1),(0,-2),(0,-1),(1,-2)],
    "green": [(-2,2),(1,-1),(1,1)],
    "blue": [(2,-1),(0,0),(1,0),(2,0)],
}

test2 = {
    "turn" : "red", "depth": 142,
    "exits": {"red": 0, "green": 1, "blue": 0},
    "red": [(-1,-1),(0,-2),(0,-1),(1,-2)],
    "green": [(0,3)],
    "blue": [(2,-1),(0,0),(1,0),(2,0)],
}

test3 = {
    "turn": 'red', 'depth':142,
    "exits": {'red':0, 'green':0, 'blue':0},
    "red": [(3,-3), (3,-2), (3,-1), (2,-3), (0,3), (-1,3), (-3,3)],
    "green": [(-3,1),(1,2),(-2,3)],
    "blue": [(2,-2)]
}

def printer(state):
    board_dict = {}
    for player in PLAYER_NAMES:
        for i in state[player]:
            board_dict[i] = f"{player}"

    print_board(board_dict)



"""
printer(test2)
x = defaultdict()
x[Z_hash(test1)] = test1
print(x)
print(Z_hash(test1) in x)
"""

for f, weight in zip([desperation, speed_demon, favourable_hexes, exits, achilles_real], [1, 0.2, 0.1 , 2.5, 0.25]):
    print(f"{f.__name__} : {f(test3)}")
print(end_game_proportion(test3))
