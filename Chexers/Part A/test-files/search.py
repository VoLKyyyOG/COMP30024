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

    data = convert_to_tuples(data)

    # Print current state


    # Implementing IDA*
    chosen_heuristics = [dijkstra_heuristic]
    optimal_solution = IDA_control_loop(data, heuristics=chosen_heuristics, debug_flag=False)

    # END TIME (FOUND SOLUTION)
    end = time.time()
    time_taken = end - start

    print(f"{time_taken:.6f}")



# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
