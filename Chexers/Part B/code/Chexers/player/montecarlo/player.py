""" player.py

Base class for any MCPlayer.
Runs a MC search using a cached tree - see the file for further details.

"""

########################### IMPORTS ##########################
# Standard modules
from random import choice
# User-defined files
from mechanics import *
from algorithms.MC import *

class MCPlayer:
    def __init__(self, colour):
        """Initialise the player"""
        self.root = UCTNode.create_root(create_initial_state())

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action."""
        self.root = [x for x in self.root.children if x.action == action].pop()
        self.root.overthrow()  # Delete all irrelevant siblings to free memory

    ################# DEFINE EVERY IMPLEMENTATION ################

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        """
        return self.root.search()
