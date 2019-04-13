""" game_mechanics.py

Contains core game functionality: defines a State and Action, and any
game-specific functions and variables.

"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files

class Action:
    """ Action objects contain all information needed to update a State"""

    def __init__(self, *args):
        """Assign any data relevant. By default, just a tuple"""
        self.data = args

    def __str__(self):
        """String representation of an Action"""
        return str(self.data)

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

    def __init__(self, *args):
        """Initialisation: assign information features"""
        raise NotImplementedError

    def __str__(self):
        """String representation"""
        raise NotImplementedError

    def possible_actions(self):
        """Returns list of possible actions for a given state"""
        raise NotImplementedError

    def valid_action(self, action):
        """Checks validity of an action to be applied to a State, returns boolean"""
        raise NotImplementedError

    def apply_action(self, action):
        """Applies an action to a State object, returns void"""
        raise NotImplementedError

    def player(self):
        """Retrieves current player"""
        raise NotImplementedError

    def game_status(self):
        """Determines if a win/loss/draw has occurred and by whom"""
        raise NotImplementedError

    def game_over(self):
        """Determines if a game is over"""
        raise NotImplementedError

    def encode(self):
        """Defines a low-collision hash for a State object"""
        raise NotImplementedError

    @staticmethod
    def decode(encoding):
        """If desired, inverts an encoding"""
        # Up to implementation whether to return raw data, or State object
        raise NotImplementedError

########### THROW ANYTHING ELSE GAME-RELATED BELOW ###########
