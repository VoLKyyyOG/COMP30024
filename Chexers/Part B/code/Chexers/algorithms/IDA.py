class IDA_Node(Node):
    """IDA* Node definition with inbuilt attributes for heuristic/total cost"""

    def __init__(self, parent):
        super().__init__(parent)
        self.total_cost = 0 # Total cost factors in depth (total_cost = depth + exit_cost)

    def __lt__(self, other):
        """Allows (node < other_node) behavior, for use in PQ"""
        return self.total_cost < other.total_cost

def IDA(node, heuristic, TT, threshold, new_threshold, debug_flag=False):
    """Implements IDA*, using IDA_node.depth as g(n) and sum(heuristics) as h(n)"""

    queue = PQ() # Gets item with lowest total_cost
    if not node.is_expanded and not node.is_dead:
        # Initialize children, with trimming
        for child in node.children:
            my_hash = encode(child.state)
            if my_hash in TT.keys():
                if child.depth >= TT[my_hash].depth and child != TT[my_hash]:
                    child.is_dead = True
                    continue

            # Evaluate heuristics, append to queue
            child.total_cost = child.depth + heuristic(child.state)
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
            root = IDA(child, heuristic, TT, threshold, new_threshold)

            if root is not None: # I found a solution below me, echo it upwards
                return root

    # IDA has failed to find anything
    return None

def IDA_control_loop(initial_state, heuristic):
    """Runs IDA*. Must use a heuristic that works with Nodes and returns goal if found"""

    initial_node = IDA_Node.create_root(initial_state)
    initial_node.total_cost = threshold = heuristic(initial_state)
    TT = dict() # Transposition Table
    TT[Z_hash(initial_node.state)] = initial_node

    root = None
    while root is None:
        new_threshold = [INF] # So that IDA() can manipulate it
        # Perform IDA* down the tree to reach nodes just beyond threshold
        root = IDA(initial_node, heuristic, TT, threshold, new_threshold)
        if root is None: # Update threshold, the goal hasn't been found
            threshold = new_threshold[0]
    return root
