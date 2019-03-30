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
########################## GLOBALS ###########################

###################### NODE BASE CLASS #######################

class Node:
    """Node superclass with core (initialized) attributes and methods
    Subclasses e.g. IDA_Node(Node) define and add extra functionality"""

    def __init__(self, parent):
        """Creates new node. NOTE: it inherits (not updates) parent state"""
        self.parent = parent # Points to parent node
        self.depth = self.parent.depth + 1 if parent else 0
        self.is_expanded = False # Flags expanded nodes
        self.action_made = None # Action that parent made to get here
        self.state = None # Stores data
        self.children = list() # Stores addresses of children

    def create_children(self):
        """Given a list of action tuples, create new children."""
        if not self.is_expanded:
            for action in possible_actions(self.state):
                new_child = self.new_child()
                new_child.state = apply_action(self.state, action)
                new_child.action_made = action
                self.children.append(new_child)
            self.is_expanded = True

    def game_status(self):
        """Determines if a win/loss/draw has occurred and by whom
        PART A: 0 is over, more than 1 is not over
        PART B: 1 W_RED, 2 W_GR, 3 W_BL, 0 NONE, -1 DRAW, -2 DUPLICATE"""
        return (len(self.state["pieces"]) if self.state else True)

    def player(self):
        """Retrieves current player.
        PART A: Simple, just get it from data
        PART B: ONLY IMPLEMENT AFTER "DATA" structure FINALISED"""
        return self.parent.state["colour"]

    # Subclasses should overrride
    def new_child(self):
        """Creates new Node instance"""
        return Node(parent=self)

    def __hash__(self):
        return Z_hash(self.state)

    def __str__(self):
        """Defines string format for use in debugging"""
        return f"# State: {self.state}\n# Depth {self.depth}" \
        + f", Game Status {self.game_status()}" \
        + f", Expanded {self.is_expanded}, Action {self.action_made}\n# " \
        + f"Actions {possible_actions(self.state)}\n# Children {self.children}"

######################## HEURISTICS ##########################

def apply_heuristics(heuristics, node):
    """Quick abstraction for applying a list of heuristics in a search problem"""
    return sum((f(node) for f in heuristics))

def dijkstra_heuristic(node):
    """Calculates worst-case cost in relaxed problem with free jumping"""
    return sum((dijkstra_board(node.state)[i] for i in node.state['pieces']))

########################### IDA* #############################

class IDA_Node(Node):
    """IDA* Node definition with inbuilt attributes for heuristic/total cost"""
    COUNT_TOTAL = TRIM_TOTAL = 0

    def __init__(self, parent):
        super().__init__(parent)
        self.exit_cost = 0 # Exit cost = cost to get from here to completion
        self.total_cost = 0 # Total cost factors in depth (total_cost = depth + exit_cost)
        IDA_Node.COUNT_TOTAL += 1
        if (IDA_Node.COUNT_TOTAL % 10000 == 0): print ("-", end="")

    def __str__(self):
        """Appends additional IDA information to standard Node str format"""
        return super().__str__() + f"\n # Exit ({self.exit_cost}) + Depth = {self.total_cost}"

    def __lt__(self, other):
        """Allows (node < other_node) behavior, for use in PQ"""
        return self.total_cost < other.total_cost

    def new_child(self):
        """Overrides child creation call in Node class"""
        return IDA_Node(parent=self)

    def update_depth(self, new_depth):
        """Update depths of all predecessors"""
        self.depth = new_depth
        for child in self.children:
            child.update_depth(new_depth + 1)

    @staticmethod
    def create_root(initial_state):
        """Creates a root IDA_Node for IDA* to work with"""
        root = IDA_Node(None)
        root.state = initial_state
        return root

def IDA(node, heuristics, TT, threshold, new_threshold, debug_flag=False):
    """Implements IDA*, using IDA_node.depth as g(n) and exit_h as h(n)"""

    queue = PQ() # Gets item with lowest total_cost

    if not node.is_expanded:
        node.create_children()

        # Initialize children, with trimming
        for child in node.children:
            my_hash = Z_hash(child.state)
            '''if my_hash in TT.keys() and child.depth < TT[my_hash][0].depth:
                IDA_Node.TRIM_TOTAL += 1
                previous = TT[my_hash][0]
                if (child.depth < previous.depth): previous.update_depth(child.depth)
                # Remove from parent's children
                previous.parent.children.remove(previous)
                node.children.append(previous)
                previous.parent = node
                continue
            else:
                TT[my_hash].append(child)'''

            # Evaluate heuristics, append to queue
            child.exit_cost = apply_heuristics(heuristics, child)
            child.total_cost = child.depth + child.exit_cost
            queue.put(child)
    else:
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

def IDA_control_loop(initial_state, heuristics=[dijkstra_heuristic], debug_flag=False):
    """Runs IDA*. Must use a heuristic that works with Nodes and returns goal if found"""

    initial_node = IDA_Node.create_root(initial_state)
    initial_node.total_cost = initial_node.exit_cost = threshold = apply_heuristics(heuristics, initial_node)
    print(f"#\n# Initial valuation: " + ", ".join([f"[{f.__name__}] {f(initial_node)}" for f in heuristics]) + f" + [Depth] {initial_node.depth} = {initial_node.total_cost}")
    TT = defaultdict(list)
    TT[Z_hash(initial_node.state)].append(initial_node)

    root = None
    while root is None:
        new_threshold = [INF] # So that IDA() can manipulate it
        # Perform IDA* down the tree to reach nodes just beyond threshold
        root = IDA(initial_node, heuristics, TT, threshold, new_threshold)
        if root is None: # Update threshold, the goal hasn't been found
            threshold = new_threshold[0]
        if debug_flag:
            print(f"Threshold ({threshold}), new_threshold ({new_threshold[0]}), generated ({IDA_Node.COUNT_TOTAL})")
    return root

#374
