""" transposition.py

Implements a tranposition table for removing symmetries down the branch and across the branch.

- 2. Use a mega transpositon table to capture 'across the branch repetition' (i.e. RSR) and 'down the branch' (li.e. kill inf loops)
    - WHY: prop. leaf nodes of all generated nodes ~ 95% (so making tons of copies is BAD IDEA)
    - TT: a defaultdict(int). Keys of the form hash(state): instance.
    - If you want to get 'down the branch' history: iterate through hash(instance.state) until you hit null (starting position)
    - If you want to check 'across the branch': check if hash(state) in TT.keys!

Abstract the handling of symmetries so it can be used in Part A and B

"""

########################## IMPORTS ############################
from collections import defaultdict
from classes import *

########################## GLOBALS ############################
def TT:
    def __init__(self):
        self.table = defaultdict(list)
        self.size = 0

    def append(self, node):
        """Appends a node instance to the TT with key hashed_state"""
        self.table[node.hashed_state].append(node)
        self.size += 1

    def in_table(self, node):
        """Checks if a node is in the TT i.e. exists in memory"""
        return (node.hashed_state in self.table.keys())

    def get_path(self, leaf_node):
        """Given a leaf_node, if in TT, returns ancestry"""
        if self.in_table(leaf_node):
            path = list()
            node = leaf_node
            while (node is not None):
                # Iterate through nodes until parent is NONE
                path.append(node)
                node = node.parent
            return path.reversed()

    def trim_duplicates(self):
        """Finds duplicates that exist and reduces tree"""
        pass


    """ SHOULD BE UN-NECESSARY IF WE DO THIS THING RIGHT
    def trim_path_duplicates(self, leaf_node):
        node = leaf_node
        while (node is not None):
            if self.in_table(node):
                # See if the repetition is a parent node
                original = node
                while (original is not None):
                    if (original.hashed_state == node.hashed_state):
                        break # This is it!
                    original = original.parent
                if (original == None):
                    # You made it to the root, so it's not a parent - nothing to kill
                    return
                else:
                    # You found a copy!
                    # Kill the leaf_node
                    # Be sure to remove killed objects from the TT
                    # Label path as looping and of high cost
    """
