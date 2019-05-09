"""
:filename: gamenode.py
:summary: Implements GameNode class for use in graph/tree search algorithms.
:authors: Akira Wang (913391), Callum Holmes (899251)

Properties of GAMENODE (NOT INHERITED):
- node.counts[node.hash()] --> # visits in the game
- node.hash() --> Z_hash(node.state)
- node.update_root(colour, action)
- node.get_node(statehash)

INHERITED:
- node.children
    --> gets children
    --> side effect auto-labels deads if they are in TT
    --> RETURNS [] IF DEAD
- node.parent
- node.depth
- node.action
- node.is_expanded
- node.is_dead
"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files
from collections import defaultdict
from structures.node import *
from mechanics import Z_hash
from mechanics import N_PLAYERS, PLAYER_NAMES
import numpy as np

class GameNode(Node):
    """
    :summary: Extends functionality of a base node to work with players
    Allows tracking of repeated states during a game as well as
    Efficient storage of all generated nodes
    Must be accessed by heuristics/etc. to be most effective.
    """

    def __init__(self, state, parent=None):
        super().__init__(state, parent)
        self.child_evaluations = dict()
        if parent:
            self.counts = parent.counts  # Tracks actual game
            self.TT = parent.TT  # Inherit memory if parent exists
        else:
            self.counts = defaultdict(int)
            self.TT = defaultdict()

        # Add to storage
        self.TT[self.hash] = self
        self.increment(self)

    def hash(self):
        """
        Wrapper function for hashing a node's state
        :return: hash
        """
        return Z_hash(self.state)

    def increment(self, node):
        """
        Increase number of visits to a node
        """
        self.counts[node.hash] += 1

    def update_root(self, colour, action):
        """
        Called when an actual game move has been decided, updates tree
        :returns: new root for player to use
        """
        root = [x for x in self.children if x.action == action].pop(0)
        root.overthrow()  # Delete all irrelevant siblings to free memory
        root.clean_tree()

        # Add to storage
        root.TT[root.hash] = root
        root.increment(root)
        return root

    def get_node(self, state_hash):
        """
        Can jump to any (explored) state given the state
        """
        return self.TT[state_hash]

    @staticmethod
    def printer(state):
        from algorithms.partA.formatting import print_board
        board_dict = {}
        for player in PLAYER_NAMES:
            for i in state[player]:
                board_dict[i] = f"{player}"
        print_board(board_dict)

    # Overriden behaviour
    def expand(self):
        assert(not self.is_expanded)
        if self.is_dead: return
        for action in possible_actions(self.state, player(self.state)):
            new_child = self.new_child(apply_action(self.state, action), self)
            new_child.action = action
            self._children.append(new_child)

            # Use TT to verify it should be considered
            node_hash = new_child.hash()
            if node_hash in self.TT:
                current = self.TT[node_hash]
                if (new_child.state['depth'] >= current.state['depth']) and new_child != current:
                    # This is a duplicate
                    new_child.is_dead = True
                else:
                    # This is better, so flag the older one dead
                    current.is_dead = True

            self.TT[node_hash] = new_child

        self.is_expanded = True
        #### TODO: Decide ordering here
