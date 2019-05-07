########################### IMPORTS ##########################

# Standard modules
from mechanics import possible_actions

# Global Imports
from mechanics import N_PLAYERS 


OPENING_BOOK = {
    'red': [
        ('MOVE', ((-3, 3), (-2, 2))), 
        ('JUMP', ((-3, 2), (-1, 2))), 
        ('JUMP', ((-3, 0), (-3, 2)))
    ], 
    'green': [
        ('MOVE', ((0, -3), (0, -2))), 
        ('JUMP', ((1, -3), (-1, -1))), 
        ('JUMP', ((3, -3), (1, -3)))
    ], 
    'blue': [
        ('MOVE', ((3, 0), (2, 0))), 
        ('JUMP', ((2, 1), (2, -1))), 
        ('JUMP', ((0, 3), (2, 1)))
    ]
}

######################## MOVE FUNCTIONS #######################

def opening_moves(state, colour):
    """
    Returns the first three opening moves if possible
    """
    action = OPENING_BOOK[colour].pop(0)
    if action in possible_actions(state, colour):
        return action
    return False