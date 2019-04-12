""" referee.py

Refactored referee code, used for any game run.
This referee also records a history of actions made and outputs to a file.


Referee
Runs a game, gets player actions
Checks action validity, visualises game

CORE ATTRIBUTES
GameState
Nplayers
Agents[N]

CORE METHODS
__init__(*agents)
…some_call_to_print_the_state

"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files
from Agent_Terminal import *
# Add any AI Agents here
# import game_visualisation here if you want debugging

################## ADDITIONAL FUNCTIONALITY ##################

def write_history(self):
    # CONSIDER DOING THIS IN 3 SEPARATE FILES - that way, can use File_Agent on
    # 3 separate files, would make parsing MUCH easier.
    raise NotImplementedError

if __name__ == "__main__":
    raise NotImplementedError
