# Global Variables
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

STARTS = {
    'red': [(-3,3), (-3,2), (-3,1), (-3,0)],
    'green': [(0,-3), (1,-3), (2,-3), (3,-3)],
    'blue': [(3, 0), (2, 1), (1, 2), (0, 3)],
}

GOALS = {
    'red': [(3,-3), (3,-2), (3,-1), (3,0)],
    'green': [(-3,3), (-2,3), (-1,3), (0,3)],
    'blue': [(-3,0),(-2,-1),(-1,-2),(0,-3)],
}

MAX_COORDINATE_VAL = 3

"""
Return values for the referee:
1. ("MOVE", ((q1, r1), (q2, r2)))
2. ("JUMP", ((q1, r1), (q2, r2)))
3. ("EXIT", (q1, q2))
4. ("PASS", None)
"""

def add(u, v):
    """Function that adds two vectors u, v (tuple representation)
    :returns: tuple vector"""
    return (u[0] + v[0], u[1] + v[1])

def sub(u, v):
    """Function that subtracts two vectors u, v (tuple representation)
    :returns: tuple vector"""
    return (u[0] - v[0], u[1] - v[1])

def get_cubic(v):
        """Converts axial coordinates to cubic coordinates"""
        return (v[0], v[1], -v[0]-v[1])

def midpoint(u, v):
    """Function that finds midpoint of two vectors u, v (tuple representation)
    :returns: tuple vector"""
    return (int((u[0] + v[0]) / 2), int((u[1] + v[1]) / 2))

def exit_action(state, colour):
    """
    Function to see if an exit is possible.
    Assumes that if a piece is at a goal hex, it is not blocked (since you are at a goal hex).
    :returns: Coordinates of pieces that can exit
    """
    return [("EXIT", piece) for piece in state[colour] if piece in GOALS[colour]]

def move_action(state, occupied, colour):
    """
    Function to see if a move action is possible.
    :returns: list of possible move directions.
    """
    possible_moves = list()

    for piece in state[colour]:
        for direction in POSSIBLE_DIRECTIONS:
            adjacent_hex = add(piece, direction)
            if adjacent_hex in VALID_COORDINATES and adjacent_hex not in occupied:
                possible_moves.append(("MOVE", (piece, adjacent_hex)))

    return sorted(possible_moves)

def jump_action(state, occupied, colour):
    """
    Function to see if a jump action is possible.
    :returns: list of possible jump directions.
    """
    possible_jumps = list()

    for piece in state[colour]:
        for direction in POSSIBLE_DIRECTIONS:
            adjacent_hex = add(piece, direction)
            target_hex = add(adjacent_hex, direction)
            if adjacent_hex in occupied:
                if target_hex in VALID_COORDINATES and target_hex not in occupied:
                    possible_jumps.append(("JUMP", (piece, target_hex)))

    return sorted(possible_jumps)
