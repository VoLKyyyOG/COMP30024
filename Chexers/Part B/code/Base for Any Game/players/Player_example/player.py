""" player.py

Base class for any Player.
Outlines attributes and methods that all Agent implementations should have.

"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files
from mechanics import *

class ExamplePlayer:
    # if renamed here, must rename in __init__.py too
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.
        """
        # Colour will be 'red', 'green' etc. so ensure it matches algorithms
        raise NotImplementedError

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action."""
        raise NotImplementedError
        # TODO: Update state representation in response to action.

    ################# DEFINE EVERY IMPLEMENTATION ################

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        """
        raise NotImplementedError
