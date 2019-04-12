""" Agent_File.py

Class for an Agent that reads actions from a file.
Outlines attributes and methods that any Agent_File implementation should have.

Notes:
- Would use to replicate a game history recorded in a file.
- Would want "player" to be an attribute of Agent, so shouldn't be written
    in command line - it's already in the class

"""

########################### IMPORTS ##########################
# Standard modules
from ast import literal_eval

# User-defined files
from game_mechanics import *
from Agent_Core import *

class Agent_File(Agent):
    def __init__(self, *args, file_str):
        super().__init__(*args)
        fyle = open(self.file_str, "r")
        self.action_strs = fyle.read().strip().split("\n") # list of all actions in string
        fyle.close()

    def action(self):
        """Parses an action from the command line and return it
        By default, expects comma-separated values
        """
        action = self.action_strs.pop().split(",")
        return Action(*map(lambda x: literal_eval(x.strip()), action))
        raise NotImplementedError
