""" Algorithms.py

Implements algorithms for use in game exploration, NOT actual agent logic.

Notes:
- Utilise game_status to tell if trimmed (symmetrical flag) --> DONT Explore
- Maybe have a different flag; so that way, one flag = "win/loss/draw", the other is "trim/duplicate" etc

"""

########################## IMPORTS ###########################

# Standard modules
from math import ceil
from sys import getsizeof
from copy import deepcopy
from queue import PriorityQueue as PQ
from collections import defaultdict

# User-defined files
from print_debug import *
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
        if (parent is not None):
            self.state = deepcopy(self.parent.state) # Stores data
            self.depth = self.parent.depth + 1 # No. actions taken so far
        else: # Initial state
            self.state = None
            self.depth = 0
        self.game_status = None # For now, is True if search ongoing
        self.possible_actions = None # Will store list of action-tuples
        self.is_expanded = False # Flags expanded nodes for use in Part B
        self.action_made = None # Action that parent made to get here
        self.children = list() # Stores addresses of children

    @trackit
    def create_children(self):
        if self.is_expanded:
            try:
                assert len(self.children) == len(self.possible_actions)
            except AssertionError:
                print(f"Children: {[i.action_made for i in self.children]}")
                print(f"Actions: {self.possible_actions}")
        """Given a list of action tuples, create new children."""
        for action in self.possible_actions:
            new_child = self.new_child()
            new_child.apply_action(action)
            self.children.append(new_child)
        self.is_expanded = True

    @trackit
    def apply_action(self, action):
        """Applies action to passed node, updates attributes.
        NOTE: state is usually the parents', as self still being defined"""
        assert not self.is_expanded
        piece, action_flag, dest = action
        if action_flag != EXIT:
            self.state["pieces"].remove(piece)
            self.state["pieces"].append(dest)
            self.state["pieces"].sort()
            """PART B: CONSIDER ORDERING & Must evaluate capturing here"""
            self.action_made = action
        elif action_flag == EXIT:
            """PART B: Do NOT evaluate no. exits - this is done via get_status below"""
            self.state["pieces"].remove(piece)
            self.action_made = action

        # Update game_status, possible_actions (now that state is updated)
        self.game_status = self.get_status()
        self.possible_actions = possible_actions(self.state)

    def get_status(self):
        """Determines if a win/loss/draw has occurred and by whom
        PART A: 0 is over, more than 1 is not over
        PART B: 1 W_RED, 2 W_GR, 3 W_BL, 0 NONE, -1 DRAW, -2 DUPLICATE"""
        return (len(self.state["pieces"]) > 0 if self.state is not None else True)

    def get_player(self):
        """Retrieves current player.
        PART A: Simple, just get it from data
        PART B: ONLY IMPLEMENT AFTER "DATA" structure FINALISED"""
        assert(self.parent is not None)
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
        + f", Game Status {self.game_status}" \
        + f", Expanded {self.is_expanded}, Action {self.action_made}\n# " \
        + f"Actions {self.possible_actions}\n# Children {self.children}"

######################## HEURISTICS ##########################

def apply_heuristics(heuristics, node):
    """Quick abstraction for applying a list of heuristics in a search problem"""
    return sum([f(node) for f in heuristics])

@trackit
def dijkstra_heuristic(node):
    """Calculates worst-case cost in relaxed problem with free jumping"""
    return sum([dijkstra_board(node.state)[i] for i in node.state['pieces']])

########################### IDA* #############################

class IDA_Node(Node):
    """IDA* Node definition with inbuilt attributes for heuristic/total cost"""
    COUNT_TOTAL = TRIM_TOTAL = MEMORY_TOTAL = F_SIDE = 0
    COUNT_BY_DEPTH = [0] * 20

    def __init__(self, parent):
        super().__init__(parent)

        # Additional functionality for IDA*
        # Exit cost = cost to get from here to completion
        # Total cost factors in depth (total_cost = depth + exit_cost)
        self.total_cost = 0
        IDA_Node.COUNT_TOTAL += 1
        IDA_Node.MEMORY_TOTAL += getsizeof(self)
        #IDA_Node.COUNT_BY_DEPTH[self.depth] += 1

    def __str__(self):
        """Appends additional IDA information to standard Node str format"""
        cur_str = super().__str__()
        cur_str += f"\n # Exit ({self.total_cost - self.depth}) + Depth = {self.total_cost}"
        return cur_str

    def __lt__(self, other):
        """Allows (node < other_node) behavior, for use in PQ"""
        return self.total_cost < other.total_cost

    @trackit
    def new_child(self):
        """Overrides child creation call in Node class"""
        return IDA_Node(parent=self)

    @trackit
    def kill_tree(self):
        # Kill subtrees
        for child in self.children[::-1]:
            kill_tree(child)
        # Remove node from parent's collections
        if self.parent:
            self.parent.children.remove(self)
        # Kill this
        IDA_Node.TRIM_TOTAL += 1
        del(self)

    @staticmethod
    def create_root(initial_state):
        """Creates a root IDA_Node for IDA* to work with"""
        root = IDA_Node(None)
        root.state = deepcopy(initial_state)
        root.game_status = IDA_Node.get_status(root)
        root.possible_actions = possible_actions(root.state)
        return root

def IDA(node, heuristics, TT, threshold, new_threshold, debug_flag=False):
    """Implements IDA*, using IDA_node.depth as g(n) and exit_h as h(n)"""

    queue = PQ() # Gets item with lowest total_cost

    if not node.is_expanded:
        node.create_children()

        # Initialize children, with trimming
        for child in node.children:
            #assert(hash(child) == Z_hash(child.state))
            my_hash = Z_hash(child.state)#Z_hash(child.state)
            if my_hash in TT.keys():
                if child.depth < TT[my_hash][0].depth:
                    #USE THIS TO CHECK HASHING: assert(Z_hash(child.state) == Z_hash(TT[my_hash][0].state))
                    # Kill previous NEEDS DEBUGGING
                    #TT[my_hash][0].kill_tree()
                    TT[my_hash] = [child]
                else:
                    IDA_Node.TRIM_TOTAL += 1
                    continue
            else:
                TT[my_hash].append(child)

            # Evaluate heuristics, define possible_actions, append to queue
            child.total_cost = child.depth + apply_heuristics(heuristics, child)
            child.possible_actions = possible_actions(child.state)
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

def IDA_control_loop(initial_state, heuristics=[dijkstra_heuristic], max_threshold = 35, debug_flag=True):
    """Runs IDA*. Must use a heuristic that works with Nodes and returns goal if found"""
    """FUTURE GOAL: Allow generated nodes to remain in system memory for other algorithms to exploit!"""

    initial_node = IDA_Node.create_root(initial_state)
    initial_node.total_cost = threshold = apply_heuristics(heuristics, initial_node)
    print(f"#\n# Initial valuation: " + ", ".join([f"[{f.__name__}] {f(initial_node)}" for f in heuristics]) + f" + [Depth] {initial_node.depth} = {initial_node.total_cost}")
    TT = defaultdict(list)
    TT[Z_hash(initial_node.state)].append(initial_node)

    root = None
    while root is None and threshold < max_threshold:
        new_threshold = [INF] # So that IDA() can manipulate it
        # Perform IDA* down the tree to reach nodes just beyond threshold
        root = IDA(initial_node, heuristics, TT, threshold, new_threshold)
        if root is None: # Update threshold, the goal hasn't been found
            threshold = new_threshold[0]
        if debug_flag:
            print(f"Threshold ({threshold}), new_threshold ({new_threshold[0]}), generated ({IDA_Node.COUNT_TOTAL})")
    return root
