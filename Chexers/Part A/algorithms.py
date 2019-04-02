""" Algorithms.py

Implements algorithms for use in game exploration, NOT actual agent logic.

"""

########################## IMPORTS ###########################

# Standard modules
from queue import PriorityQueue as PQ
from collections import defaultdict

# User-defined files
from moves import *
from classes import *

###################### NODE BASE CLASS #######################

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

    def apply_action(self, action):
        """Applies action to passed node, updates attributes.
        NOTE: state is usually the parents', as self still being defined"""
        piece, action_flag, dest = action
        self.state["pieces"].remove(piece)
        if action_flag != EXIT:
            self.state["pieces"].append(dest)
            self.state["pieces"].sort()
        self.action_made = action

    def create_children(self):
        """Given a list of action tuples, create new children."""
        if not self.is_expanded and not self.is_dead:
            for action in possible_actions(self.state):
                new_child = self.new_child()
                new_child.state = deepcopy(self.state)
                new_child.apply_action(action) # The killer
                self.children.append(new_child)
            self.is_expanded = True

    def game_status(self):
        """Determines if a win/loss/draw has occurred and by whom
        PART A: 0 is over, more than 1 is not over
        PART B: 1 W_RED, 2 W_GR, 3 W_BL, 0 NONE, -1 DRAW, -2 DUPLICATE"""
        return (len(self.state["pieces"]) > 0 if self.state else True)

    def player(self):
        """Retrieves current player.
        PART A: Simple, just get it from data
        PART B: ONLY IMPLEMENT AFTER "DATA" structure FINALISED"""
        return self.parent.state["colour"]

    # Subclasses should overrride
    def new_child(self):
        """Creates new Node instance"""
        return Node(parent=self)

    def __str__(self):
        """Defines string format for use in debugging"""
        return f"# State: {self.state}\n# Depth {self.depth}" \
        + f", Game Status {self.game_status()}" \
        + f", Expanded {self.is_expanded}, Action {self.action_made}\n# " \
        + f"Actions {possible_actions(self.state)}\n# Children {self.children}"

######################## HEURISTICS ##########################

def dijkstra_heuristic(node):
    """Calculates worst-case cost in relaxed problem with free jumping"""
    return sum([dijkstra_board(node.state)[i] for i in node.state['pieces']])

########################### IDA* #############################

class IDA_Node(Node):
    """IDA* Node definition with inbuilt attributes for heuristic/total cost"""
    COUNT_TOTAL = TRIM_TOTAL = 0

    def __init__(self, parent):
        super().__init__(parent)
        self.total_cost = 0 # Total cost factors in depth (total_cost = depth + exit_cost)
        IDA_Node.COUNT_TOTAL += 1

    def __str__(self):
        """Appends additional IDA information to standard Node str format"""
        return super().__str__() + f"\n # Exit {self.total_cost - self.depth} + Depth {self.depth} = {self.total_cost}"

    def __lt__(self, other):
        """Allows (node < other_node) behavior, for use in PQ"""
        return self.total_cost < other.total_cost

    def new_child(self):
        """Overrides child creation call in Node class"""
        return IDA_Node(parent=self)

    @staticmethod
    def create_root(initial_state):
        """Creates a root IDA_Node for IDA* to work with"""
        root = IDA_Node(None)
        root.state = initial_state
        return root

def IDA(node, heuristics, TT, threshold, new_threshold, debug_flag=False):
    """Implements IDA*, using IDA_node.depth as g(n) and sum(heuristics) as h(n)"""

    queue = PQ() # Gets item with lowest total_cost
    if not node.is_expanded and not node.is_dead:
        node.create_children()

        # Initialize children, with trimming
        for child in node.children:
            my_hash = Z_hash(child.state)
            if my_hash in TT.keys():
                IDA_Node.TRIM_TOTAL += 1
                if child.depth >= TT[my_hash].depth:
                    child.is_dead = True
                    continue

            # Evaluate heuristics, append to queue
            child.total_cost = child.depth + dijkstra_heuristic(child)
            queue.put(child)
            TT[my_hash] = child
    elif not node.is_dead:
        for child in node.children:
            queue.put(child)
    # Expand children, preferring those of least (estimated) total_cost
    while not queue.empty():
        child = queue.get()

        if child.total_cost > threshold:
            # we have expanded beyond the fringe! Check if cheaper than previous
            if child.total_cost < new_threshold[0]:
                # Update threshold
                new_threshold[0] = child.total_cost
        elif child.total_cost == child.depth:
                # Made it to completion!
                return child
        else:
            # We haven't hit the fringe yet, recursion down tree
            root = IDA(child, heuristics, TT, threshold, new_threshold)

            if root is not None: # I found a solution below me, echo it upwards
                return root

    # IDA has failed to find anything
    return None

def IDA_control_loop(initial_state, heuristics=dijkstra_heuristic):
    """Runs IDA*. Must use a heuristic that works with Nodes and returns goal if found"""

    initial_node = IDA_Node.create_root(initial_state)
    initial_node.total_cost = threshold = dijkstra_heuristic( initial_node)
    # print(f"#\n# Initial valuation: " + ", ".join([f"[{f.__name__}] {f(initial_node)}" for f in heuristics]) + f" + [Depth] {initial_node.depth} = {initial_node.total_cost}")
    TT = dict()
    TT[Z_hash(initial_node.state)] = initial_node

    root = None
    while root is None:
        new_threshold = [INF] # So that IDA() can manipulate it
        # Perform IDA* down the tree to reach nodes just beyond threshold
        root = IDA(initial_node, heuristics, TT, threshold, new_threshold)
        if root is None: # Update threshold, the goal hasn't been found
            threshold = new_threshold[0]
    return root

#374
