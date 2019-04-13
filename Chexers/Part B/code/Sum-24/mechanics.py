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
GAME_NAME = "Sum-24"
MAX_TURNS = 100 # per player

# Needs implementing
TEMPLATE_DEBUG = TEMPLATE_NORMAL = """*   ##############################
*   scores: {0}
*   Turn Player: {1} Total: {2}
*   ##############################"""

POSSIBLE_ADDITIONS = (1,2,3)
ACTION_TYPE = "ADD"

MAX_VALUE = 24

##################### CODES FOR PLAYERS ######################
"""
Do NOT need to redefine.
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

# State  = (current_total, turn_player_code)

def create_initial_state():
    """Returns the starting game state"""
    return (0, PLAYER_CODES[0])

def possible_actions(state):
    """Returns list of possible actions for a given state"""
    result = []
    for number in POSSIBLE_ADDITIONS:
        action = (ACTION_TYPE, number)
        if valid_action(state, action):
            result.append(action)

    return result

def valid_action(state, action):
    """Checks validity of an action to be applied to a State, returns boolean"""
    current_total = state[0]
    atype, aarg = action
    return (1 <= aarg <= 3 and atype == ACTION_TYPE)

def apply_action(state, action):
    """Applies an action to a State object, returns new state"""
    atype, aarg = action
    current_total, turn_player = state
    new_total = current_total + aarg
    return (new_total, next_player(state))

def player(state):
    """Retrieves current player"""
    return state[1]

def next_player(state):
    """Determines next player"""
    turn_player = player(state)
    if turn_player == PLAYER_CODES[0]:
        return PLAYER_CODES[1]
    else:
        return PLAYER_CODES[0]

def get_score(state, colour_code):
    """
    Retrieves score for player in a state.
    colour_code is the single-letter code, e.g. 'r'
    """
    if not game_over(state):
        return 0
    elif is_winner(state, colour_code):
        return 1
    else:
        return -1

def game_drawn(state):
    """Returns True if game is tied else false"""
    return False

def game_over(state):
    """Determines if a game is over"""
    return state[0] >= MAX_VALUE

def is_winner(state, colour_code):
    """Returns True if player represented by colour has won"""
    return game_over(state) and player(state) != colour_code

def encode(state):
    """Defines a low-collision invertible hash for a State object"""
    return state

def decode(state):
    """Decodes a hashed State back into a State object"""
    return state

def get_template(debug=False):
    """Returns the desired template for printing."""
    return TEMPLATE_NORMAL

def get_strings_for_template(state, debug=False):
    """Gets the strings for insertion into the template."""
    return [str(i) for i in state][::-1]

def action_str(action):
    """Defines how to print an action, for logging and display
    E.g. 'TYPE, from X to Z'"""
    atype, aarg = action
    return f"chose to {atype} {aarg}"
