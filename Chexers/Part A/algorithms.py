""" Algorithms.py

Implements algorithms for use in game exploration, NOT actual agent logic.

Notes:
- Globals below for analysis.
- Utilise game_status to tell if trimmed (symmetrical flag) --> DONT Explore
- Maybe have a different flag; so that way, one flag = "win/loss/draw", the other is "trim/duplicate" etc,
"""

########################## IMPORTS ###########################
from math import ceil
from sys import getsizeof
from copy import deepcopy
from queue import PriorityQueue as PQ

from classes import *
from moves import *
from print_debug import *
from transposition import *

########################## GLOBALS ###########################

COUNT_PER_DEPTH = list() # index by depth, e.g. COUNT_PER_DEPTH[5] has total count @ depth 5. Depth 0 is root.
MAX_COORDINATE_VAL = 3 # Point indices range from -3 to 3
INF = float("inf")

###################### NODE BASE CLASS #######################

"""Agent-INDEPENDENT Node abstract class with core information
Call this superclass like Node(hash, parent)
Most attributes/methods are initialized here, to force us to be consistent
Subclasses e.g. IDA_Node(Node) define and add extra functionality"""
class Node:

    def __init__(self, parent):
        """Creates new node. For a root node just do Node(), else do Node(parent)
        It will inherit the parent's state - this needs updating with apply_action"""
        self.parent = parent # MUST BE REFERENCE, NOT COPY # Points to parent Node
        if (parent is not None):
            self.state = deepcopy(self.parent.state)
            self.depth = self.parent.depth + 1
            self.player = self.get_player()
        else:
            self.state = self.player = None
            self.depth = 0
        self.game_status = self.possible_actions = None
        # print(f"Test in __init__: {self.game_status}")
        self.is_expanded = False # Allows us to realise, if there are no childen, this is a dead end
        self.action_made = None # The action that the parent made to get to here - is defined in apply_action/create children
        self.children = list() # Could be different, maybe a PQ for weighted choices acc. heuristic

    def __str__(self):
        return f"State: {self.state}\nDepth {self.depth}, Game Status {self.game_status}, Expanded {self.is_expanded}, Action {self.action_made}\n" + \
        f"Actions {self.possible_actions}\nChildren {self.children}"

    def create_children(self, actions):
        """Given a list of action tuples, create children.
         e.g. actions = [(piece, MOVE, new_pos),  ... (piece, EXIT, None) ... (piece, JUMP, new_pos)...]"""
        actions = possible_actions(self.state)
        for action in actions:
            new_child = self.new_child()
            new_child.apply_action(action)
            # Check if a duplicate?
            self.children.append(new_child)
        self.is_expanded = True

    def apply_action(self, action):
        """Applies action to passed node, updates attribute"""
        """NOTE: state is the parent's state!"""
        piece, action_flag, dest = action
        if action_flag == MOVE or action_flag == JUMP:
            try:
                #print(f"{action} ... My pieces: {self.state['pieces']}")
                self.state["pieces"].remove(piece)
                self.state["pieces"].append(dest)
                """PART B: CONSIDER ORDERING & Must evaluate capturing here"""
                self.action_made = action
            except:
                print(f"{action} - Error in moving/jumping - coordinate not passed?")
        elif action_flag == EXIT:
            """PART B: Do NOT evaluate no. exits - this is done via get_status below"""
            self.state["pieces"].remove(piece)
            self.action_made = action
        else:
            print("Action error: not valid action")
            raise ValueError

        # Update game_status, possible_actions (now that state is updated)
        self.game_status = self.get_status()
        self.possible_actions = possible_actions(self.state)

    def get_status(self):
        """PART A: 0 is over, more than 1 is not over
        PART B: 1 W_RED, 2 W_GR, 3 W_BL, 0 NONE, -1 DRAW -2 DUPLICATE for is_over call
        Determines if a win/loss/draw has occurred
        just read it from the state"""
        # print(f"WE MADE IT HERE {len(self.state['pieces']) > 0}")
        return (len(self.state["pieces"]) > 0 if self.state is not None else True)

    def get_player(self):
        """Retrieves current player.
        PART A: Simple, just get it from data
        PART B: ONLY IMPLEMENT AFTER "DATA" structure FINALISED"""
        assert(self.parent is not None)
        return self.parent.state["colour"]

    ##################### SUBCLASSES WILL DEFINE ADDITIONAL DATA, FUNCS ETC ######################

    # Overriden by subclasses
    def new_child(self):
        return Node(parent=self)

    def __lt__(self, other):
        """Defines behaviour for node < other_node for queues"""
        pass

################### HEURISTICS FOR PART A ####################

# Uses coordinate based system
def test_heuristic(piece_coords):
    """Admissible Heuristic (range >= 0): Assuming 100\% free jumping, calculates no. actions to win"""
    """ Note: PLAYER_CODE defined in classes.py"""
    return sum([ceil((MAX_COORDINATE_VAL - Vector.get_cubic(piece)[PLAYER_CODE["red"]]) / 2) + 1 for piece in piece_coords])

# Uses current node passed through
def jump_heuristic(node):
    """Admissible Heuristic (range >= 0): Assuming 100\% free jumping, calculates no. actions to win"""

    """ Note: PLAYER_CODE defined in classes.py"""

    """ NOTE: MUST UPDATE FOR PART B IF STATE STORAGE CHANGES """

    # Stores heuristic calculation per piece, will be summed
    # piece_eval_stor = list()
    # Use PLAYER_CODE to choose the cubic coordinate to use to evaluate distance below

    # for piece in node.state["pieces"]:
    #    # Distance of a piece to its exit (# rows between it and exit)
    #     axis_to_use = PLAYER_CODE[node.player]
    #     distance = MAX_COORDINATE_VAL - Vector.get_cubic(piece)[axis_to_use]
    #
    #    # Max jumps to get off board; the best case. +1 to account for exit action
    #    # The ceil() calculates minimum no. jumps to get to exit tile from distance
    #    piece_eval_stor.append(ceil(distance / 2.0) + 1)
    #
    # return sum(piece_eval_stor)
    #
    """PASSING NODE SHOULD BE DEFAULT PASS FOR FUNCTIONS IMO"""
    return sum([ceil((MAX_COORDINATE_VAL - Vector.get_cubic(piece)[PLAYER_CODE[node.player]]) / 2) + 1 for piece in node.state["pieces"]])

######################### IDA* #########################

def create_IDA_root(initial_state):
    root = IDA_Node(None)
    # print(f"My root is {type(root)} and has properties {dir(root)}")
    root.state = deepcopy(initial_state) # Board state data: piece positions, # exits etc. accessed through here
    root.game_status = Node.get_status(root)
    # print(f"{root.game_status}")
    root.possible_actions = possible_actions(root.state)
    root.depth =  0
    root.player = initial_state['colour']
    return root

class IDA_Node(Node):
    """Call this like IDA_node(parent)
    DOES NOT CALCULATE HEURISTICS AUTOMATICALLY"""
    COUNT_TOTAL = 0
    COUNT_TRIM = 0
    MEMORY_TOTAL = 0
    VISITED_TT = TT()

    def __init__(self, parent):
        super().__init__(parent)

        # Additional functionality for IDA*
        # Exit cost = cost to get from here to completion. Total cost factors in depth
        self.total_cost = self.exit_cost = 0
        IDA_Node.COUNT_TOTAL += 1
        IDA_Node.MEMORY_TOTAL += getsizeof(self)

    def __str__(self):
        cur_str = super().__str__()
        cur_str += f"\nExit ({self.exit_cost}) + Depth = {self.total_cost}\n"
        return cur_str

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def new_child(self):
        return IDA_Node(parent=self)

def IDA(node, exit_h, threshold, new_threshold, debug_flag=False):
    """Implements IDA*, using IDA_node.depth as g(n) and exit_h as h(n)"""
    # print(f"\n********************************\nEvaluating {node.action_made}...")
    node.create_children(node.possible_actions)
    queue = PQ() # Gets item with lowest total_cost

    # Initialize children
    for child in node.children:
        """TO-DO OPTIMISATION 1: Check this child in TT for repetition down the branch
        This must be sub_node independent."""

        # Evaluate child and calculate potential children
        #if (Z_hash(child) in VISITED_SET):
            #if child
        #    pass
        child.exit_cost = exit_h(child)
        child.total_cost = child.depth + child.exit_cost
        child.possible_actions = possible_actions(child.state)
        queue.put(child)

    # Expand children by least cost upwards
    while not queue.empty():
        child = queue.get()
        # print("Best child:\n" + str(child))
        # print("********************************************")
        # print(str(child))
        #print_board(debug(child.state))
        child.create_children(child.possible_actions)

        # print(f"For {child.action_made}, Travel {child.depth} + Exit {child.exit_cost} = {child.total_cost}")

        if child.total_cost > threshold:
            # we have expanded another node! Check if it's cheaper than previous
            if child.total_cost < new_threshold[0]:
                # Update threshold
                new_threshold[0] = child.total_cost
        elif child.total_cost == child.depth:
                # Made it to completion! This is optimal if heuristic admissible
                return child
        else:
            # We haven't hit the fringe yet... r E c U r S i O n down the tree
            root = IDA(child, exit_h, threshold, new_threshold)

            if root is not None: # I found a solution below me, return it upwards
                return root

    # IDA has failed to find anything
    return None

"""Made debug=True for now"""
def IDA_control_loop(initial_state, exit_h=jump_heuristic, max_threshold = 15, debug_flag=True):
    """Runs IDA*. Must use two heuristics that work with Nodes. Returns 0 at goal"""
    """FUTURE GOAL: Allow generated nodes to remain in system memory for other algorithms to exploit!"""

    initial_node = create_IDA_root(initial_state)
    initial_node.total_cost = initial_node.exit_cost = threshold = exit_h(initial_node)
    if debug_flag:
        print(str(initial_node))
        print_board(debug(initial_node.state))

    root = None
    while root is None and threshold < max_threshold:
        """OPTIMISATION 2: Test the TT to eliminate across-the-branch repetition"""
        new_threshold = [INF] # To allow passing of reference so that IDA() can manipulate it
        # r E c U r S i O n
        root = IDA(initial_node, exit_h, threshold, new_threshold)
        if root is None:
            threshold = new_threshold[0]
        print(f"Threshold ({threshold}), new_threshold ({new_threshold[0]})")
    return root
