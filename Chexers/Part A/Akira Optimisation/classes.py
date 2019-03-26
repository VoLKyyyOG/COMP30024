""" classes.py

All common, multi-purpose classes go here.

"""

########################## IMPORTS ###########################
# Standard modules
from collections import defaultdict

########################## GLOBALS ###########################
NUM_EXIT_STATES = 4
NUM_HEXES = 37
HASH_LEN = 82 # Bit length of any hash
CODE_LEN = 2 # Bit length of each flag. Can be 0,1,2,3
NUM_PLAYERS = 3

# Bidirectional lookup for player bit code
# Starts from 0 so that calculating heuristic values is a little smoother
PLAYER_CODE = {
    "red": 0b00,
    "green" : 0b01,
    "blue" : 0b10,
    "none" : 0b11
}
# For bidirectionality
PLAYER_CODE.update(dict(zip(PLAYER_CODE.values(), PLAYER_CODE.keys())))

# Exit code hashing scheme lookup
EXIT_CODE = list(range(3))

""" # Copy from classes. DELETE IF MERGED"""
VALID_COORDINATES = [[-3, 0], [-3, 1], [-3, 2], [-3, 3],
                    [-2, -1], [-2, 0], [-2, 1], [-2, 2], [-2, 3],
                    [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], [-1, 3],
                    [0, -3], [0, -2], [0, -1], [0, 0], [0, 1], [0, 2], [0, 3],
                    [1, -3], [1, -2], [1, -1], [1, 0], [1, 1], [1, 2],
                    [2, -3], [2, -2], [2, -1], [2, 0], [2, 1],
                    [3, -3], [3, -2], [3, -1], [3, 0]]

#################### CLASSES & FUNCTIONS #####################

class Vector:
    """Facilitates operations on axial/cubic hexagonal coordinates"""

    @staticmethod
    def add(list_1, list_2):
        """Allows for "vector_1 + vector_2"""
        return [list_1[0] + list_2[0], list_1[1] + list_2[1]]

    @staticmethod
    def sub(list_1, list_2):
        """Allows for "vector_1 - vector_2"""
        return [list_1[0] - list_2[0], list_1[1] - list_2[1]]

    @staticmethod
    def mult(list_1, n):
        """Scalar multiplication of a (direction) vector"""
        return [i*n for i in list_1]

    @staticmethod
    def get_cubic(list_1):
        """Converts axial coordinates to cubic form - assumes sum(cubic) = 0.
        Partly adapted from https://www.redblobgames.com/grids/hexagons/#neighbors-axial"""
        return [list_1[0], list_1[1], -list_1[0]-list_1[1]]
