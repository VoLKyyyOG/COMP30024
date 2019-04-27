""" 
:filename: player.py
:summary: Base class for any MPMixPlayer (Chexers)
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""

########################### IMPORTS ##########################
# Standard modules
from random import choice
from math import inf

# User-defined files
from mechanics import *
from algorithms.minimax import negamax_ab
from algorithms.heuristics import *
from algorithms.paranoid import paranoid
from algorithms.max_n import max_n
from algorithms.mp_mix import mp_mix

######################## MP-Mix Player #######################
class MPMixPlayer:
    MID_GAME_THRESHOLD = 3
    END_GAME_THRESHOLD = 100 # originally 99

    def __init__(self, colour):
        """
        Initialises MPMixPlayer.
        """
        self.colour = colour
        self.state = create_initial_state()

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
        
        for player in PLAYER_NAMES:
            if is_dead(self.state, player):
                return self.run_2_player()
        
        if sum([is_dead(state, i) for i in PLAYER_NAMES]) == 2:
            return self.all_dead()

        if self.start_mid_game():
            return self.mid_game()
        else:
            return self.early_game()

    def early_game(self):
        """
        :strategy: Uses the best opening moves found by the Monte Carlo method. (Booking)
        FOR NOW: greedy actions
        """
        return self.greedy_action()

    def mid_game(self):
        """
        Runs the MP-Mix Algorithm.
        """
        return mp_mix(self.state, mega_heuristic, defence_threshold=0, offence_threshold=0)

    def end_game(self):
        """
        :strategy: Use booking or a stronger quiesence search
        FOR NOW: negamax
        """
        return self.random_action()

    def all_dead(self):
        """
        :strategy: If everyone is dead, it becomes Part A
        """
        # return dijkstra for the closest (4 - number_of_exit) pieces

    def run_2_player(self):
        """
        Now that one player is dead, the problem reduces to a 2-player problem.
        :strategy: run a minimax algorithm with alpha-beta pruning.
        """
        return paranoid(self.state, mega_heuristic, self.colour, depth_left = 30)[1]

    def start_mid_game(self):
        """
        Determines when to shift strategy to the mid game given deciding factors.
        TODO: Add a flag once a player piece has been captured
        """
        if self.state["depth"] == self.MID_GAME_THRESHOLD:
            print(f"* ({self.colour}) is switching to midgame")
        return (self.state["depth"] >= self.MID_GAME_THRESHOLD)

    def start_end_game(self):
        """
        Determines when to shift strategy to the end game given deciding factors.
        TODO: Add a flag once a player has been eliminated
        """
        if self.state["depth"] == self.END_GAME_THRESHOLD:
            print(f"* ({self.colour}) is switching to endgame")
        return (self.state["depth"] >= self.END_GAME_THRESHOLD)

    def random_action(self):
        """
        Function that chooses a random action given a set of possible actions.
        """
        return choice(possible_actions(self.state, self.state["turn"]))

    def greedy_action(self):
        """
        Function that chooses the best action without considering opponent moves.
        """
        best_eval, best_action = -inf, None
        for action in possible_actions(self.state, self.colour):
            new_state = apply_action(self.state, action)
            new_eval = speed_demon(new_state)[PLAYER_HASH[self.colour]]
            if new_eval > best_eval:
                best_eval = new_eval
                best_action = action

        return best_action