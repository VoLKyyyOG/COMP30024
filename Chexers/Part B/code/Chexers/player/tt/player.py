""" player.py

Base class for a Greedy Player.

"""

########################### IMPORTS ##########################
# Standard modules
from random import choice
from math import inf

# User-defined files
from mechanics import *
from algorithms.heuristics import speed_demon
from structures.gamenode import GameNode
from algorithms.node import Node
from collections import defaultdict

class GreedyPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.

        "I am speed" - Lightning McQueen

        """
        self.root = GameNode(create_initial_state(), None)
        self.colour = colour

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action.
        """
        # Steal root child with this state and overthrow
        self.root = self.root.update_root(colour, action)
        self.colour = colour

    ################# DEFINE EVERY IMPLEMENTATION ################

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program. Made it so greedy will always prefer exit moves
        """
        if len(self.root.state[self.colour]) == 0:
            return ("PASS",None)

        best_eval, best_action = -inf, None
        for child in self.root.children:
            if child.action[0] == "EXIT":
                return action
            new_eval = speed_demon(child.state)[PLAYER_HASH[self.colour]]
            if new_eval > best_eval:
                best_eval = new_eval
                best_action = action

        return best_action
