"""
:filename: player.py
:summary: Base class for any MPMixPlayer (Chexers)
:authors: Akira Wang (913391), Callum Holmes (XXXXXX)
"""

########################### IMPORTS ##########################

# Standard modules
from math import inf

# User-defined files
from mechanics import create_initial_state, num_opponents_dead, apply_action, possible_actions, get_remaining_opponent
from moves import get_axial, get_cubic
from book import opening_moves

from algorithms.mp_mix import mp_mix, paranoid
from algorithms.partA.search import part_A_search
from algorithms.heuristics import achilles_vector, end_game_heuristic, speed_demon

# Global imports
from mechanics import PLAYER_HASH

PATH = list()

######################## MP-Mix Player #######################
class MPMixPlayer:
    MID_GAME_THRESHOLD = 9 # The first three moves for each player
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
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| {self.state[self.colour]}")

        if not self.state[self.colour]:
            return ("PASS", None)

        if num_opponents_dead(self.state) == 1:
            return self.run_2_player()

        if num_opponents_dead(self.state) == 2:
            print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| GG! 1 PLAYER GAME DIJKSTRA")
            return self.djikstra()

        if self.start_mid_game():
            return self.mid_game()
        else:
            return self.early_game()

    def early_game(self):
        """
        :strategy: Uses the best opening moves found by the Monte Carlo method. (Booking)
        """
        return opening_moves(self.state, self.colour) if not False else paranoid(self.state, achilles_vector, self.colour)

    def mid_game(self):
        """
        :strategy: Runs the MP-Mix Algorithm.
        :returns: The best evaluated function. If True is returned, we are at a good level to attempt a greedy approach.
        """
        action = mp_mix(self.state, end_game_heuristic, defence_threshold=0, offence_threshold=0)

        if action == True: # if True then run Greedy
            return self.end_game()
        return action

    def run_2_player(self):
        """
        :strategy: Run the paranoid algorithm with a higher depth.
                   This works because paranoid defaults to alpha-beta by ignoring
                   dead players.
        """
        action = mp_mix(self.state, end_game_heuristic, defence_threshold=0, offence_threshold=0, two_player=True)
        if action is False: # If False just use Dijkstra (we are sufficiently ahead)
            action =  self.djikstra(single_player=False)
        elif action is True: # if True then run Greedy
            return self.end_game()
        return action

    def end_game(self):
        """
        :strategy: Use booking or a stronger quiesence search
        """
        return self.greedy_action()

    def djikstra(self, single_player=True):
        """
        :strategy: If everyone is dead, it becomes Part A. Literally Part A code...
        """
        global PATH
        FLAGS = ["MOVE", "JUMP", "EXIT"]

        # AKIRA - RETURN DIJKSTRA'S GIVEN A PLAYER IS STILL ALIVE
        if not single_player:
            state = dict()
            state['colour'] = self.colour

            # TODO: Calculate jump distance for each piece and then return closest pieces for exit
            n_exited = self.state["exits"][self.colour]
            n = 4 - n_exited
        
            alive_opponent = get_remaining_opponent(self.state)

            temp = sorted([get_cubic(tup) for tup in self.state[self.colour]], reverse=True)
            state['pieces'] = [get_axial(tup) for tup in temp[:n]]
            state['blocks'] = [get_axial(tup) for tup in temp[n:]] + self.state[alive_opponent]

            action = list(map(lambda x: x.action_made, part_A_search(state)[0]))[1] # attempting the runner so take first move
            # (pos, flag, new_pos=None)

            return (FLAGS[action[1]], action[0]) if FLAGS[action[1]] == "EXIT" else (FLAGS[action[1]], (action[0], action[2]))
            
        if not bool(PATH):
            # Create part_A appropriate data
            state = dict()
            state['colour'] = self.colour

            # TODO: Calculate jump distance for each piece and then return closest pieces for exit
            n_exited = self.state["exits"][self.colour]
            n = 4 - n_exited

            temp = sorted([get_cubic(tup) for tup in self.state[self.colour]], reverse=True)
            state['pieces'] = [get_axial(tup) for tup in temp[:n]]
            state['blocks'] = [get_axial(tup) for tup in temp[n:]]

            PATH = list(map(lambda x: x.action_made, part_A_search(state)[0]))[1:]

            # (pos, flag, new_pos=None)
            PATH = [(FLAGS[x[1]], x[0]) if FLAGS[x[1]] == "EXIT" else (FLAGS[x[1]], (x[0], x[2])) for x in PATH]

            # (FLAG_str: (pos1, pos2=None))

        return PATH.pop(0)

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