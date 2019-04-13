""" mechanics.py

Contains core game functionality: defines number of players, name,
maximum turns, player names and codes, what a State object is, and any
game-specific functions and variables.

"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files

########################### GLOBALS ##########################

"""Must be defined"""

N_PLAYERS = 2 # Must be 2 minimum
GAME_NAME = "__undef__"
MAX_TURNS = 256 # per player

# Needs implementing
TEMPLATE_NORMAL = """*   scores: {0}
*   (rest of template)'"""
TEMPLATE_DEBUG = """*   scores: {0}
*   (rest of template)"""

##################### CODES FOR PLAYERS ######################
"""
Do NOT need to be redefined.
"""

# A default list of all the player names: note the auto-slicing
PLAYER_NAMES = [
    "red", "green", "blue",
    "orange", "yellow", "purple"
][:N_PLAYERS]

# 'r', 'g', etc. for display usage
PLAYER_CODES = [name[0] for name in PLAYER_NAMES]

# Maps 'r', 'g' to 'red', 'green' etc.
CODE_TO_NAME = {name[0]: name for name in PLAYER_NAMES}
NAME_TO_CODE = {name: name[0] for name in PLAYER_NAMES}

##################### STATE FUNCTIONALITY ####################

"""After defining what a state data structure is, code the following"""

# State = ...
# Must be copyable

"""
Three kinds of errors below:
- RefereeRequiredError (self explanatory)
- AlgorithmRequiredError (optional if not using certain algorithm files)
- NotImplementedError (optional, can delete if want)
"""

class RefereeRequiredError(Exception):
    """This method is utilised by the referee and must be defined"""

class AlgorithmRequiredError(Exception):
    """A number of algorithm files use this and must be defined to work"""

def create_initial_state():
    """Returns the starting game state"""
    raise RefereeRequiredError

def player(state):
    """Retrieves current player"""
    raise AlgorithmRequiredError

def next_player(state):
    """Determines next player"""
    raise NotImplementedError

def prev_player(state):
    """Determines previous player"""
    raise NotImplementedError

def get_score(state, colour_code):
    """
    Retrieves score for player in a state.
    colour_code is the single-letter code, e.g. 'r'
    """
    raise RefereeRequiredError

def game_drawn(state):
    """Returns True if game is tied else false"""
    raise RefereeRequiredError

def game_over(state):
    """Determines if a game is over"""
    raise RefereeRequiredError

def is_winner(state, colour_code):
    """Returns True if player represented by colour has won"""
    raise AlgorithmRequiredError

def valid_action(state, action):
    """Checks validity of an action to be applied to a State, returns boolean"""
    raise NotImplementedError

def apply_action(state, action):
    """Applies an action to a State object, returns new state"""
    raise RefereeRequiredError

def possible_actions(state):
    """Returns list of possible actions for a given state"""
    raise RefereeRequiredError

def encode(state):
    """Defines a low-collision invertible hash for a State object"""
    raise RefereeRequiredError

def decode(state):
    """Decodes a hashed State back into a State object"""
    raise NotImplementedError

def get_strings_for_template(state, debug=False):
    """Gets the strings for insertion into the template."""
    raise RefereeRequiredError

def action_str(action):
    """Defines how to print an action, for logging and display
    E.g. 'TYPE, from X to Z'"""
    raise RefereeRequiredError

def get_template(debug=False):
    """Returns the desired template for printing."""
    if debug:
        template = TEMPLATE_DEBUG
    else:
        template = TEMPLATE_NORMAL
    return template
