""" classes.py

All common, multi-purpose classes go here.

Document structure:

- Contents - all imports. NOT globals.

For each new addition:
- Introduction
- New Globals
- Code

"""

########################## IMPORTS ############################
from collections import defaultdict

########################## VECTORS ############################

""" Example
v1 = [1,2]
v2 = [-1,0]
Vector.add(v1, v2) # Outputs [0, 2]
Vector.sub(v1, v2) # Outputs [2, 2]
Vector.mult(v1, 2) # Outputs [2, 4]
Vector.get_cubic(v1) # Outputs [1,2,-3]
"""

class Vector:
    """Facilitates construction and smooth use of coordinates for pythonic code!"""

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
        """Converts axial coordinates to cubic coordinates"""
        return [list_1[0], list_1[1], -list_1[0]-list_1[1]]

########################## HASHING ############################

"""
Implements a MINIMUM-COST, 0% COLLISION (for our project anyway), INVERTIBLE hashing mechanism to store board states

IMPLEMENTATION: The general idea is, Each of the 37 hexes has a 2-bit flag,
 + one flag for turn player
 + 3 flags for exit_totals
 = an 82-bit long int

Example use (using my_data = {'colour': 'red', 'pieces': [[0, 0]], 'blocks': [[3, -1]]}):
- hashed_board_state = Z_hash(my_data)
# Effectively equivalent to my_data, PLUS coordinates in 'pieces', 'blocks' sorted!
- extract_data = Z_data(hashed_board_state)

This is ideally used for trees, and could allow for similarity checks.
Should be indifferent however to using hash() for hash tables HOWEVER
Unsure if hash() could yield collisions, what with the huge volume of generation that will occur
Regardless, Z_hash is invertible = win

"""

######################### NEW GLOBALS #########################
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
PLAYER_CODE.update(dict(zip(PLAYER_CODE.values(), PLAYER_CODE.keys())))

# Exit code hashing scheme lookup
EXIT_CODE = list(range(3))
VALID_COORDINATES = [[-3, 0], [-3, 1], [-3, 2], [-3, 3],
                    [-2, -1], [-2, 0], [-2, 1], [-2, 2], [-2, 3],
                    [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], [-1, 3],
                    [0, -3], [0, -2], [0, -1], [0, 0], [0, 1], [0, 2], [0, 3],
                    [1, -3], [1, -2], [1, -1], [1, 0], [1, 1], [1, 2],
                    [2, -3], [2, -2], [2, -1], [2, 0], [2, 1],
                    [3, -3], [3, -2], [3, -1], [3, 0]]
                    
def Z_hash(data):
    """Hash the board state"""
    hashed = 0b0

    """TEMPORARY (PART A) HASH SCHEME
    0b(turn)(red_exits)(green_exits)(blue_exits)(37 hex state flags....):
    - For turn player:
        - 11 for none # This is just here for Part B
        - 00 for red
        - 01 for green
        - 10 for blue
    - For flags of exit_totals:
        - 00 for 0, 01 for 1 ... etc
    - For the 37 hexes:
        - 00 for empty
        - 01 for player
        - 10 for block # Could have been 11, just needed to not be 00 or 01
     THIS WILL NEED UPDATING POST PROJECT A TO HANDLE ALL 3 COLOURS"""

    # Append turn player
    hashed = hashed | PLAYER_CODE[data["colour"]]

    # Currently 0b(turn)
    # TEMPORARY: NOT implementing num_exits flag yet. Still need to shift by 6.
    """
    for color in exit_count_data (this would need appending to data):
        hashed = (hashed << 2) | EXIT_CODE[color]
    """
    hashed = hashed << NUM_PLAYERS * CODE_LEN # just a fix to make room for num_exits

    # Encode coordinates: First, make space
    hashed = hashed << NUM_HEXES * CODE_LEN

    # ith pair of 2-bits = ith location in VALID_COORDINATES
    # AGAIN, A TEMPORARY HASHING SCHEME FOR PART A
    for coordinate in data["blocks"]:
        hashed = hashed ^ (0b10 << CODE_LEN * VALID_COORDINATES.index(coordinate))
    for coordinate in data["pieces"]:
        hashed = hashed ^ (0b01 << CODE_LEN * VALID_COORDINATES.index(coordinate))

def Z_data(hashed):
    """Return data for board"""
    result = defaultdict(list)
    result["colour"] = PLAYER_CODE[hashed >> HASH_LEN - CODE_LEN] # First entry

    # N.B.: Will need Another few lines to read exit information, not necessary right now
    """
    ( read exit states into result)
    """

    for i, coordinate in enumerate(VALID_COORDINATES):
        # ith coordinate = 2ith 2-bit combination in hash
        hex_code = (hashed >> CODE_LEN*i) & 0b11  # Extracts JUST the code for ith coordinate

        """WARNING: Will need changing to handle all colours in Part B. For now, it's either same or different"""
        if PLAYER_CODE[hex_code] == result["colour"]:
            result["pieces"].append(coordinate)
        elif PLAYER_CODE[hex_code] != "none": # Again, this will change when Part B comes along
            result["blocks"].append(coordinate)

    return dict(result)

"""Debugging
if __name__ == "__main__":
    my_data = {'colour': 'red', 'pieces': [[0, 0], [0, 1], [-2, 1]], 'blocks': [[-1, 0], [-1, 1], [1, 1], [3, -1]]}
    test_color = {'colour': 'red', 'pieces': [], 'blocks': []}
    my_hash = Z_hash(my_data)
    print(bin(my_hash.hashed))
    for i in range(41):
        if ((my_hash.hashed >> 2*i) & 0b11) > 0:
            print(i+1, my_hash.hashed >> 2*i & 0b11)
    print("*"*40)
    print(my_hash.data())
"""

########################## END OF FILE ###############################
########################## END OF FILE ###############################
########################## END OF FILE ###############################
