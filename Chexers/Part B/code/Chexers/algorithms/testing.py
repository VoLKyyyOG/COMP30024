import sys
sys.path.append("..")
from mechanics import *
from moves import *
from algorithms.heuristics import *
from algorithms.partA.formatting import print_board

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

def printer(state):
    board_dict = {}
    for player in PLAYER_NAMES:
        for i in state[player]:
            board_dict[i] = f"{player}"

    print_board(board_dict)

printer(test2)
print(end_game_heuristic(test2))
