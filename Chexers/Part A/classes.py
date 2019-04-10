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
VALID_COORDINATES = [(-3, 0), (-3, 1), (-3, 2), (-3, 3),
                    (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-2, 3),
                    (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3),
                    (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3),
                    (1, -3), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
                    (2, -3), (2, -2), (2, -1), (2, 0), (2, 1),
                    (3, -3), (3, -2), (3, -1), (3, 0)]

#################### CLASSES & FUNCTIONS #####################

######################### DECORATORS #########################

"""ADAPTED FROM https://www.python-course.eu/python3_memoization.php"""
def memoize(method):
    """Caches result of a function to prevent recalculation under same input"""
    memo = []
    def helper(*args, **kwargs):
        if not len(memo):
            memo.append(method(*args, *kwargs))
        return memo[0]
    return helper

########################## VECTORS ##########################

class Vector:
    """Facilitates operations on axial/cubic hexagonal coordinates"""

    @staticmethod
    def solve(v_1, v_2, v_target):
        """For the matrix equation Ay = target, calculates y
            Assumed A is 2x2 with columns v_1 and v_2"""
        u, v, x = v_1, v_2, v_target
        det_uv = float(u[0]*v[1]-u[1]*v[0])
        assert(abs(det_uv) > 0.0001)
        return (int((v[1]*x[0] - v[0]*x[1]) / det_uv), int((-u[1]*x[0] + u[0]*x[1]) / det_uv))

    @staticmethod
    def add(list_1, list_2):
        """Allows for "vector_1 + vector_2"""
        return (list_1[0] + list_2[0], list_1[1] + list_2[1])

    @staticmethod
    def sub(list_1, list_2):
        """Allows for "vector_1 - vector_2"""
        return (list_1[0] - list_2[0], list_1[1] - list_2[1])


    @staticmethod
    def mult(list_1, n):
        """Scalar multiplication of a (direction) vector"""
        return tuple([i*n for i in list_1])
        
########################## HASHING ############################

"""
Implements a MINIMUM-COST, 0% COLLISION, INVERTIBLE hash for board states

Each of the 37 hexes has a 2-bit flag:
 + one flag for turn player
 + 3 flags for exit_totals
 = an 82-bit long int

"""

def Z_hash(data):
    """Hash the board state"""
    hashed = 0

    """TEMPORARY (PART A) HASH SCHEME
    0b(turn)(red_exits)(green_exits)(blue_exits)(37 hex state flags....):
    - For turn player:
        - 11 for none - This is just here for Part B
        - 00 for red
        - 01 for green
        - 10 for blue
    - For flags of exit_totals:
        - 00 for 0, 01 for 1 ... etc . Part B usage only
    - For the 37 hexes:
        - 00 for empty
        - 01 for player
        - 10 for block # Could have been 11, just needed to not be 00 or 01
     THIS WILL NEED UPDATING POST PROJECT A TO HANDLE ALL 3 COLOURS"""

    # Append turn player
    hashed = hashed | PLAYER_CODE[data["colour"]]
    """
    for color in exit_count_data (this would need appending to data):
        hashed = (hashed << 2) | EXIT_CODE[color]
    """
    # just a fix to make room for num_exits
    hashed = hashed << NUM_PLAYERS * CODE_LEN

    # Encode coordinates: First, make space
    hashed = hashed << NUM_HEXES * CODE_LEN

    # ith pair of 2-bits = ith location in VALID_COORDINATES
    # AGAIN, A TEMPORARY HASHING SCHEME FOR PART A
    for piece in data["blocks"]:
        hashed = hashed ^ (0b10 << CODE_LEN * VALID_COORDINATES.index(piece))
    for piece in data["pieces"]:
        hashed = hashed ^ (0b01 << CODE_LEN * VALID_COORDINATES.index(piece))
    return hashed


def Z_data(hashed):
    """Return data for board"""
    result = defaultdict(list)
    result["colour"] = PLAYER_CODE[hashed >> HASH_LEN - CODE_LEN] # First entry
    """
    PART B: ( read exit states into result)
    """

    hex_codes = [(hashed >> CODE_LEN*i) & 0b11 for i in range(NUM_HEXES)]
    for i, coordinate in enumerate(VALID_COORDINATES):
        # ith coordinate = 2ith 2-bit combination in hash
        hex_code = (hashed >> CODE_LEN*i) & 0b11

        """PART B: Will need changing to handle all colours"""
        if hex_code == 0b01:
            result["pieces"].append(coordinate)
        elif hex_code == 0b10:
            result["blocks"].append(coordinate)

    return dict(result)
