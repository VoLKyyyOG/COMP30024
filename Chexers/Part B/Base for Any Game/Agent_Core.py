""" Agent_Core.py

Base class for an Agent.
Outlines attributes and methods that all Agent implementations should have.

"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files
from game_mechanics import *

class Agent:
    def __init__(self, *args):
        """Initialise Agent, especially any objects/data needed for game"""
        raise NotImplementedError

    def __str__(self):
        """Printing functionality"""
        # Think about naming agents
        print(f"{self.__class__.__name__}")

    def update(self, action):
        """Update stored State with another player's Action"""
        raise NotImplementedError

    ################## DEFINE IN SUBCLASSES ONLY #################

    def action(self):
        """Decide on an Action and return it"""
        raise NotImplementedError
        # return Action
