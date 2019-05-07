"""
:filename: moves.py
:summary: Module which contain all move related functions
:authors: Akira Wang (913391), Callum Holmes (899251)
"""

########################### GLOBALS ##########################
POSSIBLE_DIRECTIONS = [(-1,+0),(+0,-1),(+1,-1),(+1,+0),(+0,+1),(-1,+1)]

VALID_COORDINATES = [
    (-3, 0), (-3, 1), (-3, 2), (-3, 3),
    (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-2, 3),
    (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3),
    (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3),
    (1, -3), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
    (2, -3), (2, -2), (2, -1), (2, 0), (2, 1),
    (3, -3), (3, -2), (3, -1), (3, 0)
]

VALID_SET = set(VALID_COORDINATES)

CORNER_HEXES = [
    (-3, 0), (-3, 3), (0, 3), (3, 0), (3, -3), (0, -3)
]

CORNER_SET = set(CORNER_HEXES)

GOALS = {
    'red': [(3,-3), (3,-2), (3,-1), (3,0)],
    'green': [(-3,3), (-2,3), (-1,3), (0,3)],
    'blue': [(-3,0),(-2,-1),(-1,-2),(0,-3)],
}

########################## FUNCTIONS #########################

def add(u, v):
    """
    Function that adds two vectors u, v (tuple representation)
    :returns: tuple vector
    """
    return (u[0] + v[0], u[1] + v[1])

def sub(u, v):
    """
    Function that subtracts two vectors u, v (tuple representation)
    :returns: tuple vector
    """
    return (u[0] - v[0], u[1] - v[1])

def get_cubic_ordered(v):
    """
    Function that converts axial to cubic, but in order of (x, z, y) in order to allow for colour hashing.
    :returns: cubic coordinates in player ordering
    """
    return (v[0], v[1], -v[0]-v[1])

def get_cubic(v):
    """
    Function that converts axial coordinates to conventional cubic coordinates
    :returns: cubic coordinates
    """
    return (v[0], -v[0]-v[1], v[1])

def get_axial(v):
    """
    Function that converts cubic coordinates to axial coordinates
    :returns: axial coordinates
    """
    return (v[0], v[2])

def get_axial_ordered(v):
    """
    Function that converts player-ordered cubic coordinates to axial coordinates
    :returns: axial coordinates
    """
    return (v[0], v[1])

def midpoint(u, v):
    """
    Function that finds midpoint of two vectors u, v (tuple representation)
    :returns: tuple vector
    """
    return (int((u[0] + v[0]) / 2), int((u[1] + v[1]) / 2))

def exit_action(state, colour):
    """
    Function to see if an exit is possible.
    Assumes that if a piece is at a goal hex, it is not blocked (since you are at a goal hex).
    :returns: Coordinates of pieces that can exit
    """
    return [("EXIT", piece) for piece in state[colour] if piece in GOALS[colour]]

def move_action(state, occupied_hexes, colour):
    """
    Function to see if a move action is possible.
    :returns: list of possible move directions.
    """
    possible_moves = list()

    for piece in state[colour]:
        for direction in POSSIBLE_DIRECTIONS:
            adjacent_hex = add(piece, direction)
            if adjacent_hex in VALID_COORDINATES and adjacent_hex not in occupied_hexes:
                possible_moves.append(("MOVE", (piece, adjacent_hex)))

    return possible_moves

def jump_action(state, occupied_hexes, colour):
    """
    Function to see if a jump action is possible.
    :returns: list of possible jump directions.
    """
    possible_jumps = list()

    for piece in state[colour]:
        for direction in POSSIBLE_DIRECTIONS:
            adjacent_hex = add(piece, direction)
            target_hex = add(adjacent_hex, direction)
            if adjacent_hex in occupied_hexes:
                if target_hex in VALID_COORDINATES and target_hex not in occupied_hexes:
                    possible_jumps.append(("JUMP", (piece, target_hex)))

    return possible_jumps
