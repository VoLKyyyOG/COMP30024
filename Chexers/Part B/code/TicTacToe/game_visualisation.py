""" game_visualisation.py

Includes all methods necessary to visualise a game.

"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files

SEPARATOR = '\n---------------'

def display_state(state, message = ""):
    """Prints the current board state""""
    print(f"NOTE: {message} {SEPARATOR}")
    for row in state.board:
        for tile in row:
            print(f"| {tile} |", end="")
        print(SEPARATOR)
    raise NotImplementedError
