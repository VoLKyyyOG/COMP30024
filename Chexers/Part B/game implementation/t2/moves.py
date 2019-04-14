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

PIECE_COORD, NO_PIECE, NO_EXIT_PIECE = 0, 1, 2

COLOURS = ["red", "green", "blue"]

# Move related functions -> to be called by agent for possible actions at the current stage
"""
Return values for the referee:
1. ("MOVE", ((q1, r1), (q2, r2)))
2. ("JUMP", ((q1, r1), (q2, r2)))
3. ("EXIT", (q1, q2))
4. ("PASS", None)
"""

def add(u, v):
    """
    Function that adds two vectors u, v.
    :returns: vector p = u + v
    """
    return (u[0] + v[0], u[1] + v[1])

def find_possible_actions(player):
    """
    Function that finds all possible actions in a given state.
    :returns: list of possible actions.
    """
    possible_actions = list()

    current_state = player.state[player.colour][PIECE_COORD]

    # All occupied hexes (doesn't account for who's who)
    # That is taken care of if a capture has occurred in update()
    # temp is a generator function that returns all piece coordinates per player
    temp = list(i[0] for i in player.state.values())
    occupied = temp[0].union(temp[1].union(temp[2])) # pythonic methods they said
    del temp

    # Exits
    possible_actions.extend(exit_action(current_state, player.goal))

    # Moves
    possible_actions.extend(move_action(current_state, occupied))

    # Jumps
    possible_actions.extend(jump_action(current_state, occupied))

    return possible_actions

def exit_action(state, goal):
    """
    Function to see if an exit is possible.
    Assumes that if a piece is at a goal hex, it is not blocked (since you are at a goal hex).
    :returns: Coordinates of pieces that can exit
    """
    return [("EXIT", i) for i in state if i in goal]

def move_action(state, occupied):
    """
    Function to see if a move action is possible.
    :returns: list of possible move directions.
    """
    possible_moves = list()

    for piece in state:
        for direction in POSSIBLE_DIRECTIONS:
            adjacent_hex = add(piece, direction)
            if adjacent_hex in VALID_COORDINATES and adjacent_hex not in occupied:
                    possible_moves.append(("MOVE", (piece, adjacent_hex)))

    return sorted(possible_moves)  

def jump_action(state, occupied):
    """
    Function to see if a jump action is possible.
    :returns: list of possible jump directions.
    :TODO: ACCOUNT FOR CAPTURING PIECES
    """
    possible_jumps = list()

    for piece in state:
        for direction in POSSIBLE_DIRECTIONS:
            adjacent_hex = add(piece, direction)
            target_hex = add(adjacent_hex, direction)
            if adjacent_hex in occupied:
                if target_hex in VALID_COORDINATES and target_hex not in occupied:
                    possible_jumps.append(("JUMP", (piece, target_hex)))

    return sorted(possible_jumps)

def find_jumped_piece(player, coordinates):
    initial, destination = coordinates[0], coordinates[1]
    """
    Attempts linear combinations to find the adjacent hex.
    :returns: a tuple with the colour of the piece jumped and the coordinate of the jumped hex.
    """
    for direction in POSSIBLE_DIRECTIONS:
        adjacent_hex = add(initial, direction)
        if add(adjacent_hex, direction) == destination: # Found linear combination and the adjacent hex
            for colour in COLOURS: # Now for each player
                current = player.state[colour] # Get the state of player # 
                if adjacent_hex in current[PIECE_COORD]: # if adjacent hex is player piece
                    return colour, adjacent_hex