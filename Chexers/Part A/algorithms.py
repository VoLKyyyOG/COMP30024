""" Algorithms.py

Implements algorithms for use in game exploration, NOT actual agent logic.

Notes:
- Globals below for analysis.
- Utilise game_status to tell if trimmed (symmetrical flag) --> DONT Explore
- Maybe have a different flag; so that way, one flag = "win/loss/draw", the other is "trim/duplicate" etc,
"""

########################## IMPORTS ###########################
from math import ceil
from classes import *

########################## GLOBALS ###########################
COUNT_TRIM = 0
COUNT_TOTAL = 0
COUNT_PER_DEPTH = list() # index by depth, e.g. COUNT_PER_DEPTH[5] has total count @ depth 5. Depth 0 is root.
MAX_COORDINTE_VAL = 3 # Point indices range from -3 to 3
INF = float("inf")

###################### NODE BASE CLASS #######################

"""Agent-INDEPENDENT Node abstract class with core information
Call like Node(hash, parent, alpha, beta, gamma, delta)
Most attributes/methods are initialized here, to force us to be consistent
Subclasses e.g. IDA_Node(Node) define and add extra functionality"""
class Node:
    def __init__(self, hashed_state, parent):
        COUNT_TOTAL += 1
        self.hashed_state = hashed_state
        self.depth = self.parent.depth + 1
        self.is_expanded = False # Allows us to realise, if there are no childen, this is a dead end
        self.state = hashed_state.data() # Board state data: piece positions, # exits etc. accessed through here
        self.player = self.__get_player() # Flag for which player you are
        self.game_status = self.__get_status(self)
        self.children = list() # Could be different, maybe a PQ for weighted choices acc. heuristic
        self.parent = parent # MUST BE REFERENCE, NOT COPY # Points to parent Node
        self.possible_actions = possible_actions(self.state)

    # FINALISE ACTIONS FIRST
    def create_children(self, actions):
        """Given a chosen action(s), create children"""
        for action in actions:
            new_child = Node(hashed_state = self.hashed_state, parent = self)
            new_child.apply_action(action)
            # Check if a duplicate?
            self.children.append(new_child)
        self.is_expanded = True

    ######################### TO DEFINE ############################
    def apply_action(self, action):
        """Applies action to passed node, updates attributes"""
        pass

    def __get_status(self):
        """1 W_RED, 2 W_GR, 3 W_BL, 0 NONE, -1 DRAW -2 DUPLICATE for is_over call
        Determines if a win/loss/draw has occurred
        just read it from the state hash"""
        pass

    def __get_player(self):
        """Retrieves current player. ONLY IMPLEMENT AFTER "DATA" structure FINALISED
        Consider just reading it from the state hash"""
        pass

    ##################### SUBCLASSES WILL DEFINE ADDITIONAL DATA, FUNCS ETC ######################


################ HEURISTICS FOR PART A #################

def jump_manhattan(node):
    """Admissible Heuristic (range >= 0): Assuming 100\% free jumping, calculates no. actions to win"""

    """ Note: PLAYER_CODE defined in hash.py"""

    # Stores heuristic calculation per piece, will be summed
    piece_eval_stor = list()
    # Use PLAYER_CODE to choose the cubic coordinate to use to evaluate distance below

    for piece in node.state["pieces"]:
        # Distance of a piece to its exit (# rows between it and exit)
        axis_to_use = PLAYER_CODE[node.get_player()]
        distance = Vector.get_cubic(piece)[axis_to_use] - MAX_COORDINTE_VAL

        # Max jumps to get off board; the best case. +1 to account for exit action
        # The ceil() calculates minimum no. jumps to get to exit tile from distance
        piece_eval_stor.append(ceil(distance / 2.0) + 1)

    return sum(piece_eval_list)

######################### IDA* #########################

class IDA_Node(Node):
    """Call this like IDA_node(state, parent)"""
    def __init__(self, *args):
        try:
            # Define properties that a Node already has
            self.super().__init__(self, args[0], args[1])
        except:
            print("Uh oh, someone *cough-cough Callum* screwed up here...\n")
            raise ValueError
        # Additional functionality for IDA*
        self.travel_cost = 0   # Travel cost = cost to have gotten to this state
        self.exit_cost = 0     # Exit cost = cost to get from here to completion
        self.total_cost = self.travel_cost + self.exit_cost

def IDA(node, travel_h, exit_h, threshold, new_threshold):
    """Implements IDA*"""
    for action in node.possible_actions:

        # Create a child following that action
        # NOTE: apply_action has side-effect of self.travel_cost += 1
        new_node = IDA_Node(node.state, node)
        new_node.apply_action(action)

        """TO-DO OPTIMISATION 1: Check this child in TT for repetition down the branch
        This must be sub_node independent.
        I (Callum) would realllllly like to do this"""

        # Heuristic cost
        new_node.travel_cost = travel_h(new_node)
        new_node.exit_cost = exit_h(node)
        new_node.total_cost = new_node.travel_cost + new_node.exit_cost

        if new node.heuristic > threshold:
            # we have expanded another node! Check if it's cheaper than previous
            if new_node.heuristic < newThreshold[0]:
                # Update threshold
                newThreshold[0] = new_node.heuristic
        elif cost == 0:
                # Made it to completion! This is optimal if heuristic admissible
                return new_node
        else:
            # We haven't hit the fringe yet... DFS
            # r E c U r S i O n down the tree
            root = IDA(new_node, threshold, newThreshold)

            if root: # I found a solution below me, return it upwards
                return root

    # IDA has failed to find anything
    return None

def IDA_control_loop(initial_state, travel_h, exit_h, debug=False):
    """Runs IDA*. Must use two heuristics that work with Nodes. Returns 0 at goal"""
    """FUTURE GOAL: Allow generated nodes to remain in system memory for other algorithms to exploit!"""

    initial_node = IDA_Node(initial_state, None)
    initial_node.total_cost = threshold = exit_h(initial_node)

    root = None
    while not root:
        """OPTIMISATION 2: Test the TT to eliminate across-the-branch repetition"""
        newThreshold = [INF] # To allow passing of reference so that IDA() can manipulate it

        # r E c U r S i O n
        root = IDA(initial_node, travel_h, exit_h, threshold, newThreshold)

        if not root:
            threshold = newThreshold[0]
            if debug:
                print(newThreshold[0])

    return root
