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
from structures.ttplayer import TTPlayer

class GreedyPlayer(TTPlayer):

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program. Made it so greedy will always prefer exit moves
        """
        if not self.root.state[self.colour]:
            return ("PASS", None)

        best_eval, best_action = -inf, None

        # TODO: Use TT to prevent recalculation

        for child in self.root.children:
            if child.action[0] == "EXIT":
                return child.action
            new_eval = speed_demon(child.state)[PLAYER_HASH[self.colour]]
            self.root.child_evaluations[child.action] = new_eval
            # ONLY select non-repetitive moves
            if new_eval > best_eval:
                best_eval = new_eval
                best_action = child.action
        self.root.fully_evaluated = True
        if best_action == None:
            print("The none error.")
            GameNode.debugger(self.root)
        return best_action
