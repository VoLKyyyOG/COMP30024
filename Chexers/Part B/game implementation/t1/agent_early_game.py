
class Agent_Minimax(Agent):
    def __init__(self, player, *args):
        """Initialise Agent, especially any objects/data needed for game"""
        super().__init__()
        self.maximisingPlayer = None # Symbol for maximisingPlayer
        self.heuristic = None # Must take inputs (state, maximisingPlayer)
        raise NotImplementedError

    def action(self):
        """Decide on an Action and return it"""
        choice = minimax(self.state, self.heuristic, self.maximisingPlayer)[0]
        assert(choice) # Shouldn't get to endgame, referee should catch first
        return choice
        raise NotImplementedError

