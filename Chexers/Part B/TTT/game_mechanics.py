""" game_mechanics.py

Contains core game functionality: defines a State and Action, and any
game-specific functions and variables.

"""

########################### IMPORTS ##########################
# Standard modules
from math import inf
from os import system
from time import sleep
from copy import deepcopy
# User-defined files

# Global Variables
INITIAL_BOARD = [
    [0, 0 ,0],
    [0, 0, 0],
    [0, 0, 0]
]

PLAYER_X = 'X'
PLAYER_O = 'O'
NEXT_PLAYER = {
    PLAYER_X: PLAYER_O,
    PLAYER_O: PLAYER_X
}

class Action:
    """ Action objects contain all information needed to update a State"""

    def __init__(self, i, j, player):
        """Assign any data relevant. By default, just a tuple"""
        self.i, self.j, self.player = i, j, player

    def __str__(self):
        """String representation of an Action"""
        return f"Position {self.i}x{self.j} by player {self.player}"

    def __eq__(self, other):
        """Defines equality of two Actions"""
        if not type(self) == type(other):
            return False
        for attribute in vars(self):
            if getattr(self, attribute) != getattr(other, attribute):
                return False
        return True

class State:
    """Stores all information that defines any game state as an object.
    Defines key methods to manipulate any state with actions"""

    def __init__(self, board=None, player='X'):
        """Initialisation: assign information features"""
        if not board:
            self.board = deepcopy(INITIAL_BOARD)
        else:
            self.board = deepcopy(board)
        self.player = 'X' # Turn player

    def __str__(self):
        """String representation"""
        return f"Turn player: {self.player}\n{self.board}"

    def possible_actions(self):
        """Returns list of possible actions for a given state"""
        result = list()
        for i, row in enumerate(self.board):
            for j, tile in enumerate(row):
                if not tile: # Tile is non-0, i.e. occupied by a piece
                    action = Action(i, j, NEXT_PLAYER[self.player()])
                    result.append(action)

        return result

    def valid_action(self, action):
        """Checks validity of an action to be applied to a State, returns boolean"""
        return (action in self.possible_actions() and
                self.player == action.player)

    def apply_action(self, action):
        """Applies an action to a State object, returns void"""
        if not self.valid_action(action):
            return
        self.board[action.i][action.j] = action.player
        if self.player == PLAYER_X:
            self.player = PLAYER_O
        else:
            self.player == PLAYER_X
        return True

    def player(self):
        """Retrieves current player"""
        return self.player

    def game_status(self):
        """Determines if a win/loss/draw has occurred and by whom"""
        win_state = [
            [self.state[0][0], self.state[0][1], self.state[0][2]], # Row 1
            [self.state[1][0], self.state[1][1], self.state[1][2]], # Row 2
            [self.state[2][0], self.state[2][1], self.state[2][2]], # Row 3
            [self.state[0][0], self.state[1][0], self.state[2][0]], # Col 1
            [self.state[0][1], self.state[1][1], self.state[2][1]], # Col 2
            [self.state[0][2], self.state[1][2], self.state[2][2]], # Col 3
            [self.state[0][0], self.state[1][1], self.state[2][2]], # Diag 1
            [self.state[2][0], self.state[1][1], self.state[0][2]], # Diag 2
        ]
        for player in NEXT_PLAYER:
            if [player]*3 in win_state:
                return player
        else:
            return None

    def game_over(self):
        """Determines if a game is over"""
        return self.game_status() in NEXT_PLAYER

########### THROW ANYTHING ELSE GAME-RELATED BELOW ###########
