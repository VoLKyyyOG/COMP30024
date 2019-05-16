"""
:filename: IDA.py
:summary: Complete refactoring of Part A code.
:authors: Akira Wang (913391), Callum Holmes (899251)
"""

########################### IMPORTS ##########################

# Standard modules
from queue import PriorityQueue as PQ
from collections import defaultdict
from math import inf
from copy import deepcopy

# User-defined functions
from mechanics import Z_hash
from moves import add
from algorithms.PARTA.search import printing, original_search

# Global Imports
from moves import GOALS, POSSIBLE_DIRECTIONS, VALID_COORDINATES
from mechanics import (
    PLAYER_HASH, N_PLAYERS, CODE_LEN, NUM_HEXES, MAX_EXITS, MAX_COORDINATE_VAL
)

# action_flags for use in action tuples
MOVE, JUMP, EXIT = 0, 1, 2

#################### MOVEMENT FUNCTIONS #####################

def possible_actions(state, debug_flag = False):
    """Possible actions from current location"""
    result = list()

    # if a piece can exit, great! Do that immediately for Part A
    possible_exit = [i for i in state["pieces"] if i in GOALS[state["colour"]]]
    if possible_exit:
        return [(possible_exit[0], EXIT, None)]

    for piece in state["pieces"]:
        result.extend([(piece, MOVE, dest) for dest in move(piece, state)])
        result.extend([(piece, JUMP, dest) for dest in jump(piece, state)])

    return result

def move(coordinate, state, relaxed=False):
    """Finds possible move actions given a coordinate"""
    # Non-movable pieces on board
    if relaxed:
        occupied = state["blocks"]
    else:
        occupied = state["blocks"] + state["pieces"]

    possible_moves = list()

    for direction in POSSIBLE_DIRECTIONS:
        adjacent_hex = add(coordinate, direction)

        if adjacent_hex in VALID_COORDINATES: # Then it's not off-board
            if adjacent_hex not in occupied: # Then it's free for the taking
                possible_moves.append(adjacent_hex)

    return sorted(possible_moves)

def jump(coordinate, state, relaxed=False):
    """Finds possible jump actions given a coordinate"""
    if relaxed:
        occupied = state["blocks"]
    else:
        occupied = state["blocks"] + state["pieces"]

    possible_jumps = list()

    for direction in POSSIBLE_DIRECTIONS:
        adjacent_hex = add(coordinate, direction)
        target_hex = add(adjacent_hex, direction)

        if relaxed or adjacent_hex in occupied: # Then you can jump over it
            if target_hex in VALID_COORDINATES: # Then not off-board
                if target_hex not in occupied: # Then actual place to land
                    possible_jumps.append(target_hex)

    return sorted(possible_jumps)

# Determines if exit action possible
def exit_action(coordinate, state):
    return coordinate in GOALS[state["colour"]]

"""ADAPTED FROM https://www.python-course.eu/python3_memoization.php"""
def memoize(method):
    """Caches result of a function to prevent recalculation under same input"""
    memo = []
    def helper(*args, **kwargs):
        if not len(memo):
            memo.append(method(*args, *kwargs))
        return memo[0]
    return helper

@memoize
def dijkstra_board(state):
    """Evaluates minimum cost to exit for each non-block position"""
    valid_goals = set(GOALS[state['colour']]).difference(set(state['blocks']))

    visited = set() # Flags if visited or not
    cost = {x:inf for x in VALID_COORDINATES} # Stores costs
    cost.update({x:1 for x in valid_goals}) # Sets goals cost
    queue = PQ()

    # Add exits to queue to get it started
    for goal in valid_goals:
        queue.put((cost[goal], goal))

    # Loop over queue (dijsktra)
    while not queue.empty():
        curr_cost, curr = queue.get()
        if curr not in visited:
            visited.add(curr)
            poss_neighbours = set(move(curr, state, True)).union(set(jump(curr, state, True)))
            for new in poss_neighbours:
                est_cost = curr_cost + 1
                if est_cost < cost[new]: # Better path than previous
                    cost[new] = est_cost
                    return cost
                queue.put((cost[new], new))

def Z_hash(data):
    """Hash of the form
        0b(turn)(red_exits)(green_exits)(blue_exits)(37 hex state flags....)
    """
    hashed = 0

    # Append turn player
    hashed = hashed | PLAYER_HASH[data["colour"]]

    # Encode coordinates: First, make space
    hashed = hashed << NUM_HEXES * CODE_LEN

    # ith pair of 2-bits = ith location in VALID_COORDINATES
    for piece in data["blocks"]:
        hashed = hashed ^ (0b10 << CODE_LEN * VALID_COORDINATES.index(piece))
    for piece in data["pieces"]:
        hashed = hashed ^ (0b01 << CODE_LEN * VALID_COORDINATES.index(piece))
    return hashed

###################### NODE BASE CLASS #######################

class IDA_Node:
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
        self.total_cost = 0 # Total cost factors in depth (total_cost = depth + exit_cost)

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

    def __lt__(self, other):
        """Allows (node < other_node) behavior, for use in PQ"""
        return self.total_cost < other.total_cost

    def game_status(self):
        """Determines if a win/loss/draw has occurred and by whom"""
        return (len(self.state["pieces"]) > 0 if self.state else True)

    def player(self):
        """Retrieves current player"""
        return self.parent.state["colour"]

    # Subclasses should overrride
    def new_child(self):
        """Creates new Node instance"""
        return IDA_Node(parent=self)

    @staticmethod
    def create_root(initial_state):
        """Creates a root IDA_Node for IDA* to work with"""
        root = IDA_Node(None)
        root.state = initial_state
        return root

######################## HEURISTIC ##########################

def dijkstra_heuristic(node):
    """Calculates worst-case cost in relaxed problem with free jumping"""
    return sum([dijkstra_board(node.state)[i] for i in node.state['pieces']])

########################### IDA* #############################

def IDA(node, TT, threshold, new_threshold, debug_flag=False):
    """Implements IDA*, using IDA_node.depth as g(n) and sum(heuristics) as h(n)"""

    queue = PQ() # Gets item with lowest total_cost
    if not node.is_expanded and not node.is_dead:
        node.create_children()

        # Initialize children, with trimming
        for child in node.children:
            my_hash = Z_hash(child.state)
            if my_hash in TT.keys():
                if child.depth >= TT[my_hash].depth and child != TT[my_hash]:
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
            root = IDA(child, TT, threshold, new_threshold)

            if root is not None: # I found a solution below me, echo it upwards
                return root

    # IDA has failed to find anything
    return None

def IDA_control_loop(initial_state):
    """Runs IDA*. Must use a heuristic that works with Nodes and returns goal if found"""

    initial_node = IDA_Node.create_root(initial_state)
    initial_node.total_cost = threshold = dijkstra_heuristic(initial_node)
    TT = dict() # Transposition Table
    TT[Z_hash(initial_node.state)] = initial_node

    root = None
    while root is None:
        new_threshold = [inf] # So that IDA() can manipulate it
        # Perform IDA* down the tree to reach nodes just beyond threshold
        root = IDA(initial_node, TT, threshold, new_threshold)
        if root is None: # Update threshold, the goal hasn't been found
            threshold = new_threshold[0]
    return root

########################### MAIN #############################

def part_A_search(data):
    """
    Performs the search algorithm used in Part A
    """
    #print(f"\n\n\n\n{data}\n\n\n\n")
    # Perform search and return node of solution state
    #optimal_solution = IDA_control_loop(data)
    #print("\n\nALTERED: ")
    #printing(optimal_solution)

    #print("\n\nORIGINAL: ")
    optimal_solution = original_search(data)

    if (optimal_solution is not None):
        path = list()
        node_temp = optimal_solution

        # Re-assemble path taken
        while (node_temp is not None):
            path.append(node_temp)
            node_temp = node_temp.parent

        return path[::-1]
