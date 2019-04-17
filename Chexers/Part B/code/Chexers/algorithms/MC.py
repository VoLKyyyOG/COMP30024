""" MC.py

Core functionality for Monte-Carlo tree searches and variants.
A more succinct implementation: https://github.com/brilee/python_uct/blob/master/numpy_impl.py
Unused but still curious: https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/

Process:
- 1. Select an unexpaned node by choosing highest scored branch iteratively, scoring with wins/visits via UCB1
- 2. Expand this node and randomly choose a child.
- 3. Simulate a game by randomly choosing actions, until depth_limit is reached or game finishes.
        - Return either the outcome [1 0 0] for win, or who had the max (exits + desperation)
- 4. Backpropagate outcome to re-evaluate wins and visits for parent nodes

"""

########################### IMPORTS ##########################
# Standard modules
import collections
import numpy as np
import math
from random import choice
# User-defined files
from mechanics import *
from algorithms.node import Node
from algorithms.heuristics import *

class UCTNode(Node):
    total_visits = 0   # Tracks total UCT visits
    scale = math.sqrt(2)    # Sets scaling for exploration in UCB1 equations

    # Number of times MC will select and simulate a node
    # This is 'sample size' - larger sample size will give better estimates
    iterations = 25

    # Number of moves made before cutting off a simulation with heuristic evaluation
    depth_limit = 25

    def __init__(self, state, parent=None):
        super().__init__(state, parent)
        self.wins = np.zeros([N_PLAYERS], dtype=float)  # Total wins/player

    @property
    def visits(self):
        """Returns total number of visits, inferring from children"""
        return sum(self.wins)

    @property
    def score(self):
        """Computes UCB1 score, i.e. exploitation + exploration"""
        return self.Q() + self.U()

    def Q(self):
        """Fetches exploitation factor, i.e. measures whether this path wins"""
        return self.wins[PLAYER_HASH[player(self.state)]] / (self.visits + 1)

    def U(self):
        """Fetches exploration factor, i.e. measures extent of unexploration"""
        return UCTNode.scale * np.sqrt(math.log(UCTNode.total_visits) / (self.visits + 1))

    def select_simulation(self):
        """Step 1 & 2 - recurse down to the best, unexpanded child.
        Then expand it and pick a child to simulate
        :returns: chosen state to simulate"""
        current = self
        while current.is_expanded:
            scores = np.asarray([child.score for child in current.children])
            current = current.children[np.argmax(scores)]

        # Expand child and choose (randomly) a child of this to simulate
        return choice(current.children)

    @staticmethod
    def apply_heuristics(state):
        """Evaluate a terminal simulation state with heuristics"""
        total_exits = np.asarray(exits(state))
        if game_over(state):
            # Return who won e.g. 1 0 0 if red. Otherwise 0.33 0.33 0.33 if drawn
            result = (total_exits == MAX_EXITS).astype(float)
        else:
            # Returns who is leading (or the tie)
            total = total_exits + np.asarray(desperation(state)) + np.asarray(speed_demon(state))
            result = (total == total.max()).astype(float)
        return result / np.sum(result)

    def simulate(self):
        """Run a simulation of this (unexpanded) node and return result"""
        # TODO - Maybe quiescence search result to depth_limit is better?
        # This would make MC more like A*
        current = self.state

        # IDEA: Push to depth_limit randomly and return heuristic evaluation
        for _ in range(UCTNode.depth_limit):
            try:
                chosen_action = choice(possible_actions(current, player(current)))
                current = apply_action(current, chosen_action)
            except:
                break
                # No actions exist - the game is over

        return UCTNode.apply_heuristics(current)

    def backpropagate(self, result):
        """Updates parents recursively (note that visits is implicit on wins)
        Assumes the simulated child has already updated"""
        current = self
        UCTNode.total_visits += sum(result)  # Result must total 1 due to evaluate function
        while isinstance(current, UCTNode):
            current.wins = current.wins + result
            current = current.parent

    def overthrow(self):
        """Recursively kill down each subtree, side-effect of updating wins/visits"""
        for sibling in self.parent.children:
            if sibling != self:
                UCTNode.total_visits -= sibling.visits
                sibling.kill_tree()
        del(self.parent)
        self.parent = None

    def search(self, iterations):
        """Performs the UCT search on a node for given iterations
        :returns: optimal action based on search"""
        for _ in range(iterations):
            leaf = self.select_simulation()  # Steps 1 and 2
            result = leaf.simulate()  # Step 3
            leaf.backpropagate(result)   # Step 4
        # Return action of child that was most visited
        #### TODO: Some sources say focus on visits, others say wins,
        #### and one presumes others would say wins/visits. I don't know
        #### What's best.
        child_visits = np.asarray([child.visits for child in self.children])
        chosen_action = self.children[np.argmax(child_visits)].action
        return chosen_action

    def __str__(self):
        return "  > " * depth(self.state) +
            f"{id(self)} inherits from {id(self.parent)} - wins ({self.wins})"

    def recursive_print(self):
        """Prints tree structure"""
        print(self)
        if self.is_expanded:
            for child in self.children:
                child.recursive_print()
