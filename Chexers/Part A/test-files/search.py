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
from algorithms import *
from classes import *
from print_debug import *

########################## GLOBALS ###########################
BANNER = '*' * 60 + '\n'

######################### FUNCTIONS ##########################

def main():
    # Read argv input for initial state
    with open(argv[1]) as file:
        data = load(file)

    data = convert_to_tuples(data)
    # Implementing IDA*
    optimal_solution = IDA_control_loop(data, dijkstra_heuristic)
    
    print(f'{IDA_Node.COUNT_TOTAL} {optimal_solution.depth}')

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
