"""
Missionaries and Cannibals Problem
   Uninformed Search Approach

   DEPTH-FIRST SEARCH ALGO.
  *--------------------------*

Author: Matthew Farrugia-Roberts
"""

from mc_problem.state import State

def main():
    # how many on starting side?
    initial_state = State(3, 3, 1)
    #                     |  |  |
    #      missionaries --*  |  |
    #      cannibals --------*  |
    #      the boat ------------*

    states_prev = {initial_state: None}
    state_stack = [(initial_state, 0)]
    while state_stack and not state_stack[-1][0].is_goal():
        state, depth = state_stack.pop()
        print('.' * depth + "expanding:", state)
        for successor_state in state.successors():
            if successor_state in states_prev:
                continue
            state_stack.append((successor_state, depth+1))
            states_prev[successor_state] = state

    if state_stack:
        goal, cost = state_stack[-1]
        print("goal found:", goal)
        path = reconstruct_path(states_prev, goal)
        print("path:", path)
    else:
        print("no path found...")


def reconstruct_path(prev_dict, end_state):
    path = []
    state = end_state
    while prev_dict[state] is not None:
        path.append(state)
        state = prev_dict[state]
    path.append(state)
    return path[::-1]

if __name__ == '__main__':
    main()
