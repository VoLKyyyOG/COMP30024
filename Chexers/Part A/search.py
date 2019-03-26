"""
################################################################################
##########    COMP30024 Artificial Intelligence, Semester 1 2019    ############
##########          Solution to Project Part A: Searching           ############
##########       Akira Wang (######), Callum Holmes (899251)        ############
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

def main():
    DEBUG_FLAG = False # FOR DEBUGGING

    # Read argv input for initial state
    with open(argv[1]) as file:
        data = load(file)
        print('# Data input:', data)

    # Print current state
    print_board(debug(data), debug=True)

    # Begin Timer
    start = time.time()

    # Implementing IDA*
    optimal_solution = IDA_control_loop(data, debug_flag=DEBUG_FLAG)

    # End Timer
    end = time.time()

    print(f"(Real) Time Elapsed {end - start:.6f}s")

    print(f'# {BANNER}# {IDA_Node.COUNT_TOTAL} generated, {IDA_Node.TRIM_TOTAL} trimmed and ~{IDA_Node.MEMORY_TOTAL} bytes used.')
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

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()