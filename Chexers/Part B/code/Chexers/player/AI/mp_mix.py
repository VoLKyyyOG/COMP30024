""" mp_mix.py

Implements an amazing 3-player algorithm

"""

########################### IMPORTS ##########################
# Standard modules
from copy import deepcopy
from math import inf
# User-defined files
from mechanics import *

def mp_mix(state, heuristic, defenceThreshold, offenceThreshold, maximisingPlayer):
    """
    Works under the assumption that there are 3 players - can be made to catch exceptions.
    """
    opponents = [i for i in PLAYER_NAMES if i != maximisingPlayer]
    H = list()
    for maximisingPlayer in opponents:
        H.append(heuristic(state, maximisingPlayer, maximisingPlayer))
    H.sort(reversed=True)
    

    return AlgorithmRequiredError

"""
for i in Players:
    H[i] = evaluate(i)
end
sort(H) in decreasing order (max -> min)
leadingEdge = H[0] - H[1] # the two leaders of three players
leader = Player with max(H)

if leader is maximisingPlayer:
    if leadingEdge >= defenceThreshold:
        PARANOID
    end
else:
    if leadingEdge >= offenceThreshold:
        OFFENSIVE
    end
end

MAXN
"""
    