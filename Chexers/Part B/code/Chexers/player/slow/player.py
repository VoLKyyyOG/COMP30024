""" player.py

Base class for any RunnerPlayer.
Plays a paranoid implementation and attempts to get to the goal fastest.
Uses number_of_pieces_lost = 0 and retrograde_dijkstra as heuristic

"""

########################### IMPORTS ##########################
# User-defined files
from mechanics import *
from moves import get_cubic, get_axial
from algorithms.adversarial_algorithms import max_n
from algorithms.heuristics import *
from algorithms.partA.search import part_A_search
from random import choice

PATH = list()

class Slow:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.
        """
        self.state = create_initial_state()
        self.depth = 0
        self.colour = colour

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action."""
        self.state = apply_action(self.state, action)

    def action(self):
        self.depth += 1
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        """
        if self.depth%100000 == 0:
            return choice(possible_actions(self.state, self.colour))

        if is_dead(self.state, self.colour):
            return ("PASS", None)
        else:
            action = max_n(self.state, runner)[1]
            if action == None:
                action = possible_actions(self.state, self.colour, sort=True)[0]
            return action
