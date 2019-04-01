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
from classes import *

########################## GLOBALS ###########################
BANNER = '*' * 60 + '\n'

######################### FUNCTIONS ##########################

# BEGIN TIME (PROGRAM EXECUTION)
start = time.time()

def main():
    DEBUG_FLAG = True # FOR DEBUGGING

    # Read argv input for initial state
    with open(argv[1]) as file:
        data = load(file)
        print('# Data input:', data)

    data = convert_to_tuples(data)

    # Print current state
    print_board(debug(data), debug=False)
    print_board(dijkstra_board(data), debug=False)

    # Implementing IDA*
    chosen_heuristics = [dijkstra_heuristic]
    optimal_solution = IDA_control_loop(data, heuristics=chosen_heuristics, debug_flag=False)

    # END TIME (FOUND SOLUTION)
    end = time.time()
    time_taken = end - start

    timing_info(time_taken, TIME_LOG, COUNT_LOG)

    print(f'# {BANNER}# {argv[1]} - {IDA_Node.COUNT_TOTAL} generated, {IDA_Node.TRIM_TOTAL} ({100*IDA_Node.TRIM_TOTAL / IDA_Node.COUNT_TOTAL:.2f}%) trimmed.')

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

    print(f"#\n# (Real) Time Elapsed {time_taken:.4f} seconds")
    if (time_taken < 30):
        PASSED = True
    else:
        print("# F to Pay Respects.")
# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
