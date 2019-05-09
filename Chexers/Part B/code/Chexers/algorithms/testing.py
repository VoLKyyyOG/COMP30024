import sys
sys.path.append("..")
from mechanics import *
from moves import *
from algorithms.heuristics import *
from structures.TT import *
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



"""
printer(test2)
x = defaultdict()
x[Z_hash(test1)] = test1
print(x)
print(Z_hash(test1) in x)
"""

from math import factorial as fact
result = 0
for N in range(12, 12+1):
    for r in range(0, N+1):
        for g in range(0, N-r+1):
            result += 1.0 * fact(37) / fact(r)*fact(g)*fact(N - r - g)

print(result)

from math import factorial as fact
result = 0
for N in range(3,12+1):
    for r in range(0, N+1):
        for g in range(0, N-r+1):
            result += 1.0 * fact(37) / fact(r)*fact(g)*fact(N - r - g)

print(result)
