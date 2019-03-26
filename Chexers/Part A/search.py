"""
################################################################################
##########    COMP30024 Artificial Intelligence, Semester 1 2019    ############
##########          Solution to Project Part A: Searching           ############
##########       Akira Wang (), Callum Holmes (899251)        ############
##########                       Team: _blank_                      ############
################################################################################
"""

########################## IMPORTS ###########################
# Standard modules
from json import load
from sys import argv
import time

# User-defined files
from print_debug import *
from algorithms import *

########################## GLOBALS ###########################
BANNER = '*' * 60 + '\n'

######################### FUNCTIONS ##########################

# BEGIN TIME (PROGRAM EXECUTION)
start = time.time()

def main():
    DEBUG_FLAG = False # FOR DEBUGGING

    # Read argv input for initial state
    with open(argv[1]) as file:
        data = load(file)
        print('# Data input:', data)

    # Print current state
    print(f"# Check hash accuracy: {Z_data(Z_hash(data))}")
    print_board(debug(data), debug=False)

    # Implementing IDA*
    optimal_solution = IDA_control_loop(data, debug_flag=DEBUG_FLAG)

    # END TIME (FOUND SOLUTION)
    end = time.time()
    time_taken = end - start

    print(f'# {BANNER}# {IDA_Node.COUNT_TOTAL} generated, {IDA_Node.TRIM_TOTAL} trimmed and ~{IDA_Node.MEMORY_TOTAL} bytes used.')
    print(f'# Depth analysis: ')
    print(f'# Depth: ' + " | ".join([f"{x:7d}" for x in range(10)]))
    print(f'# Count: ' + " | ".join(map(lambda x: f"{x:7d}", IDA_Node.COUNT_BY_DEPTH[:10])))
    print('# ' + '-' * 110 +  f'\n# Depth: ' + " | ".join([f"{x:7d}" for x in range(10, 20)]))
    print(f'# Count: ' + " | ".join(map(lambda x: f"{x:7d}", IDA_Node.COUNT_BY_DEPTH[10:])))

    if (optimal_solution is not None):
        print(f'# A solution was found! Cost: {optimal_solution.depth}\n# Sequence of moves: ')
        path = list()
        node_temp = optimal_solution
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
    else:
        print(f'# ERROR: No solution found at this depth')

    print(f"#\n#\n# (Real) Time Elapsed {time_taken:.6f}")
    if (time_taken < 30):
        PASSED = True
    else:
        print("# F to Pay Respects.")


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
