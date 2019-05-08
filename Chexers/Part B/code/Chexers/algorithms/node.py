"""
:filename: node.py
:summary: Implements Node class for use in graph/tree search algorithms.
:authors: Akira Wang (913391), Callum Holmes (899251)
"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files
from mechanics import possible_actions, apply_action, player

class Node:
    """Node superclass with core (initialized) attributes and methods
    Subclasses e.g. IDANode(Node) define and add extra functionality"""

    def __init__(self, state, parent=None):
        """
        Creates new node
        """
        self.parent = parent  # Points to parent node
        self.is_expanded = False  # Flags the fact that children have been generated
        self.is_dead = False  # DO NOT continue to explore
        self.action = None  # Action that parent made to get here
        self.state = state  # Stores data. Must have been a deepcopy
        self._children = list()  # list of children

    @property
    def children(self):
        """Generate children if not done so already, and return them"""
        if not (self.is_expanded or self.is_dead):
            for action in possible_actions(self.state, player(self.state)):
                new_child = self.new_child(apply_action(self.state, action), self)
                new_child.action = action
                self._children.append(new_child)
            self.is_expanded = True
            #### TODO: Decide ordering here
            
        return self._children

    @classmethod
    def new_child(cls, state, parent):
        """Creates new, empty instance"""
        return cls(state, parent)

    @classmethod
    def create_root(cls, initial_state):
        """Creates first instance"""
        return cls.new_child(state=initial_state, parent=None)

    def kill_tree(self):
        """Recursively kills down subtree, however will not kill ignores
        Inferred that references to ignore nodes are retained externally"""
        # Kill each subtree
        if self.is_expanded:
            for child in self.children:
                Node.kill_tree(child)
        del(self)
