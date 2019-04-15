""" Node.py

Implements Node class for use in graph/tree search algorithms.

"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files
from mechanics import *

class Node:
    """Node superclass with core (initialized) attributes and methods
    Subclasses e.g. IDANode(Node) define and add extra functionality"""

    def __init__(self, state, parent=None):
        """Creates new node"""
        self.parent = parent # Points to parent node
        self.depth = self.parent.depth + 1 if parent else 0
        self.is_expanded = False # Flags expanded nodes
        self.is_dead = False # DO NOT continue to explore
        self.action = None # Action that parent made to get here
        self.state = state # Stores data. Must have been a deepcopy

        self._children = dict{} # {action: Node}

    @property
    def children(self):
        """Generate children if not done so already, and return them"""
        if not self.is_expanded and not self.is_dead:
            for action in possible_actions(self.state):
                new_child = self.new_child(apply_action(self.state, action))
                self._children[action] = new_child
            self.is_expanded = True
            # Decide ordering here, and ONLY here
            # UCT relies on this order
        return self._children

    @staticmethod
    def new_child(state, parent):
        """Creates new, empty instance"""
        return parent.__class__(state, parent)

    @classmethod
    def create_root(cls, initial_state):
        """Creates first instance"""
        root = cls.new_child(parent=None)
        root.state = initial_state
        return root
