""" 
:filename: player.py
:summary: Base class for any MPMixPlayer (Chexers)
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""

########################### IMPORTS ##########################
# Standard modules
from random import choice

# User-defined files
from mechanics import *
from algorithms.minimax import negamax_ab
from algorithms.heuristics import exit_diff_2_player #retrograde_dijkstra
from algorithms.mp_mix import mp_mix as amazeballs

######################## MP-Mix Player #######################
class MPMixPlayer:
    MID_GAME_THRESHOLD = 18
    END_GAME_THRESHOLD = 99

    def __init__(self, colour):
        """
        Initialises MPMixPlayer.
        """
        self.colour = colour
        self.colour_code = colour[0] # This will be 'r', 'g', 'b' (save space)
        self.state = create_initial_state()
        self.run_2_player_depth = 6 # Controls the depth of negascout

    def update(self, colour, action):
        """
        Updates a players action and adds a turn count.
        """
        self.state = apply_action(self.state, action)

    def action(self):
        """
        Returns an action given conditions.
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
        """
        Runs the MP-Mix Algorithm.
        """
        return self.random_action()

        #### TODO: mp_mix(state, heuristic, defenceThreshold, offenceThreshold, maximisingPlayer)
        ####       heuristic = exited_pieces + number_of_pieces_captured + number_of_pieces_lost + distance_to_goal
        ####       will need to add weighting to each of them. ideally, we want number of pieces captured > 0, number of pieces = 0
        ####       return amazeballs(self.state, exit_diff_2_player, 0, 0, self.colour)

    def run_2_player(self):
        """
        Now that one player is dead, the problem reduces to a 2-player problem.
        :strategy: run a negamax algorithm with alpha-beta pruning.
        """
        return negamax_ab(self.state, exit_diff_2_player, depth_left=self.run_2_player_depth)[1]

    def early_game(self):
        """
        :strategy: Uses the best opening moves found by the Monte Carlo method. (Booking)
        FOR NOW: random choices.
        """
        return self.random_action()

    def end_game(self):
        """
        :strategy: Use booking or a stronger quiesence search
        FOR NOW: negamax
        """
        return self.random_action()

    def start_mid_game(self):
        """
        Determines when to shift strategy to the mid game given deciding factors.
        TODO: Add a flag once a player piece has been captured
        """
        if self.turn_count == self.MID_GAME_THRESHOLD:
            print(f"* ({self.colour}) is switching to midgame")
        return (self.turn_count >= self.MID_GAME_THRESHOLD)

    def start_end_game(self):
        """
        Determines when to shift strategy to the end game given deciding factors.
        TODO: Add a flag once a player has been eliminated
        """
        if self.turn_count == self.END_GAME_THRESHOLD:
            print(f"* ({self.colour}) is switching to endgame")
        return (self.turn_count >= self.END_GAME_THRESHOLD)

    def random_action(self):
        """
        Function that chooses a random action given a set of possible actions.
        """
        return choice(possible_actions(self.state, self.state["turn"]))
