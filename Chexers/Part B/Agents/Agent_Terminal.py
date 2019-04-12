""" Agent_Terminal.py

Class for an Agent that uses actions from command line.
Outlines attributes and methods that any Agent_Terminal implementation should have.

Notes:
- Will need to disable game timer for this
- Consider ability to refer to Agent.state and tell if Action is valid
- Would want "player" to be an attribute of Agent, so as not write it again
    in command line - it's already in the class!!

"""

########################### IMPORTS ##########################
# Standard modules
from ast import literal_eval

# User-defined files
from game_mechanics import *
from Agent_Core import *

class Agent_Terminal(Agent):
    def action(self):
        """Parses an action from the command line and return it
        By default, expects comma-separated values, but any form of input can be
        implemented here.
        """
        raise NotImplementedError
        while(True):
            data = input("Enter next action >>> ")
            try:
                return Action(*literal_eval(data))
            except SyntaxError:
                print("ERROR: Invalid input")
