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
        Initializes the Player class to an assigned colour.
        """
        self.colour = colour

        self.opponents = [i for i in COLOURS if i != self.colour]

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
        self.state[self.opponents[0]] = [ # Opponent 1
            START_POINT[self.opponents[0]],
            INITIAL_PIECE_COUNT,
            INITIAL_EXITED_PIECES
        ]
        self.state[self.opponents[1]] = [ # Opponent 2
            START_POINT[self.opponents[1]],
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
        Based on the current state of the game, it will decide on an action to make.
        :returns: an action in format ("MOVE", ((q1, r2), (q2, r2))) if possible, else ("PASS", None)
        :globals: NUMBER_OF_ACTIONS keeps track of the number of actions taken (in case we need it)
        """

        action = agent_logic(self, random=True)

        NUMBER_OF_ACTIONS += 1

        if bool(action[0]):
            return action
        
        return ("PASS", None)


    def update(self, colour, action):
        """
        Updates the internal board state representation given:
            - Our player
            - The colour of the player who made an action
            - The action itself
        """
        # Current Action Coordinate
        current = action[1][0]
        state = self.state

        if action[0] == "EXIT":
            # If there is an exit, no destination coordinate for piece
            # Doesn't affect any other players
            state[colour][PIECE_COORD].remove(current)
            state[colour][NO_PIECE] -= 1
            state[colour][NO_EXIT_PIECE] += 1
        elif action[0] == "JUMP":
            print("\n\nJUMP WAS MADE")
            # Destination Coordinate
            destination = action[1][1]
            # Find the piece colour and coordinate that was jumped
            jumped_colour, jumped_hex = find_jumped_piece(self, action[1])

            # If the jumped piece was ours and it is OUR action
            # Does not affect any other player
            if jumped_colour == self.colour and self.colour == colour:
                print("JUMP WAS OVER OUR OWN PIECE")
                state[self.colour][PIECE_COORD].remove(current)
                state[self.colour][PIECE_COORD].add(destination)
            # If the jumped piece was another players piece and it was their turn
            # Does not affect any other player
            elif jumped_colour == colour:
                print("A PLAYER JUMPED OVER THEIR OWN PIECE")
                state[colour][PIECE_COORD].remove(current)
                state[colour][PIECE_COORD].add(destination)
            else:
                print("A PIECE WAS CAPTURED")
                # If the jumped piece was ours and it is another players action
                # Our piece was captured. Remove ours and add it to the capturing opponent
                if jumped_colour == self.colour and colour != self.colour:
                    print("OUR PIECE WAS CAPTURED")
                    # Remove our piece
                    state[self.colour][PIECE_COORD].remove(jumped_hex)
                    state[self.colour][NO_PIECE] -= 1
                    # Update opponent piece
                    capturing_opponent = state[colour] # Capturing Opponents state
                    capturing_opponent[PIECE_COORD].remove(current)
                    capturing_opponent[PIECE_COORD].add(jumped_hex)
                    capturing_opponent[PIECE_COORD].add(destination)
                    capturing_opponent[NO_PIECE] += 1
                # If the jumped piece was not ours but we made the jump
                # We captured a piece. Remove their piece and it to ours
                elif jumped_colour != self.colour and colour == self.colour:
                    print("WE CAPTURED A PIECE")
                    # Find the captured opponents colour
                    captured_opponent = state[jumped_colour] # Captured Opponents state
                    # Remove their piece
                    captured_opponent[PIECE_COORD].remove(jumped_hex)
                    captured_opponent[NO_PIECE] -= 1
                    # Add the captured piece and our jumping piece coordinates
                    state[self.colour][PIECE_COORD].remove(current)
                    state[self.colour][PIECE_COORD].add(jumped_hex)
                    state[self.colour][PIECE_COORD].add(destination)
                    state[self.colour][NO_PIECE] += 1
                # If the jumped piece was not ours and it is another players action
                # Does not affect us
                else:
                    print("ANOTHER PLAYERS PIECE WAS CAPTURED")
                    # Capturing player colour and captured player colour
                    capturing_player = state[colour] # Capturing players state
                    captured_player = state[jumped_colour] # Captured players state
                    # Remove captured players' piece
                    captured_player[PIECE_COORD].remove(jumped_hex)
                    captured_player[NO_PIECE] -= 1
                    # Add the captured piece and the capturing players' piece coordinates
                    capturing_player[PIECE_COORD].remove(current)
                    capturing_player[PIECE_COORD].add(jumped_hex)
                    capturing_player[PIECE_COORD].add(destination)
                    capturing_player[NO_PIECE] += 1

            print("Number of Pieces:")
            print(f"Red {state['red'][NO_PIECE]} Green {state['green'][NO_PIECE]} Blue {state['blue'][NO_PIECE]}")
        else:
            # MOVE action was completed
            # Doesn't affect any players
            destination = action[1][1]
            state[colour][PIECE_COORD].remove(current)
            state[colour][PIECE_COORD].add(destination)

        print(f"Player {self.colour} - Successfully updated internal state for {colour}:")
        print(state)
        print('*'*80)







POSSIBLE_DIRECTIONS = [(-1,+0),(+0,-1),(+1,-1),(+1,+0),(+0,+1),(-1,+1)]