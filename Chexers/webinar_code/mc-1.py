"""
Missionaries and Cannibals Problem
   Uninformed Search Approach
  *--------------------------*

Author: Matthew Farrugia-Roberts
"""

"""
Initial
Side           Goal
      Boat   | 
 M M M  | -> | 
 C C C  |    | 

"""

# how many on starting side?
initial_state = (3, 3, 1)
#                |  |  |
# missionaries --*  |  |
# cannibals --------*  |
# the boat ------------*

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

states_seen = {initial_state}
state_stack = [initial_state]
while state_stack and not goal_test(state_stack[-1]):
    state = state_stack.pop()
    print("expanding:", state)
    for successor_state in successors(state):
        if successor_state in states_seen:
            continue
        state_stack.append(successor_state)
        states_seen.add(successor_state)

if state_stack:
    print("goal found:", state_stack[-1])
else:
    print("no path found...")

