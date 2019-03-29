"""
Missionaries and Cannibals Problem
   Uninformed Search Approach
  *--------------------------*

Author: Matthew Farrugia-Roberts
"""

def main():
    # how many on starting side?
    initial_state = (3, 3, 1)
    #                |  |  |
    # missionaries --*  |  |
    # cannibals --------*  |
    # the boat ------------*

    # states_seen = {initial_state}
    states_prev = {initial_state: None}
    state_stack = [(initial_state, 0)]
    while state_stack and not goal_test(state_stack[-1][0]):
        state, depth = state_stack.pop()
        print('.' * depth + "expanding:", state)
        for successor_state in successors(state):
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

def goal_test(state):
    return not (state[0] or state[1])


def successors(state):
    all_states = []
    if state[2] == 1:
        # boat is on starting side:
        all_states.append((state[0]-2, state[1],   0)) # 2M -->
        all_states.append((state[0]-1, state[1],   0)) # 1M -->
        all_states.append((state[0]-1, state[1]-1, 0)) # 1M1C -->
        all_states.append((state[0],   state[1]-1, 0)) # 1C -->
        all_states.append((state[0],   state[1]-2, 0)) # 2C -->
    else:
        # boat is on other side
        all_states.append((state[0]+2, state[1],   1)) # 2M <--
        all_states.append((state[0]+1, state[1],   1)) # 1M <--
        all_states.append((state[0]+1, state[1]+1, 1)) # 1M1C <--
        all_states.append((state[0],   state[1]+1, 1)) # 1C <--
        all_states.append((state[0],   state[1]+2, 1)) # 2C <--

    # filter out invalid states
    allowed_states = []
    for s in all_states:
        if (0 <= s[0] <= 3 and 0 <= s[1] <= 3              # no negative numbers
                and not (s[0] > 0 and s[0] < s[1])         # not outnumbered (1)
                and not (3-s[0] > 0 and 3-s[0] < 3-s[1])): # not outnumbered (2)
            allowed_states.append(s)

    return allowed_states


if __name__ == '__main__':
    main()
