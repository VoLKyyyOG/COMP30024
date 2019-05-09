"""
:filename: gamenode.py
:summary: Implements GameNode class for use in graph/tree search algorithms.
:authors: Akira Wang (913391), Callum Holmes (899251)

Properties of GAMENODE (NOT INHERITED):
- node.counts[node.hash] --> # visits in the game
- node.hash --> Z_hash(node.state)
- node.update_root(action, kill) --> reassigns root, trims tree if kill
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
from mechanics import Z_hash, draw_hash
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
        self.fully_evaluated = False
        if parent:
            self.counts = parent.counts  # Tracks actual game
            self.TT = parent.TT  # Inherit memory if parent exists
        else:
            self.counts = defaultdict(int)
            self.TT = defaultdict()

        # Add to storage
        self.TT[self.hash] = self
        self.increment(self)

    def hash(self, draws=False):
        """
        Wrapper function for hashing a node's state
        :return: hash
        """
        if draws:
            return draw_hash(self.state)
        else:
            return Z_hash(self.state)

    def increment(self, node):
        """
        Increase number of visits to a node
        """
        self.counts[self.hash(draws=True)] += 1

    def update_root(self, action, kill=True):
        """
        Called when an actual game move has been decided, updates tree
        :returns: new root for player to use
        """
        try:
            root = [x for x in self.children if x.action == action].pop(0)
        except:
            self.debugger()
        if kill:
            root.overthrow()  # Delete all irrelevant siblings to free memory
            root.clean_tree()

        # Add to storage
        root.TT[root.hash()] = root
        root.increment(root)
        return root

    def get_node(self, state_hash, draws):
        """
        Can jump to any (explored) state given the state
        """
        if draws:
            return self.counts[state_hash]
        else:
            return self.TT[state_hash]

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

    @staticmethod
    def debugger(current):
        """Modified referee calls this, allows for navigation of search tree
        Can call anywhere in execution"""
        while(1):
            chosen = input(">> Change node (c) literal eval (e) parent (p) print state info (s) quit (q) >> ")
            if chosen not in "cpesq":
                print(">> Invalid, try again.")
            elif chosen == "c":
                try:
                    nodehash = int(input("Specify FULL hash for state >> ").strip())
                    current = current.get_node(nodehash)
                except:
                    print(">> invalid, try again.")
            elif chosen == "p":
                current = current.parent
                print(">> Navigated to parent.")
            elif chosen == "e":
                try:
                    exec(input("Object called current, it is a gamenode >> "))
                except:
                    print(">> invalid, try again.")
            elif chosen == "s":
                current.format()
            else:
                break

    def format(self):
        """
        Defines how to display a state in debugging.
        """
        current.printer(current.state)
        print(f"Depth {current.state['depth']}, colour {current.state['turn']} full_eval {current.fully_evaluated} dead {current.is_dead} expanded {current.is_expanded}\nChildren: ")
        for child in current.children:
            print(f"FULL HASH {child.hash()} - {child.action}",end="")
            if child.action in current.child_evaluations.keys():
                print(f" - {current.child_evaluations[child.action]}")
            else:
                print("")

    @staticmethod
    def printer(state):
        from algorithms.partA.formatting import print_board
        board_dict = {}
        for player in PLAYER_NAMES:
            for i in state[player]:
                board_dict[i] = f"{player}"
        print_board(board_dict)
