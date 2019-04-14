""" player.py

Base class for any AIPlayer.

"""

########################### IMPORTS ##########################
# Standard modules
from random import choice
# User-defined files
from mechanics import *
from .minimax import alphabeta_search
from .heuristics import retrograde_dijkstra, exit_diff_2_player
from .mp_mix import mp_mix as amazeballs

class AIPlayer:
    MID_GAME_THRESHOLD = 18
    END_GAME_THRESHOLD = 99

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
        return self.random_action()
        
        #### TODO: mp_mix(state, heuristic, defenceThreshold, offenceThreshold, maximisingPlayer)
        ####       heuristic = exited_pieces + number_of_pieces_captured + number_of_pieces_lost + distance_to_goal
        ####       will need to add weighting to each of them. ideally, we want number of pieces captured > 0, number of pieces = 0
        ####       return amazeballs(self.state, exit_diff_2_player, 0, 0, self.colour)

    def early_game(self):
        """Uses booking/random choice to make early game decisions"""
        return self.random_action()

    def end_game(self):
        """Given two players are left, uses optimal 2-player strategy to choose
        action. """
        #print(f"{self.turn_count}, running alphabeta on {self.state}")
        if not self.state[self.colour]:
            return ("PASS", None)
        elif two_players_left(self.state):
            return alphabeta_search(self.state, exit_diff_2_player, self.colour)
        else:
            return self.random_action()

    def start_mid_game(self):
        """Determines when to shift strategy to the mid game"""
        #### TODO: Probably best to add a flag once a player piece has been
        ####       captured and transition to mid game
        if self.turn_count == AIPlayer.MID_GAME_THRESHOLD:
            print(f"* ({self.colour}) is switching to midgame")
        return (self.turn_count >= AIPlayer.MID_GAME_THRESHOLD)

    def start_end_game(self):
        if self.turn_count == AIPlayer.END_GAME_THRESHOLD:
            print(f"* ({self.colour}) is switching to endgame")
        """Determines when to shift strategy to the end game"""
        return (two_players_left(self.state) or self.turn_count >= AIPlayer.END_GAME_THRESHOLD)

    def random_action(self):
        return choice(possible_actions(self.state))
