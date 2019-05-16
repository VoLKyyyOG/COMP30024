"""
:filename: IDA.py
:summary: Complete refactoring of Part A code.
:authors: Akira Wang (913391), Callum Holmes (899251)
"""

########################### IMPORTS ##########################

# User-defined functions
from algorithms.PARTA.search import printing, original_search

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
