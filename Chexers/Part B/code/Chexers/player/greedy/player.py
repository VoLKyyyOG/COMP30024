""" player.py

Base class for any RandomPlayer.
Asks for inputs directly from command line.

"""

########################### IMPORTS ##########################
# Standard modules
from random import choice
# User-defined files
from mechanics import *
from algorithms.heuristics import speed_demon

class GreedyPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.
        """
        self.state = create_initial_state()

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action."""
        self.state = apply_action(self.state, action, self.colour)

    ################# DEFINE EVERY IMPLEMENTATION ################

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        """
        best_eval, best_action = None
        for action in possible_actions(self.state, self.colour):
            new_state = apply_action(self.state, action, self.colour)
            new_eval = speed_demon(state)[PLAYER_HASH[self.colour]]
            if best_eval < new_eval:
                best_eval = new_eval
                best_action = action
        return action
