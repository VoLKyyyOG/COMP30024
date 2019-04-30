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
from .algorithms import *

######################### FUNCTIONS ##########################

def part_A_search(data):

    optimal_solution = IDA_control_loop(data, dijkstra_heuristic)

    if (optimal_solution is not None):
        path = list()
        node_temp = optimal_solution

        # Re-assemble path taken
        while (node_temp is not None):
            path.append(node_temp)
            node_temp = node_temp.parent

        return (path[::-1], optimal_solution.depth)