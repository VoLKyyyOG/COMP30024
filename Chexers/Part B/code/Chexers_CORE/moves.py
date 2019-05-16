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

VALID_SET = {
    (-3, 0), (-3, 1), (-3, 2), (-3, 3),
    (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-2, 3),
    (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3),
    (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3),
    (1, -3), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
    (2, -3), (2, -2), (2, -1), (2, 0), (2, 1),
    (3, -3), (3, -2), (3, -1), (3, 0)
}

CORNER_SET = {
    (-3, 0), (-3, 3), (0, 3), (3, 0), (3, -3), (0, -3)
}

OPPONENTS = {
    'red': ['green', 'blue'],
    'green': ['blue', 'red'],
    'blue': ['red', 'green']
}

GOALS = {
    'red': [(3,-3), (3,-2), (3,-1), (3,0)],
    'green': [(-3,3), (-2,3), (-1,3), (0,3)],
    'blue': [(-3,0), (-2,-1), (-1,-2), (0,-3)],
}

OPPONENT_GOALS = {
    'red': {
        (-3,3), (-2,3), (-1,3), (0,3),
        (-3,0), (-2,-1), (-1,-2), (0,-3)
    },
    'green': {
        (3,-3), (3,-2), (3,-1), (3,0),
        (-3,0), (-2,-1), (-1,-2), (0,-3)
    },
    'blue': {
        (3,-3), (3,-2), (3,-1), (3,0),
        (-3,3), (-2,3), (-1,3), (0,3)
    }
}

###################### VECTOR FUNCTIONS ######################

def add(u, v):
    """
    :summary: adds two vectors u, v (tuple representation)
    :returns: tuple vector
    """
    return (u[0] + v[0], u[1] + v[1])

def sub(u, v):
    """
    :summary: subtracts two vectors u, v (tuple representation)
    :returns: tuple vector
    """
    return (u[0] - v[0], u[1] - v[1])

def get_cubic_ordered(v):
    """
    :summary: converts axial to cubic, but in order of (x, z, y) in order to allow for colour hashing.
    :returns: cubic coordinates in player ordering
    """
    return (v[0], v[1], -v[0]-v[1])

def get_axial_ordered(v):
    """
    :summary: converts player-ordered cubic coordinates to axial coordinates
    :returns: axial coordinates
    """
    return (v[0], v[1])

def midpoint(u, v):
    """
    :summary: finds midpoint of two vectors u, v (tuple representation)
    :returns: tuple vector
    """
    return (int((u[0] + v[0]) / 2), int((u[1] + v[1]) / 2))

###################### ACTION FUNCTIONS ######################

def exit_action(state, colour):
    """
    :summary: Function to see if an exit is possible.
    :assumption: if a piece is at a goal hex, it is not blocked (since you are at a goal hex).
    :returns: Coordinates of pieces that can exit
    """
    return [("EXIT", piece) for piece in state[colour] if piece in GOALS[colour]]

def move_action(state, occupied_hexes, colour):
    """
    :summary: Function to see if a move action is possible.
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
    :summary: Function to see if a jump action is possible.
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

######################## MOVE ORDERING #######################

def capture(state, old, new, colour):
    """
    :summary: Checks if the jump is a capturing jump.
    :returns: boolean
    """
    return midpoint(old, new) not in state[colour]

def capture_jumps(state, occupied_hexes, colour):
    """
    :summary: Fetches all jump actions that could capture pieces
    :returns: list of actions
    """
    captures = list()

    for piece in state[colour]:
        for direction in POSSIBLE_DIRECTIONS:
            adjacent_hex = add(piece, direction)
            target_hex = add(adjacent_hex, direction)
            if adjacent_hex in occupied_hexes:
                if target_hex in VALID_COORDINATES and target_hex not in occupied_hexes and capture(state, piece, target_hex, colour):
                    captures.append(("JUMP", (piece, target_hex)))

    return captures

def jump_sort(state, possible_jumps, colour):
    """
    :summary: Orders all possible jumps from capturing jumps to self jumps.
    Useful for alpha-beta pruning.
    :returns: list of jump actions
    """
    capture_jumps = list()
    self_jumps = list()

    for jump in possible_jumps:
        if capture(state, jump[1][0], jump[1][1], colour):
            capture_jumps.append(jump)
        else:
            self_jumps.append(jump)

    return capture_jumps + self_jumps
