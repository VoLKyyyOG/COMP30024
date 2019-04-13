""" player.py

Base class for any MinimaxPlayer.
Uses the common minimax 2-player algorithm to decide actions.

"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files
from mechanics import *
from .minimax import *

class MinimaxPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.
        """
        self.colour_code = colour[0] # This will be 'r', 'g' etc.
        self.maximisingPlayer = PLAYER_CODES[0]
        self.state = create_initial_state()

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action."""
        self.state = apply_action(self.state, action)

    ################# DEFINE EVERY IMPLEMENTATION ################

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        """
        return minimax(self.state, evaluation, self.maximisingPlayer)[0]
