"""
:filename: gamenode.py
:summary: Implements GameNode class for use in graph/tree search algorithms.
:authors: Akira Wang (913391), Callum Holmes (899251)

Properties of GAMENODE (NOT INHERITED):
- node.counts[node.hash()] --> # visits in the game
- node.hash() --> Z_hash(node.state)
- node.update_root(colour, action)
- node.get_node(state)

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
from mechanics import N_PLAYERS

class GameNode(Node):
    """
    :summary: Extends functionality of a base node to work with players
    Allows tracking of repeated states during a game as well as
    Efficient storage of all generated nodes
    Must be accessed by heuristics/etc. to be most effective.
    """

    def __init__(self, state, parent=None):
        super().__init__(state, parent)
        self.evaluation = np.zeros(N_PLAYERS)
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
        self.counts[Z_hash(node)] += 1

    def update_root(self, colour, action):
        """
        Called when an actual game move has been decided, updates tree
        :returns: new root for player to use
        """
        root = [x for x in self.root.children if x.action == action].pop(0)
        root.overthrow()  # Delete all irrelevant siblings to free memory
        root.clean_tree()

        # Add to storage
        root.TT[root.hash] = root
        root.increment(root)
        return root

    def get_node(self, state):
        """
        Can jump to any (explored) state given the state
        """
        return self.TT[Z_hash(state)]

    # Overriden behaviour
    @property
    def children(self):
        """
        Process generated children with TT prior to returning them
        :returns: [children_list] or [] if dead
        """
        for child in self.children:
            # Use TT to verify it should be considered
            node_hash = Z_hash(child.state)
            if node_hash in self.TT:
                current = self.data[node_hash]
                # Either better or worse
                if (child.depth >= current.depth):
                    # This is a duplicate
                    current.is_dead = True
                    continue
                # This is better, so flag the older one dead
                current.is_dead = True

            self.data[node_hash] = node
            #### TODO: Decide ordering here

        return self.children
