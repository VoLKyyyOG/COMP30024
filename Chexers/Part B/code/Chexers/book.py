########################### IMPORTS ##########################

# Standard modules
from mechanics import possible_actions

# Global Imports
#### TODO: Consider if this will be used
from mechanics import N_PLAYERS

OPENING_BOOK = {
    'red': [
        ('MOVE', ((-3, 3), (-2, 2))),
        ('JUMP', ((-3, 2), (-1, 2))),
        ('JUMP', ((-3, 0), (-3, 2))),
        ('JUMP', ((-3, 1), (-3, 3))),
    ],
    'green': [
        ('MOVE', ((0, -3), (0, -2))),
        ('JUMP', ((1, -3), (-1, -1))),
        ('JUMP', ((3, -3), (1, -3))),
        ('JUMP', ((2, -3), (0, -3)))
    ],
    'blue': [
        ('MOVE', ((3, 0), (2, 0))),
        ('JUMP', ((2, 1), (2, -1))),
        ('JUMP', ((0, 3), (2, 1))),
        ('JUMP', ((1, 2), (3, 0)))
    ]
}

######################## MOVE FUNCTIONS #######################

def opening_moves(state, colour):
    """
    Returns the first three opening moves if possible
    :returns: action
    """
    action = OPENING_BOOK[colour].pop(0)
    return action if action in possible_actions(state, colour) else False
