""" Experimentation.py

"""

from sys import argv
import json
from moves import *
from classes import *
from queue import Queue

def optimal_paths(state, cost):
    """Given relaxed costs, infers all optimal paths from pieces to exit"""
    optimal_neighbours = defaultdict(list)
    queue = Queue()
    for piece in state['pieces']:
        queue.put(piece)
    while not queue.empty():
        new = queue.get()
        for neighbour in set(move(new, state, True)).union(set(jump(new, state, True))):
            if cost[neighbour] < cost[new]:
                optimal_neighbours[new].append(neighbour)
                queue.put(neighbour)
        # All optimal neighbours computed
    return optimal_neighbours

if __name__ == "__main__":
    with open(argv[1]) as file:
        data = load(file)

    data = convert_to_tuples(data)
    dijk = dijkstra_board(data)
    print_board(debug(data))
    print_board(dijk)
    print optimal_paths(data, dijk)
