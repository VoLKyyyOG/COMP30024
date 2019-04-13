"""
Team: _blank_ 
player.py to hold our player class
"""
# Import Dependencies
from .agent_logic import *
import numpy as np
from collections import defaultdict

# Global Variables
INITIAL_PIECE_COUNT = 4
INITIAL_EXITED_PIECES = 0
NUMBER_OF_ACTIONS = 0

# Indexes of the internal board state
PIECE_COORD, NO_PIECE, NO_EXIT_PIECE = 0, 1, 2

START_POINT = {
    "red": {(-3,3), (-3,2), (-3,1), (-3,0)},
    "green": {(0,-3), (1,-3), (2,-3), (3,-3)},
    "blue": {(3, 0), (2, 1), (1, 2), (0, 3)}
}

GOAL = {
    "red": {(3,-3), (3,-2), (3,-1), (3,0)},
    "green": {(-3,3), (-2,3), (-1,3), (0,3)},
    "blue": {(-3,0),(-2,-1),(-1,-2),(0,-3)},
}


COLOURS = ["red", "green", "blue"]

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
        self.colour = colour

        opponent = [i for i in COLOURS if i != self.colour]

        """
        self.state represents our internal board state using a defaultdict.
        self.state holds players: [red, green, blue]
        :format: [piece coordinates, number of pieces, number of exited pieces]
        """
        self.state = defaultdict(list)
        self.state[colour] = [ # This is our assigned colour
            START_POINT[colour],
            INITIAL_PIECE_COUNT,
            INITIAL_EXITED_PIECES
        ]
        self.state[opponent[0]] = [ # Opponent 1
            START_POINT[opponent[0]],
            INITIAL_PIECE_COUNT,
            INITIAL_EXITED_PIECES
        ]
        self.state[opponent[1]] = [ # Opponent 2
            START_POINT[opponent[1]],
            INITIAL_PIECE_COUNT,
            INITIAL_EXITED_PIECES
        ]

        self.goal = GOAL[colour]

        print("*"*80)
        print(f"Player {colour} has been initialized")
        print(self.state)
        print("*"*80)

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
        ##### FOR NOW ALL AGENTS PLAY RANDOM MOVES
        # Code below assumes we are player Red, therefore all other players will be random
        # This means for random = False we can use a strategy
        # choice = agent_logic(self, self.colour == "red")

        choice = agent_logic(self)

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
        # AKIRA TODO: write function to see if action is jump, check piece captured
        # Current Coordinate
        current = action[1][0]
        player = self.state[colour]
        player[PIECE_COORD].remove(current)

        if action[0] == "EXIT":
            # If there is an exit, no destination for piece
            player[NO_PIECE] -= 1
            player[NO_EXIT_PIECE] += 1
        elif action[0] == "JUMP":
            # player has jumped over a coordinate
            # if player has jumped over NOT their piece
                # THEN need to get the coordinate thats jumped over
                # FIND colour of piece on that coordinate
                # colour captured will -=1
                # player no pieces will += 1
                # remove piece from colour captured
                # add piece to our state
            # else just append the new destination
            pass
        else:
            destination = action[1][1]
            player[PIECE_COORD].add(destination)

        print(f"Updated internal state for {colour}:")
        print(player)


class Opponent:
    def __init__(self, colour):
        self.state = START_POINT[colour]
        self.colour = colour
        self.pieces = INITIAL_PIECE_COUNT
        self.exited_pieces = INITIAL_EXITED_PIECES
