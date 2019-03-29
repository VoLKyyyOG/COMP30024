"""
Missionaries and Cannibals Problem
   Uninformed Search Approach

      STATE REPRESENTATION
  *--------------------------*

Author: Matthew Farrugia-Roberts
"""

class State:
    """
    Represent a missionaries and cannibals problem state
    """
    def __init__(self, missionaries, cannibals, boat):
        self.missionaries = missionaries
        self.cannibals    = cannibals
        self.boat         = boat
    def __str__(self):
        return "S({}, {}, {})".format(self.missionaries, self.cannibals, self.boat)
    def __repr__(self):
        return str(self)

    def __hash__(self):
        my_tuple = (self.missionaries, self.cannibals, self.boat)
        return hash(my_tuple)
    def __eq__(self, other):
        return (self.missionaries, self.cannibals, self.boat) == (other.missionaries, other.cannibals, other.boat)

    def is_goal(self):
        return not (self.missionaries or self.cannibals)
    def successors(self):
        all_states = []
        if self.boat == 1:
            # boat is on starting side:
            all_states.append(State(self.missionaries-2, self.cannibals,   0)) # 2M -->
            all_states.append(State(self.missionaries-1, self.cannibals,   0)) # 1M -->
            all_states.append(State(self.missionaries-1, self.cannibals-1, 0)) # 1M1C -->
            all_states.append(State(self.missionaries,   self.cannibals-1, 0)) # 1C -->
            all_states.append(State(self.missionaries,   self.cannibals-2, 0)) # 2C -->
        else:
            # boat is on other side
            all_states.append(State(self.missionaries+2, self.cannibals,   1)) # 2M <--
            all_states.append(State(self.missionaries+1, self.cannibals,   1)) # 1M <--
            all_states.append(State(self.missionaries+1, self.cannibals+1, 1)) # 1M1C <--
            all_states.append(State(self.missionaries,   self.cannibals+1, 1)) # 1C <--
            all_states.append(State(self.missionaries,   self.cannibals+2, 1)) # 2C <--

        # filter out invalid states
        allowed_states = []
        for state in all_states:
            if (0 <= state.missionaries <= 3 and 0 <= state.cannibals <= 3              # no negative numbers
                    and not (state.missionaries > 0 and state.missionaries < state.cannibals)         # not outnumbered (1)
                    and not (3-state.missionaries > 0 and 3-state.missionaries < 3-state.cannibals)): # not outnumbered (2)
                allowed_states.append(state)

        return allowed_states
