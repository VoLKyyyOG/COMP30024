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
        #print(f"\nHash: {self.root.hash()}\n")
        self.colour = colour

    def debug(self):
        self.debugger(self.root)

    @staticmethod
    def debugger(current):
        """Modified referee calls this, allows for navigation of search tree
        Can call anywhere in execution"""
        while(1):
            chosen = input(">> Change node (c) literal eval (e) parent (p) print state info (s) quit (q) >> ")
            if chosen not in "cpesq":
                print(">> Invalid, try again.")
            elif chosen == "c":
                try:
                    nodehash = int(input("Specify hash for state >> ").strip())
                    current = current.get_node(nodehash)
                except:
                    print(">> invalid, try again.")
            elif chosen == "p":
                current = current.parent
                print(">> Navigated to parent.")
            elif chosen == "e":
                try:
                    exec(input("Object called current, it is a gamenode. >> "))
                except:
                    print(">> invalid, try again.")
            elif chosen == "s":
                current.printer(current.state)
                print(f"Depth {current.state['depth']}, colour {current.state['turn']} full_eval {current.fully_evaluated}\nChildren: ")
                for child in current.children:
                    print(f"{child.hash()} - {child.action}",end="")
                    if child.action in current.child_evaluations.keys():
                        print(f" - {current.child_evaluations[child.action]}")
                    else:
                        print("")
            else:
                break

    ################# DEFINE EVERY IMPLEMENTATION ################

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program. Made it so greedy will always prefer exit moves
        """
        if len(self.root.state[self.colour]) == 0:
            return ("PASS",None)

        best_eval, best_action = -inf, None

        # TODO: Use TT to prevent recalculation

        for child in self.root.children:
            if child.action[0] == "EXIT":
                return child.action
            new_eval = speed_demon(child.state)[PLAYER_HASH[self.colour]]
            self.root.child_evaluations[child.action] = new_eval
            if new_eval > best_eval:
                best_eval = new_eval
                best_action = child.action
        self.root.fully_evaluated = True
        return best_action
