""" hash.py
Implements a MINIMUM-COST, 0% COLLISION (for our project anyway), INVERTIBLE hashing mechanism to store board states

Example use (using my_data = {'colour': 'red', 'pieces': [[0, 0]], 'blocks': [[3, -1]]}):

# Encodes into an 82-bit (long) integer
- hashed_board_state = Z_hash(my_data)
# Effectively equivalent to my_data, PLUS coordinates in 'pieces', 'blocks' sorted!
- extract_data = hashed_board_state.data()

This is ideally used for trees, and could allow for similarity checks.
Should be indifferent however to using hash() for hash tables HOWEVER
Unsure if hash() could yield collisions, what with the huge volume of generation that will occur
Regardless, Z_hash is invertible = win

"""

from collections import defaultdict
from classes import *
from moves import *

"""IDEA: Each of the 37 hexes has a 2-bit flag, + one flag for turn player + 3 flags for exit_totals = an 88-bit long int
00 > empty, 01 > R, 10 > G, 11 > B"""

######################### GLOBALS #########################
NUM_EXIT_STATES = 4
NUM_HEXES = 37
HASH_LEN = 82
CODE_LEN = 2
NUM_PLAYERS = 3

# Bidirectional lookup for player bit code
PLAYER_CODE = {
    "none": 0b00,
    "red" : 0b01,
    "green" : 0b10,
    "blue" : 0b11
}
PLAYER_CODE.update(dict(zip(PLAYER_CODE.values(), PLAYER_CODE.keys())))

# If we're desperate for memory optimisation, use this to lookup coordinates and get the index for the hash
# But enumerate is really efficient so the implementation in Z_hash.data() should be FINE
# get_index = {x:i for i,x in enumerate(VALID_COORDINATES)}

# Exit code hashing scheme lookup
EXIT_CODE = list(range(3))

class Z_hash:
    def __init__(self, data):
        """Hash the board state"""
        self.hashed = 0b0

        """TEMPORARY (PART A) HASH SCHEME
        0b(turn)(red_exits)(green_exits)(blue_exits)(37 hex state flags....):
        - For turn player:
            - 00 for none # This is just here for Part B
            - 01 for red
            - 10 for green
            - 11 for blue
        - For flags of exit_totals:
            - 00 for 0, 01 for 1 ... etc
        - For the 37 hexes:
            - 00 for empty
            - 01 for player
            - 10 for block # Could have been 11, just needed to not be 00 or 01
         THIS WILL NEED UPDATING POST PROJECT A TO HANDLE ALL 3 COLOURS"""

        # Append turn player
        self.hashed = self.hashed | PLAYER_CODE[data["colour"]]

        # Currently 0b(turn)
        # TEMPORARY: NOT implementing num_exits flag yet. Still need to shift by 6.
        """
        for color in exit_count_data (this would need appending to data):
            self.hashed = (self.hashed << 2) | EXIT_CODE[color]
        """
        self.hashed = self.hashed << NUM_PLAYERS * CODE_LEN # just a fix to make room for num_exits

        # Encode coordinates: First, make space
        self.hashed = self.hashed << NUM_HEXES * CODE_LEN

        # ith pair of 2-bits = ith location in VALID_COORDINATES
        # AGAIN, A TEMPORARY HASHING SCHEME FOR PART A
        for coordinate in data["blocks"]:
            self.hashed = self.hashed ^ (0b10 << CODE_LEN * VALID_COORDINATES.index(coordinate))
        for coordinate in data["pieces"]:
            self.hashed = self.hashed ^ (0b01 << CODE_LEN * VALID_COORDINATES.index(coordinate))

    def data(self):
        """Return data for board"""
        result = defaultdict(list)
        result["colour"] = PLAYER_CODE[self.hashed >> HASH_LEN - CODE_LEN]

        # N.B.: Will need Another few lines to read exit information, not necessary right now
        """
        ( read exit states into result)
        """

        for i, coordinate in enumerate(VALID_COORDINATES):
            # ith coordinate = 2ith 2-bit combination in hash
            hex_code = (self.hashed >> CODE_LEN*i) & 0b11  # Extracts JUST the code for ith coordinate

            """WARNING: Will need changing to handle all colours in Part B. For now, it's either same or different"""
            if PLAYER_CODE[hex_code] == result["colour"]:
                result["pieces"].append(coordinate)
            elif PLAYER_CODE[hex_code] != "none": # Again, this will change when Part B comes along
                result["blocks"].append(coordinate)

        return dict(result)

"""Debugging"""
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
