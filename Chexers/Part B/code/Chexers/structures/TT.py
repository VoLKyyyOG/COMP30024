"""
:filename: TT.py
:summary: Implements Transposition table for use in graph/tree search algorithms.
:authors: Akira Wang (913391), Callum Holmes (899251)
"""

from mechanics import Z_hash
from collections import defaultdict

class TT:
    """Create a unique one for a player to track symmetries"""
    def __init__(self):
        self.data = defaultdict()

    def add(self, node):
        node_hash = Z_hash(node)

        if node in self:
            current = self.data[Z_hash(node)]
            # Either better or worse
            if (node.depth >= current.depth):
                assert(node != current)
                # This is a duplicate
                node.is_dead = True
                return
            else:
                # This is better
                #### TODO: Do something with the old one
                self.data[Z_hash(node)] = node
        else:
            self.data[Z_hash(node)] = node

    def __contains__(self, state):
        return Z_hash(state) in self.data.keys()
