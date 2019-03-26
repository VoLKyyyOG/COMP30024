""" transposition.py

Implements a tranposition table for removing symmetries down the branch and across the branch.
- WHY: prop. leaf nodes of all generated nodes ~ 95% (so making tons of copies is BAD IDEA)

"""

########################## IMPORTS ############################
# Standard modules
from collections import defaultdict

# User-defined files
from classes import *

class TT:
    def __init__(self):
        self.table = defaultdict(list)
        self.size = 0

    def append(self, node):
        """Appends a node instance to the TT with key hashed_state"""
        self.table[Z_hash(node.state)].append(node)
        self.size += 1

    def in_table(self, node):
        """Checks if a node is in the TT i.e. exists in memory"""
        return (Z_hash(node.state) in self.table.keys())
