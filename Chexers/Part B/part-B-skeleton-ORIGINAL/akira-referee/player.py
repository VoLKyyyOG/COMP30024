"""
Team: _blank_ 
player.py to hold our player class
"""
# Import Dependencies
from agent_logic import * # includes moves

# Global Variables
INITIAL_PIECE_COUNT = 4
INITIAL_EXITED_PIECES = 0
NUMBER_OF_ACTIONS = 0

START_POINT = {
    "red": np.matrix([[-3, 0], [-3, 1], [-3, 2], [-3, 3]]),
    "green": np.matrix([[0, -3],[1, -3],[2, -3],[3, -3]]),
    "blue": np.matrix([[3, 0], [2, 1], [1, 2], [0, 3]])
}

COLOURS = np.array(["red", "green", "blue"])

class Player:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (Red, Green or Blue). The value will be one of the 
        strings "red", "green", or "blue" correspondingly.
        """
        # TODO: Set up state representation.

        self.own_state = START_POINT[colour]
        self.opponents = [i for i in COLOURS if i != colour]
        self.colour = colour
        self.pieces = INITIAL_PIECE_COUNT # Can add or subtract depending on captured pieces. If more than 4 then we can sacrifice
        self.exited_pieces = INITIAL_EXITED_PIECES


    def action(self):
        global NUMBER_OF_ACTIONS
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. If there are no allowed 
        actions, your player must return a pass instead. The action (or pass) 
        must be represented based on the above instructions for representing 
        actions.
        """
        # TODO: Decide what action to take.
        if NUMBER_OF_ACTIONS == 0:
            opponent1 = Opponent(self.opponents[0]) # first colour eg green
            opponent2 = Opponent(self.opponents[1]) # second colour eg blue
            assert(opponent1)
            assert(opponent2)

        choice = agent_logic(self, opponent1, opponent2)

        NUMBER_OF_ACTIONS += 1

        if bool(choice[0]):
            return choice
        
        return ("PASS", None)


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red", 
        "green", or "blue" correspondingly.

        The parameter action is a representation of the most recent action (or 
        pass) conforming to the above instructions for representing actions.

        You may assume that action will always correspond to an allowed action 
        (or pass) for the player colour (your method does not need to validate 
        the action/pass against the game rules).
        """
        # TODO: Update state representation in response to action.
        """
        action = ("MOVE", ((0,1), (-1,0)))
        d = {'blue': [(0,1), (0,2), (-1,2)]}
        action[1][0] -> (q1, r2)
        action[1][1] -> (q2, r2)
        NUMPY DELETE IS NOT IN PLACE AND RETURNS A COPY, PYTHON DEL COMPLETELY REMOVES IT
        piece_index = self.opponent[colour].index(action[1][0]) # index of the piece to update in self.opponent[colour]
        if action[0] == 'EXIT':
            del self.opponent[colour][piece_index]
        self.opponent[colour][piece_index] = action[1][1]
        """
        for opponent in self.opponent: # eg "green", "blue"
            print()


class Opponent:
    def __init__(self, colour):
        self.own_state = START_POINT[colour]
        self.colour = colour
        self.pieces = INITIAL_PIECE_COUNT
        self.exited_pieces = INITIAL_EXITED_PIECES