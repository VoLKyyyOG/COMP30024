"""
################################################################################
##########    COMP30024 Artificial Intelligence, Semester 1 2019    ############
##########          Solution to Project Part A: Searching           ############
##########       Akira Wang (913391), Callum Holmes (899251)        ############
##########                       Team: _blank_                      ############
################################################################################
"""

########################## IMPORTS ###########################
# Standard modules
from json import load
from sys import argv

# User-defined files
from print_debug import *
from algorithms import *
from classes import *

########################## GLOBALS ###########################
BANNER = '*' * 60 + '\n'

######################### FUNCTIONS ##########################

def main():
    # Read argv input for initial state
    with open(argv[1]) as file:
        data = load(file)

    data = convert_to_tuples(data)
    import time
    start = time.time()
    # Implementing IDA*
    print("# Prepare for amazingness")
    optimal_solution = IDA_control_loop(data, dijkstra_heuristic)
    end = time.time()

    branching = get_data(optimal_solution, optimal_solution.depth)[1:-1]

    # Compute average
    totals = [sum(data) for data in branching]
    zero_counts = list(map(lambda x: x[0], branching))
    avg_zeroes = sum([i*val / sum(zero_counts) for i, val in enumerate(zero_counts)])
    avgs = [sum([i*depth[i] / float(max(sum(depth[1:]), 0.00001)) for i in range(1, len(depth))]) for depth in branching]
    print(f"# Average depth (ignores root, solution): {avg_zeroes:.1f}\n# Average branching (ignores root, solution): {sum(avgs) / len(avgs):.2f}")

    # print(f"# Time elapsed: {(end-start)}s")
    # print(f'# {argv[1]} - {IDA_Node.COUNT_TOTAL} generated, {IDA_Node.TRIM_TOTAL} ({100*IDA_Node.TRIM_TOTAL / IDA_Node.COUNT_TOTAL:.2f}%) trimmed.')

    if (optimal_solution is not None):
        print(f'# A solution was found! {IDA_Node.COUNT_TOTAL} generated. Cost: {optimal_solution.depth}\n# Sequence of moves:')
        path = list()
        node_temp = optimal_solution

        # Re-assemble path taken
        while (node_temp is not None):
            path.append(node_temp)
            node_temp = node_temp.parent

        for move in path[::-1]:
            if (move.action_made is not None):
                piece, action, dest = move.action_made
                if (action == MOVE):
                    print(f'MOVE from {piece} to {dest}.')
                elif (action == JUMP):
                    print(f'JUMP from {piece} to {dest}.')
                elif (action == EXIT):
                    print(f'EXIT from {piece}.')
        print(pikawin)
    else:
        print(f'# ERROR: No solution found at this depth')
# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
