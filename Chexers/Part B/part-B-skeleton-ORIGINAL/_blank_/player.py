"""
Team: _blank_ 
player.py to hold our player class
"""
# Import Dependencies
from .agent_logic import *
import numpy as np

# Global Variables
INITIAL_PIECE_COUNT = 4
INITIAL_EXITED_PIECES = 0
NUMBER_OF_ACTIONS = 0

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

        opponent_colours = [i for i in COLOURS if i != self.colour]

        self.own_state = START_POINT[colour]
        self.opponents = {
            opponent_colours[0]: Opponent(opponent_colours[0]),
            opponent_colours[1]: Opponent(opponent_colours[1])
        }
        self.goal = GOAL[colour]
        print("*"*80)
        print(self)
        print(self.own_state)
        print(self.opponents[opponent_colours[0]].own_state)
        print(self.opponents[opponent_colours[1]].own_state)
        print("*"*80)
        
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
        p3 = ''.join([i for i in COLOURS if i != self.colour and i != colour]) # The third player (not us or the current player in turn)

        current = action[1][0]
        if action[0] != "EXIT":
            destination = action[1][1]
        
        if colour == self.colour: # This is us
            
            print("*"*80)
            print(f"PLAYER {self.colour.upper()} (C U R R E N T)\nOUR CURRENT STATE:", self.own_state)
    
            if action[0] == "EXIT":
                self.own_state.remove(current)
                self.pieces -= 1
                self.exited_pieces += 1
            else:
                self.own_state.remove(current)
                self.own_state.add(destination)

            print("UPDATED TO: ", self.own_state)
            print("\nOPPONENT STATES:")
            for i in list(self.opponents.values()):
                print(f"OPPONENT {i.colour.upper()} HAS STATE {i.own_state}")
            print("*"*80)
        else:
            print("*"*80)

            print(f"OPPONENT {self.colour.upper()} STATE IS:")
            print(self.own_state)
            
            opponent = self.opponents[colour]

            print(f"OPPONENT {self.colour.upper()}'s OTHER OPPONENT THATS NOT US (OPPONENT {p3.upper()}) HAS STATE:")
            print(opponent.own_state)
            print("*"*80)

            # for some reason it updates wat
            # if action[0] == "EXIT":
            #     opponent.own_state.remove(current)
            #     opponent.pieces -= 1
            #     opponent.exited_pieces += 1
            # else:
            #     print("error here")
            #     opponent.own_state.remove(current)
            #     opponent.own_state.remove(destination)


class Opponent:
    def __init__(self, colour):
        self.own_state = START_POINT[colour]
        self.colour = colour
        self.pieces = INITIAL_PIECE_COUNT
        self.exited_pieces = INITIAL_EXITED_PIECES
