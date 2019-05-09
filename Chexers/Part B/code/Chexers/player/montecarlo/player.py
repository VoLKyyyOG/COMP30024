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
from structures.gamenode import GameNode
from structures.ttplayer import TTPlayer

class MCPlayer(TTPlayer):
    def __init__(self, colour):
        """Initialise the player"""
        super().__init__(colour)

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        """
        return self.root.search()
