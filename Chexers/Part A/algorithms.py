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
from sys import getsizeof

########################## GLOBALS ###########################
COUNT_TRIM = 0
COUNT_TOTAL = 0
MEMORY_TOTAL = 0
MOVE = 0
JUMP = 1
EXIT = 2
COUNT_PER_DEPTH = list() # index by depth, e.g. COUNT_PER_DEPTH[5] has total count @ depth 5. Depth 0 is root.
MAX_COORDINATE_VAL = 3 # Point indices range from -3 to 3
INF = float("inf")

###################### NODE BASE CLASS #######################

"""Agent-INDEPENDENT Node abstract class with core information
Call like Node(hash, parent, alpha, beta, gamma, delta)
Most attributes/methods are initialized here, to force us to be consistent
Subclasses e.g. IDA_Node(Node) define and add extra functionality"""
class Node:
    def __init__(self, hashed_state, parent):
        COUNT_TOTAL += 1
        MEMORY_TOTAL += getsizeof(self)
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
    def apply_action(self, piece, action_flag, new_position=None):
        """Applies action to passed node, updates attribute"""
        if action_flag == MOVE or action_flag == JUMP:
            try:
                self.state["pieces"].replace(piece, Vector.add(piece, new_position))
            except:
                print("Error in moving/jumping - coordinate not passed?")
        elif action_flag == EXIT:
                """PART B: Must update exit total flags here"""
                self.remove(piece)
        else:
            print("Action error: not valid action_flag")
            raise ValueError

        # Update hashed_state, game_status, possible_actions
        self.__init__(Z_hash(self.state), self.parent)

    def __get_status(self):
        """PART A: 0 is over, more than 1 is not over
        PART B: 1 W_RED, 2 W_GR, 3 W_BL, 0 NONE, -1 DRAW -2 DUPLICATE for is_over call
        Determines if a win/loss/draw has occurred
        just read it from the state for Part A, try doing it from hash for Part B"""
        return not len(self.state["pieces"])

    def __get_player(self):
        """Retrieves current player.
        PART A: Simple, just get it from data
        PART B: ONLY IMPLEMENT AFTER "DATA" structure FINALISED
        Consider just reading it from the state hash"""
        return self.state["colour"]

    ##################### SUBCLASSES WILL DEFINE ADDITIONAL DATA, FUNCS ETC ######################


################ HEURISTICS FOR PART A #################

def test_heuristic(piece_coords):
    """Admissible Heuristic (range >= 0): Assuming 100\% free jumping, calculates no. actions to win"""

    """ Note: PLAYER_CODE defined in hash.py"""

    # Stores heuristic calculation per piece, will be summed
    piece_eval_stor = list()
    # Use PLAYER_CODE to choose the cubic coordinate to use to evaluate distance below

    for piece in piece_coords:
        # Distance of a piece to its exit (# rows between it and exit)
        axis_to_use = PLAYER_CODE["red"]
        distance = MAX_COORDINATE_VAL - Vector.get_cubic(piece)[axis_to_use]

        # Max jumps to get off board; the best case. +1 to account for exit action
        # The ceil() calculates minimum no. jumps to get to exit tile from distance
        piece_eval_stor.append(ceil(distance / 2.0) + 1)

    return sum(piece_eval_stor)

print(f"Test for red: {test_heuristic([[0,0]])}")

def jump_heuristic(node):
    """Admissible Heuristic (range >= 0): Assuming 100\% free jumping, calculates no. actions to win"""

    """ Note: PLAYER_CODE defined in hash.py"""

    # Stores heuristic calculation per piece, will be summed
    piece_eval_stor = list()
    # Use PLAYER_CODE to choose the cubic coordinate to use to evaluate distance below

    for piece in node.state["pieces"]:
        # Distance of a piece to its exit (# rows between it and exit)
        axis_to_use = PLAYER_CODE[node.get_player()]
        distance = MAX_COORDINATE_VAL - Vector.get_cubic(piece)[axis_to_use]

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
        This must be sub_node independent."""

        # Heuristic cost
        new_node.travel_cost = travel_h(new_node)
        new_node.exit_cost = exit_h(node)
        new_node.total_cost = new_node.travel_cost + new_node.exit_cost

        if new_node.total_cost > threshold:
            # we have expanded another node! Check if it's cheaper than previous
            if new_node.total_cost < newThreshold[0]:
                # Update threshold
                newThreshold[0] = new_node.total_cost
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

def IDA_control_loop(initial_state, travel_h, exit_h, maxThreshold = 60, debug=False):
    """Runs IDA*. Must use two heuristics that work with Nodes. Returns 0 at goal"""
    """FUTURE GOAL: Allow generated nodes to remain in system memory for other algorithms to exploit!"""

    initial_node = IDA_Node(initial_state, None)
    initial_node.total_cost = threshold = exit_h(initial_node)

    root = None
    while not root and threshold < maxThreshold:
        """OPTIMISATION 2: Test the TT to eliminate across-the-branch repetition"""
        newThreshold = [INF] # To allow passing of reference so that IDA() can manipulate it

        # r E c U r S i O n
        root = IDA(initial_node, travel_h, exit_h, threshold, newThreshold)

        if not root:
            threshold = newThreshold[0]
            if debug:
                print(newThreshold[0])

    return root
