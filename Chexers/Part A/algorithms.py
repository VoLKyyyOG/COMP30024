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

# User-defined files
from classes import *
from moves import *
from print_debug import *
from transposition import *

########################## GLOBALS ###########################
INF = float('inf')

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
            self.player = self.get_player() # Identifies which color turn it was
        else: # Initial state
            self.state = self.player = None
            self.depth = 0
        self.game_status = None # For now, is True if search ongoing
        self.possible_actions = None # Will store list of action-tuples
        self.is_expanded = False # Flags expanded nodes for use in Part B
        self.action_made = None # Action that parent made to get here
        self.children = list() # Stores addresses of children

    def create_children(self):
        """Given a list of action tuples, create new children."""
        for action in self.possible_actions:
            new_child = self.new_child()
            new_child.apply_action(action)
            self.children.append(new_child)
        self.is_expanded = True

    def apply_action(self, action):
        """Applies action to passed node, updates attributes.
        NOTE: state is usually the parents', as self still being defined"""
        piece, action_flag, dest = action
        if action_flag != EXIT:
            self.state["pieces"].remove(piece)
            self.state["pieces"].append(dest)
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

    def __str__(self):
        """Defines string format for use in debugging"""
        return f"State: {self.state}\nDepth {self.depth}" \
        + f", Game Status {self.game_status}" \
        + f", Expanded {self.is_expanded}, Action {self.action_made}\n" \
        + f"Actions {self.possible_actions}\nChildren {self.children}"

######################## HEURISTICS ##########################

def jump_heuristic(node):
    """Admissible Heuristic for a relaxed problem that allows jumping
        over empty tiles (still needs empty landing zone)"""
    """ NOTE: MUST UPDATE FOR PART B IF STATE STORAGE CHANGES """

    total = 0
    for piece in node.state["pieces"]:
        # Distance of a piece to its exit (# rows between it and exit)
        # Uses cubic coordinate form to efficiently isolate correct axis
        axis_to_use = PLAYER_CODE[node.player]
        move_distance = MAX_COORDINATE_VAL - Vector.get_cubic(piece)[axis_to_use]

        # Max jumps to get off board; the best case. +1 to account for exit action
        # The ceil() calculates minimum no. jumps to get to exit tile
        total += ceil(move_distance / 2.0) + 1

    return total

    # return sum([ceil((MAX_COORDINATE_VAL - Vector.get_cubic(piece)[PLAYER_CODE[node.player]]) / 2) + 1 for piece in node.state["pieces"]])

########################### IDA* #############################

def create_IDA_root(initial_state):
    """Creates a root IDA_Node for IDA* to work with"""
    root = IDA_Node(None)
    root.state = deepcopy(initial_state)
    root.game_status = IDA_Node.get_status(root)
    root.possible_actions = possible_actions(root.state)
    root.player = initial_state['colour']
    return root

class IDA_Node(Node):
    """IDA* Node definition with inbuilt attributes for heuristic/total cost"""
    COUNT_TOTAL = TRIM_TOTAL = MEMORY_TOTAL = 0

    def __init__(self, parent):
        super().__init__(parent)

        # Additional functionality for IDA*
        # Exit cost = cost to get from here to completion
        # Total cost factors in depth (total_cost = depth + exit_cost)
        self.total_cost = self.exit_cost = 0
        IDA_Node.COUNT_TOTAL += 1
        IDA_Node.MEMORY_TOTAL += getsizeof(self)

    def __str__(self):
        """Appends additional IDA information to standard Node str format"""
        cur_str = super().__str__()
        cur_str += f"\nExit ({self.exit_cost}) + Depth = {self.total_cost}\n"
        return cur_str

    def __lt__(self, other):
        """Allows (node < other_node) behaviour, for use in PQ"""
        return self.total_cost < other.total_cost

    def new_child(self):
        """Overrides child creation call in Node class"""
        return IDA_Node(parent=self)

def IDA(node, exit_h, threshold, new_threshold, debug_flag=False):
    """Implements IDA*, using IDA_node.depth as g(n) and exit_h as h(n)"""
    node.create_children()
    queue = PQ() # Gets item with lowest total_cost

    # Initialize children, with trimming
    for child in node.children:
        """Help me debug this, it's meant to not allow 'inverse actions'"""
        if False and (node.parent is not None) and (Z_hash(node.parent.state) == Z_hash(child.state)):
            # You repeated the last move, do not evaluate!
            # node.children.remove(child) Can't remove while iterating over it or it skips children :(
            IDA_Node.MEMORY_TOTAL -= getsizeof(child)
            IDA_Node.TRIM_TOTAL += 1
            continue
        """IGNORE THIS, THIS IS FOR TRYING TO DO TT
        # Evaluate child and calculate potential children
        if (Z_hash(child.state) in IDA_Node.VISITED_TT):
            # Duplicate - keep the most optimal position
            assert(len(IDA_Node.VISITED_TT[Z_hash(child.state)]) == 1)
            if not (child < IDA_Node.VISITED_TT[Z_hash(child.state)][0]):
                # The currently stored is better - kill it
                print("********************************************")
                node.children.remove(child)
                IDA_Node.MEMORY_TOTAL -= getsizeof(child)
                IDA_Node.TRIM_TOTAL += 1
                del(child)
                continue
        else:
            IDA_Node.VISITED_TT[Z_hash(child.state)].append(child)"""

        # Evaluate heuristics, define possible_actions, append to queue
        child.exit_cost = exit_h(child)
        child.total_cost = child.depth + child.exit_cost
        child.possible_actions = possible_actions(child.state)
        queue.put(child)

    # Expand children, preferring those of least (estimated) total_cost
    while not queue.empty():
        child = queue.get()
        child.create_children()

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
            root = IDA(child, exit_h, threshold, new_threshold)

            if root is not None: # I found a solution below me, echo it upwards
                return root

    # IDA has failed to find anything
    return None

"""Made debug_flag=True for now"""
def IDA_control_loop(initial_state, exit_h=jump_heuristic, max_threshold = 14, debug_flag=True):
    """Runs IDA*. Must use a heuristic that works with Nodes and returns 0 @ goal"""
    """FUTURE GOAL: Allow generated nodes to remain in system memory for other algorithms to exploit!"""

    initial_node = create_IDA_root(initial_state)
    initial_node.total_cost = initial_node.exit_cost = threshold = exit_h(initial_node)
    if debug_flag:
        print(str(initial_node))
        print_board(debug(initial_node.state))

    root = None
    while root is None and threshold < max_threshold:
        new_threshold = [INF] # So that IDA() can manipulate it
        # Perform IDA* down the tree to reach nodes just beyond threshold
        root = IDA(initial_node, exit_h, threshold, new_threshold)
        if root is None: # Update threshold, the goal hasn't been found
            threshold = new_threshold[0]
        if debug_flag:
            print(f"Threshold ({threshold}), new_threshold ({new_threshold[0]})")
    return root
