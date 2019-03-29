""" algorithm.py

Implements DFS for a given problem.

"""

SOLVED, UNSOLVED, NO_SOLUTION = 1, 0, -1
GAME_STATES = [NO_SOLUTION, UNSOLVED, SOLVED]
STR_GAME_STATES = ["No solution", "Unsolved", "Solved"]
RESULT_STR = {key:string for string, key in zip(STR_GAME_STATES, GAME_STATES)}

def DFS(root, TT, depth, debug = False):
    """performs DFS in subtree, else evaluates"""
    if (hash(root) in TT):
        return UNSOLVED

    TT.add(hash(root))

    # Identify children
    if root.evaluate():
        print(f"Solution identified!\n{root}")
        return SOLVED
    elif (depth == 0):
        return UNSOLVED
    else:
        curr = NO_SOLUTION
        for child in root.get_children(debug):
            if (child not in TT):
                curr = max(DFS(child, TT, depth-1, debug), curr)
        if curr == SOLVED:
            print(root)
        return curr

def IDS(root, max_depth=20, debug = False):
    for depth in range(1, max_depth + 1):
        TT = set()
        result = DFS(root, TT, depth, debug)
        if (result == SOLVED):
            break
    print(f"Up to depth {depth}: {RESULT_STR[result]}")
