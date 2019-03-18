""" Algorithms.py

Implements algorithms for use in game exploration, NOT actual agent logic.

"""

"""Agent-INDEPENDENT Node structure with core information
Call like Node(hash, parent, alpha, beta, gamma, delta)"""
class Node:
    def __init__(self, hashed_state, parent, *data):
        self.state = hashed_state.data() # Board state data: piece positions, # exits etc. accessed through here
        self.data = list(data) # For any other data like alpha/betas etc.
        self.player = self.get_player() # Flag for which player you are
        self.children = list() # Could be different, maybe a PQ for weighted choices acc. heuristic
        self.parent = parent # Points to parent Node
        self.possible_moves = possible_moves(self.data)

    # FINALISE ACTIONS FIRST
    def create_children(self, actions):
        """Given a chosen action(s), create children"""
        # Apply_board()

    def apply_move(self, action):
        """Applies action and returns new Node (state)"""

    # FINALISE DATA FIRST
    def is_over(self):
        """Determines if a win/loss/draw has occurred"""
        pass

    ######################### GETTERS AND SETTERS ############################
    # FINALISE DATA FIRST
    def _get_player(self):
        """Retrieves current player. ONLY IMPLEMENT AFTER "DATA" structure FINALISED"""
        pass
