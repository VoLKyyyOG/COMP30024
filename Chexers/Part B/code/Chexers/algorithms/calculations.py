
"""

Branching calculations:
- Formula for depth 3k: product((6*n_i else epsilon)^k)
- Worst case is (2*avg)^(3k)
- Best case is


"""

import numpy as np
import math

def player_max_actions(n):
    return 6*n

def b_factor(n_matrix, k=1):
    """Branching factor over 3k turns (k cycles)"""
    result = 1
    for n in n_matrix:
        result *= player_max_actions(n) if (n > 0) else 1
    return result**k

def d_factor(n_matrix, th=15000):
    """Gets depth allowed that reaches threshold"""
    return 3*math.log(th) / math.log(b_factor(n_matrix))

N = np.array([12,11,10,9,8,7,6,5,4])
worst_case = lambda N: np.array([N / 3.0]*3)
worst = [worst_case(n) for n in N]
two_player_worst_case = np.vectorize(lambda N: np.array([N / 2.0]*2 + [0]))
two_worst = [two_player_worst_case(n) for n in N]


depth_t = 1500000
for n in N:
    print(f"{n} - 3P {b_factor(worst_case(n))} --> depth {d_factor(worst_case(n), depth_t):.3f}", end='')
    print(f" 2P {b_factor(two_player_worst_case(n))} --> depth {d_factor(two_player_worst_case(n), depth_t):.3f}")
