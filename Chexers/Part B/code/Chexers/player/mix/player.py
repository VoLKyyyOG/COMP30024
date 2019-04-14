""" player.py

Base class for any MPMixPlayer.

"""

########################### IMPORTS ##########################
# Standard modules
from random import choice
# User-defined files
from mechanics import *
from algorithms.minimax import negamax_ab
from algorithms.heuristics import retrograde_dijkstra, exit_diff_2_player
from algorithms.mp_mix import mp_mix as amazeballs

class MPMixPlayer:
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
        self.run_2_player_depth = 6 # Controls depth of negamax

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
        if not self.state[self.colour]:
            return ("PASS", None)
        elif two_players_left(self.state):
            return self.run_2_player()
        elif self.start_end_game():
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

    def run_2_player(self):
        """Chooses actions with 2-player algorithms as one player is dead"""
        return negamax_ab(self.state, exit_diff_2_player, depth_left=self.run_2_player_depth)[1]

    def early_game(self):
        """Uses booking/random choice to make early game decisions"""
        return self.random_action()

    def end_game(self):
        """May use booking or stronger quiesence searches to determine moves"""
        return self.random_action()

    def start_mid_game(self):
        """Determines when to shift strategy to the mid game"""
        #### TODO: Probably best to add a flag once a player piece has been
        ####       captured and transition to mid game
        if self.turn_count == self.MID_GAME_THRESHOLD:
            print(f"* ({self.colour}) is switching to midgame")
        return (self.turn_count >= self.MID_GAME_THRESHOLD)

    def start_end_game(self):
        """Determines when to shift strategy to the end game"""
        if self.turn_count == self.END_GAME_THRESHOLD:
            print(f"* ({self.colour}) is switching to endgame")
        return (self.turn_count >= self.END_GAME_THRESHOLD)

    def random_action(self):
        return choice(possible_actions(self.state))
