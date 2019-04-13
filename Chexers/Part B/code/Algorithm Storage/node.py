""" Node.py

Implements Node class for use in graph/tree search algorithms.

"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files
from mechanics import possible_actions, apply_action

class Node:
    """Node superclass with core (initialized) attributes and methods
    Subclasses e.g. IDA_Node(Node) define and add extra functionality"""

    def __init__(self, parent):
        """Creates new node. NOTE: it inherits (not updates) parent state"""
        self.parent = parent # Points to parent node
        self.depth = self.parent.depth + 1 if parent else 0
        self.is_expanded = False # Flags expanded nodes
        self.is_dead = False # DO NOT continue to explore
        self.action_made = None # Action that parent made to get here
        self.state = None # Stores data
        self.children = list() # Stores addresses of children

    def create_children(self):
        """Given a list of action tuples, create new children."""
        if not self.is_expanded and not self.is_dead:
            for action in possible_actions(self.state):
                new_child = self.new_child()
                new_child.state = apply_action(deepcopy(self.state), action)
                self.children.append(new_child)
            self.is_expanded = True

    @staticmethod
    def new_child(parent):
        """Creates new instance"""
        return parent.__class__(parent)

    @classmethod
    def create_root(cls, initial_state):
        """Creates first instance"""
        root = cls.new_child(parent=None)
        root.state = initial_state
        return root
