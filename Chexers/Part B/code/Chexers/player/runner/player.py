""" player.py

Base class for any RunnerPlayer.
Plays a paranoid implementation and attempts to get to the goal fastest.
Uses number_of_pieces_lost = 0 and retrograde_dijkstra as heuristic

"""

########################### IMPORTS ##########################
# User-defined files
from mechanics import *
from moves import get_cubic, get_axial
from algorithms.adversarial_algorithms import paranoid, alpha_beta
from algorithms.heuristics import *
from algorithms.partA.search import part_A_search

PATH = list()

class RunnerPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.
        """
        self.state = create_initial_state()
        self.colour = colour

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action."""
        self.state = apply_action(self.state, action)

    def dijkstra(self, single_player=True):
        """
        :strategy: If everyone is dead, it becomes Part A. Literally Part A code...
        """
        global PATH
        FLAGS = ["MOVE", "JUMP", "EXIT"]

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

            PATH = list(map(lambda x: x.action_made, part_A_search(state)[0]))[1:]

            # (pos, flag, new_pos=None)
            PATH = [(FLAGS[x[1]], x[0]) if FLAGS[x[1]] == "EXIT" else (FLAGS[x[1]], (x[0], x[2])) for x in PATH]

            # (FLAG_str: (pos1, pos2=None))

        return PATH.pop(0)

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        """
        if is_dead(self.state, self.colour):
            return ("PASS", None)
        elif two_players_left(self.state):
            return alpha_beta(self.state, runner, self.colour)[1]
        else:
            return paranoid(self.state, runner, self.colour)[1]
