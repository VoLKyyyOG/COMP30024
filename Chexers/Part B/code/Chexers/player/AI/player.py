""" player.py

Base class for any AIPlayer.

"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files
from mechanics import *
from random import choice
from .minimax import alphabeta_search
from .heuristics import retrograde_dijkstra

class AIPlayer:
    MID_GAME_THRESHOLD = 18
    END_GAME_THRESHOLD = 150

    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.
        """
        self.colour = colour
        self.colour_code = colour[0] # This will be 'r', 'g' etc.
        self.state = create_initial_state()
        self.turn_count = 0

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action."""
        self.state = apply_action(self.state, action)
        self.turn_count += 1

    ################# DEFINE EVERY IMPLEMENTATION ################

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        """
        if self.start_end_game():
            return self.end_game()
        elif self.start_mid_game():
            return self.mid_game()
        else:
            return self.early_game()

    def mid_game(self):
        """Runs amazing 3-player algorithms"""
        return choice(possible_actions(self.state))
        # When they've been coded

    def early_game(self):
        """Uses booking/random choice to make early game decisions"""
        return choice(possible_actions(self.state))

    def end_game(self):
        """Given two players are left, uses optimal 2-player strategy to choose
        action. """
        return alphabeta_search(self.state, get_score, self.colour)

    def start_mid_game(self):
        """Determines when to shift strategy to the mid game"""
        return (self.turn_count >= AIPlayer.MID_GAME_THRESHOLD)

    def start_end_game(self):
        """Determines when to shift strategy to the end game"""
        return (two_players_left(self.state) or self.turn_count >= AIPlayer.END_GAME_THRESHOLD)
