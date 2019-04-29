"""
:filename: player.py
:summary: Base class for any MPMixPlayer (Chexers)
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""

########################### IMPORTS ##########################
# Standard modules
from random import choice
from copy import deepcopy
from math import inf

# User-defined files
from algorithms.partA.search import part_A_search
from mechanics import *
from algorithms.heuristics import *
from algorithms.paranoid import paranoid
from algorithms.max_n import max_n
from algorithms.mp_mix import mp_mix

PATH = list()

############## TEMP IM SORRY DONT HATE ME
def get_cubic(tup):
    """Converts axial coordinates to cubic coordinates"""
    return (tup[0], -tup[0]-tup[1], tup[1])

def get_axial(tup):
    """Converts axial coordinates to cubic coordinates"""
    return (tup[0], tup[2])

def num_opponents_dead(state):
    """Find the number of dead players"""
    return sum([is_dead(state, i) for i in PLAYER_NAMES])

######################## MP-Mix Player #######################
class MPMixPlayer:
    MID_GAME_THRESHOLD = 2
    END_GAME_THRESHOLD = 99

    def __init__(self, colour):
        """
        Initialises an MPMixPlayer agent.
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

        if num_opponents_dead(self.state) == 1:
            print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| 2 PLAYER! USING ALPHA-BETA | DEPTH = {8}")
            return self.run_2_player()

        if num_opponents_dead(self.state) == 2:
            print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| GG! 1 PLAYER GAME DIJKSTRA")
            return self.all_dead()

        if self.start_mid_game():
            return self.mid_game()
        else:
            return self.early_game()

    def early_game(self):
        """
        :strategy: Uses the best opening moves found by the Monte Carlo method. (Booking)
        """
        return self.greedy_action()

    def mid_game(self):
        """
        :strategy: Runs the MP-Mix Algorithm.
        """
        return mp_mix(self.state, mega_heuristic, defence_threshold=0, offence_threshold=0)

    def end_game(self):
        """
        :strategy: Use booking or a stronger quiesence search
        """
        return self.random_action()

    def all_dead(self):
        """
        :strategy: If everyone is dead, it becomes Part A. Literally Part A code...
        """
        global PATH

        if not bool(PATH):
            # Create part_A appropriate data
            state = dict()
            state['colour'] = deepcopy(self.colour)

            # TODO: Calculate jump distance for each piece and then return closest pieces for exit
            n_exited = self.state["exits"][self.colour]
            n = 4 - n_exited

            temp = sorted([get_cubic(tup) for tup in self.state[self.colour]], reverse=True)
            state['pieces'] = [get_axial(tup) for tup in temp[:n]]
            state['blocks'] = [get_axial(tup) for tup in temp[n:]]

            PATH = list(map(lambda x: x.action_made, part_A_search(state)))[1:]

            # (pos, flag, new_pos=None)
            FLAGS = ["MOVE", "JUMP", "EXIT"]
            PATH = [(FLAGS[x[1]], x[0]) if FLAGS[x[1]] == "EXIT" else (FLAGS[x[1]], (x[0], x[2])) for x in PATH]

            # (FLAG_str: (pos1, pos2=None))

        return PATH.pop(0)
        # return dijkstra for the closest (4 - number_of_exit) pieces

    def run_2_player(self):
        """
        :strategy: Run the paranoid algorithm with a higher depth.
                   This works because paranoid defaults to alpha-beta by ignoring
                   dead players.
        """
        return paranoid(self.state, mega_heuristic, self.colour, depth_left = 8)[1]

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
        :strategy: Choose a random action given a set of possible actions.
        """
        return choice(possible_actions(self.state, self.state["turn"]))

    def greedy_action(self):
        """
        :strategy: Choose the best action without considering opponent moves.
        """
        best_eval, best_action = -inf, None
        for action in possible_actions(self.state, self.colour):
            new_state = apply_action(self.state, action)
            new_eval = speed_demon(new_state)[PLAYER_HASH[self.colour]]
            if new_eval > best_eval:
                best_eval = new_eval
                best_action = action

        return best_action
