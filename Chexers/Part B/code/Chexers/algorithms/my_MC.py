""" MC.py

Core functionality for Monte-Carlo tree searches and variants.
A more succinct implementation: https://github.com/brilee/python_uct/blob/master/numpy_impl.py

"""

########################### IMPORTS ##########################
# Standard modules
import collections
import numpy as np
import math
# User-defined files
from mechanics import *
from algorithms.node import Node

class UCTNode(Node):
    def __init__(self, state, parent=None):
        super().__init__(state, parent)
        # In this tree, is_expanded flags the fact you've started evaluating it
        # Statistics for MC
        max_children = MAX_ACTIONS_PER_PIECE * state[player(state)]
        self.child_priors = np.zeros([max_children], dtype=np.float32)  # Probabilities of all children
        self.child_wins = np.zeros([max_children], dtype=np.float32)    # Win count of all children
        self.child_visits = np.zeros([max_children], dtype=np.float32)  # Visitations of all children

    def action_index(self, action):
        """Maps an action to its index"""
        # TODO: Update code below with the difference
        return self.children.index(action)

    @property
    def visits(self):
        """Returns number of visitations of this node/state"""
        assert(self.parent)
        return self.parent.child_visits[self.action] # self.action is an index for child_visits array

    @visits.setter
    def visits(self, value):
        assert(self.parent)
        self.parent.child_visits[self.action] = value

    @property
    def total_value(self):
        assert(parent)
        return self.parent.child_wins[self.action]

    @total_value.setter
    def total_value(self, value):
        assert(parent)
        self.parent.child_wins[self.action] = value

    def child_Q(self):
        """Total number of wins as a proportion of total visits i.e. mean_evaluation
        :returns: array of proportions, which can range from 0 to just below 1"""
        return self.child_wins / (1 + self.child_visits)   # Prevent zero division

    def child_U(self):
        """Confidence in the children. Alternative formulation is
        c * sqrt(ln N_total / n_(child)_node). Either way, N weights slowly over time."""
        # c = sqrt(2)
        # return c * math.sqrt(math.log(self.TOTAL) / (self.child_visits + 1))
        return math.sqrt(self.visits) * (self.child_priors / (1 + self.child_visits))

    def best_child(self):
        """Returns numpy index of the best child according to UCT
        Used to define evaluation for parent"""
        return np.argmax(self.child_Q() + self.child_U())

    def choose_child(self):
        """Fetch the best child in the ENTIRE tree"""
        current = self
        while current.is_expanded:
            best_action = current.best_child()
            current = current.get_child(best_action)
        return current

    def expand(self, child_priors):
        """Update child priors and label node as expanded"""
        self.is_expanded = True
        self.child_priors = child_priors

    def get_child(self, action):
        """This action was desirable - create a node for it (if not already a child)
        Return this node"""
        if action not in self.children:
            self.children[action] = UCTNode(
              self.state.play(action), action, parent=self)
        return self.children[action]

    def backup(self, value_estimate: float):
        current = self
        while current.parent is not None:
            current.visits += 1
            current.total_value += (value_estimate *
            self.state.to_play)
            current = current.parent

class StatisticsNode(Node):
    def __init__(self):
        self.parent = None
        self.child_wins = collections.defaultdict(float)
        self.child_visits = collections.defaultdict(float)

def UCT_search(state, num_reads):
    """Performs the UCT search on a state with num_reads iterations"""
    root = UCTNode(state, action=None, parent=StatisticsNode())
    for _ in range(num_reads):
        leaf = root.choose_child()
        child_priors, value_estimate = NeuralNet.evaluate(leaf.state)
        leaf.expand(child_priors)
        leaf.backup(value_estimate)
    return np.argmax(root.child_visits)


class NeuralNet():
    @classmethod
    def evaluate(self, state):
        return np.random.random([362]), np.random.random()

num_reads = 10000
UCT_search(GameState(), num_reads)
