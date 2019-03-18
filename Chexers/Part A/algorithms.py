""" Algorithms.py

Implements algorithms for use in game exploration, NOT actual agent logic.

Notes:
- Globals below for analysis.
- Utilise game_status to tell if trimmed (symmetrical flag) --> DONT Explore
- Maybe have a different flag; so that way, one flag = "win/loss/draw", the other is "trim/duplicate" etc,
"""

COUNT_TRIM = 0
COUNT_TOTAL = 0
COUNT_PER_DEPTH = list() # index by depth, e.g. COUNT_PER_DEPTH[5] has total count @ depth 5. Depth 0 is root.

"""Agent-INDEPENDENT Node structure with core information
Call like Node(hash, parent, alpha, beta, gamma, delta)"""
class Node:
    def __init__(self, hashed_state, parent, *data):
        COUNT_TOTAL += 1
        self.state = hashed_state.data() # Board state data: piece positions, # exits etc. accessed through here
        self.data = list(data) # For any other data like alpha/betas etc.
        self.player = self.get_player() # Flag for which player you are
        self.game_status = self.get_status(self)
        self.children = list() # Could be different, maybe a PQ for weighted choices acc. heuristic
        self.parent = parent # MUST BE REFERENCE, NOT COPY # Points to parent Node
        self.possible_moves = possible_moves(self.data)

    # FINALISE ACTIONS FIRST
    def create_children(self, actions):
        """Given a chosen action(s), create children
        MUST BE STORED AS REFERENCES TO CHILDREN"""
        # Apply_board()

    def apply_move(self, action):
        """Applies action and returns new Node (state)"""

    # FINALISE DATA FIRST
    def get_status(self):
        """1 W_RED, 2 W_GR, 3 W_BL, 0 NONE, -1 DRAW -2 DUPLICATE for is_over call
        Determines if a win/loss/draw has occurred
        just read it from the state hash"""
        pass

    ######################### GETTERS AND SETTERS ############################
    # FINALISE DATA FIRST
    def _get_player(self):
        """Retrieves current player. ONLY IMPLEMENT AFTER "DATA" structure FINALISED
        Consider just reading it from the state hash"""
        pass
