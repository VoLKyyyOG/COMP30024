""" Agent_Minimax.py

Runs Minimax on TTT.

"""

########################### IMPORTS ##########################
# Standard modules
from math import inf
# User-defined files
from game_mechanics import *
from Agent_Core import *

class Agent:
    def __init__(self, player):
        """Initialise Agent, especially any objects/data needed for game"""
        # Check player format is correct
        self.player = player
        self.state = State(INITIAL_BOARD, player)
        raise NotImplementedError

    def __str__(self):
        """Printing functionality"""
        # Think about naming agents
        print(f"{self.__class__.__name__} is Player {self.player}")

    def update(self, action):
        """Update stored State with another player's Action"""
        # Reformat input into an Action object
        self.state.apply_action(action)
        raise NotImplementedError

    ################## DEFINE IN SUBCLASSES ONLY #################

    def action(self):
        """Decide on an Action and return it"""
        raise NotImplementedError
        # return Action
