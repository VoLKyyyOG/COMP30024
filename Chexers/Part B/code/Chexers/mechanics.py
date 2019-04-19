""" mechanics.py

Contains core game functionality: defines number of players, name,
maximum turns, player names and codes, what a State object is, and any
game-specific functions and variables.

"""

########################### IMPORTS ##########################
# Standard modules
from copy import deepcopy
# User-defined files
from moves import *

########################### GLOBALS ##########################

N_PLAYERS = 3 # Must be 2 minimum
GAME_NAME = "Chexers"
MAX_TURNS = 256 # per player

# Needs implementing
TEMPLATE_NORMAL = """*   scores: {0}
*   board:    .-'-._.-'-._.-'-._.-'-.
*            |{16:}|{23:}|{29:}|{34:}|
*          .-'-._.-'-._.-'-._.-'-._.-'-.
*         |{10:}|{17:}|{24:}|{30:}|{35:}|
*       .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
*      |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}|
*    .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
*   |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}|
*   '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
*      |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}|
*      '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
*         |{03:}|{08:}|{14:}|{21:}|{28:}|
*         '-._.-'-._.-'-._.-'-._.-'-._.-'
*            |{04:}|{09:}|{15:}|{22:}|
*            '-._.-'-._.-'-._.-'-._.-'"""

TEMPLATE_DEBUG = """*   scores: {0}
*   board:       ,-' `-._,-' `-._,-' `-._,-' `-.
*               | {16:} | {23:} | {29:} | {34:} |
*               |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
*            ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
*           | {10:} | {17:} | {24:} | {30:} | {35:} |
*           | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
*        ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
*       | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
*       | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
*    ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
*   | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
*   | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
*    `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
*       | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
*       | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
*        `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
*           | {03:} | {08:} | {14:} | {21:} | {28:} |
*           | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
*            `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
*               | {04:} | {09:} | {15:} | {22:} |   | input |
*               | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
*                `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

##################### CODES FOR PLAYERS ######################

# A default list of all the player names: note the auto-slicing
PLAYER_NAMES = [
    "red", "green", "blue",
    "orange", "yellow", "purple"
][:N_PLAYERS]

# 'r', 'g', etc. for display usage
PLAYER_CODES = [name[0] for name in PLAYER_NAMES]

# Maps 'r', 'g' to 'red', 'green' etc.
NAMING_DICT = {name[0]: name for name in PLAYER_NAMES}
NAMING_DICT.update({name: name[0] for name in PLAYER_NAMES})

INITIAL_EXITED_PIECES = 0
MAX_EXITS = 4
MAX_ACTIONS_PER_PIECE = 6

# For hashing
NUM_HEXES = 37
CODE_LEN = 2 # Bit length of each flag. Can be 0,1,2,3
# bidirectional lookup for player bit code
PLAYER_HASH = {
    "red": 0b00,
    "green" : 0b01,
    "blue" : 0b10,
    "none" : 0b11
}
PLAYER_HASH.update(dict(zip(PLAYER_HASH.values(), PLAYER_HASH.keys())))

##################### STATE FUNCTIONALITY ####################

"""After defining what a state data structure is, code the following

state = {red=list(), green=list(), blue=list(), exits=dict(), turn=str, depth=0}
action = (MOVE, (loc_1, loc_2)), (JUMP, (loc_1, loc_2)), (EXIT, (loc_1)),  (PASS, None)

# Must be copyable

"""

def create_initial_state():
    """Returns the starting game state"""
    #### TODO: Instead of deepcopy(), we can just hardcode it here since we
    ####       won't be using the global again.
    ####       Confirming that we derive number of pieces using len() in two_players left
    initial_state = deepcopy(STARTS)
    initial_state['exits'] = {name: INITIAL_EXITED_PIECES for name in PLAYER_NAMES}
    initial_state['turn'] = 'red'
    initial_state['depth'] = 0
    return initial_state

def player(state):
    """Retrieves current player"""
    return state['turn']

def depth(state):
    """Returns number of turns"""
    return state['depth']

def occupied(state, colours):
    """Fetches set of all pieces for all colours"""
    occupied = set()
    for player in colours:
        occupied.update(set(state[player]))
    return occupied

def next_player(state, ignore_dead=False):
    """Determines next player. Can reduce to 2-player if ignore_dead"""
    # Exploits ordering of PLAYER_NAMES, gets index of next along
    if ignore_dead and two_players_left(state):
        try:
            return get_opponents(state).pop()
        except:
            print("NEXT_PLAYER ERROR ... this is easily fixed")
    else:
        current_index = PLAYER_NAMES.index(state['turn'])
        return PLAYER_NAMES[(current_index + 1) % N_PLAYERS]

#### TODO: May be redundant
def prev_player(state, ignore_dead=False):
    """Determines previous player"""
    # Exploits ordering of PLAYER_NAMES, gets index of next along
    if ignore_dead and two_players_left(state):
        return get_opponents(state).pop()
    current_index = PLAYER_NAMES.index(state['turn'])
    return PLAYER_NAMES[(current_index - 1) % N_PLAYERS]

def get_score(state, colour):
    """Retrieves score for player in a state."""
    return state['exits'][colour]

def game_over(state):
    """
    Determines if a game is over.
    Conditions:
    - A player has exited all pieces
    - 2 players have been eliminated
    - 256 move max for each player has been exceeded
    - A state has been visited 4 times
    """
    draw = depth(state) == MAX_TURNS * N_PLAYERS
    all_dead = sum([bool(state[colour]) for colour in PLAYER_NAMES]) == 1
    winner = MAX_EXITS in state['exits'].values()

    return winner or draw or all_dead

def apply_action(state, action, ignore_dead=False):
    """Applies an action to a State object, returns new state"""
    flag, pieces = action
    new_state = deepcopy(state)

    print("\n\nPRINTING STATE AND NEW STATE")
    print(state)

    turn_player = new_state['turn']

    player_pieces = new_state[turn_player]
    if flag in ("MOVE", "JUMP"):
        old, new = pieces

        # AKIRA DEBUG - GREEDY IS BROKEN AFTER SOME SEVERAL NUMBER OF MOVES
        """
        line 183, in apply_action
        player_pieces.remove(old)
        ValueError: list.remove(x): x not in list
        """
        try:
            player_pieces.remove(old)
            player_pieces.append(new)
        except ValueError:
            print(f"Flag was found - {flag}")
            print(player_pieces)
            print("Old is",old)
            print("New is",new)
            return None
        #######################################################################

        # Check for captures
        if flag == "JUMP":
            adjacent_hex = midpoint(old, new)
            if adjacent_hex not in player_pieces:
                player_pieces.append(adjacent_hex)
                # Identify opponent and remove it
                for player in PLAYER_NAMES:
                    if player != turn_player and adjacent_hex in new_state[player]:
                        new_state[player].remove(adjacent_hex)

    elif flag == "EXIT":
        player_pieces.remove(pieces)
        new_state['exits'][turn_player] += 1

    elif flag == "PASS":
        pass

    # Update turn player
    new_state['turn'] = next_player(state, ignore_dead)
    new_state['depth'] += 1
    print(new_state)
    return new_state

def is_capture(state, action, colour):
    """Checks if an action to be applied to a state will capture"""
    atype, pieces = action
    if atype != "JUMP": return False
    old, new = pieces
    return midpoint(old, new) not in state[colour]

def possible_actions(state, colour, paranoid_ordering=False):
    """Returns list of possible actions for a given state"""
    actions = list()

    if game_over(state):
        return actions

    # All occupied hexes (doesn't account for who's who)
    occupied_hexes = occupied(state, PLAYER_NAMES)

    # Append exits, moves, jumps and passes respectively
    if paranoid_ordering:
        possible_exits = exit_action(state, colour)
        if bool(possible_exits):
            actions.extend(possible_exits)
            return actions
        actions.extend(jump_action(state, occupied_hexes, colour))
        actions.extend(move_action(state, occupied_hexes, colour))
        return actions
    else:
        actions.extend(jump_action(state, occupied_hexes, colour))
        actions.extend(move_action(state, occupied_hexes, colour))
        actions.extend(exit_action(state, colour))

    if not actions:
        return [("PASS", None)]
    else:
        return actions

def encode(state):
    """Defines a low-collision invertible hash for a State object"""
    return Z_hash(state, ignore_exits=True)

def decode(state):
    """Decodes a hashed State back into a State object"""
    raise NotImplementedError

def get_strings_for_template(state, debug=False):
    """Gets the strings for insertion into the template."""
    string_stor = dict()
    for name in PLAYER_NAMES:
        for piece in state[name]:
            string_stor[piece] = f"  {name[0].upper()}  "
    result = ["     "] * NUM_HEXES
    for piece in string_stor:
        result[VALID_COORDINATES.index(piece)] = string_stor[piece]
    return result

def log_action(state, action):
    """Defines how to print an action, for logging and display
    E.g. 'TYPE, from X to Z'"""
    flag, pieces = action
    base_str = f"chose to {flag}"
    capture_str = ""
    if (flag == "PASS"):
        return base_str
    elif flag == "EXIT":
        return base_str + f" {pieces}" + f" - exits now {state['exits']}"
    else:
        if flag == "JUMP" and is_capture(state, action, state['turn']):
            old, new  = pieces
            captured = midpoint(old, new)
            for player in PLAYER_NAMES:
                if captured in state[player]:
                    total_pieces = ', '.join([str(len(state[x])) for x in PLAYER_NAMES])
                    capture_str = f" - you mad {player}? Piece totals {total_pieces}"

        # Any other flags can go here
        return base_str + f" {pieces[0]} to {pieces[1]}{capture_str}"

def get_template(debug=False):
    """Returns the desired template for printing."""
    if debug:
        template = TEMPLATE_DEBUG
    else:
        template = TEMPLATE_NORMAL
    return template

def two_players_left(state):
    """Checks if one player has lost all pieces"""
    if not game_over(state):
        return len(players_left(state)) == 2
    return False

def get_opponents(state):
    """Fetches a turn player's opponents"""
    return [player for player in PLAYER_NAMES if player != state['turn']]

def players_left(state):
    """Finds all players left"""
    return [player for player in PLAYER_NAMES if len(state[player])]

########################## HASHING ############################

def Z_hash(state, ignore_exits=True):
    """
    Implements a minimal collision hash for states
    Hash of the form
        0b(turn)(exit_counts)(37 hex state flags....)
    Where
    - For turn player:
        - 00 for red
        - 01 for green
        - 10 for blue
    - For the 37 hexes:
        - 01 for red
        - 10 for green
        - 11 for blue
        - 00 for none """

    hashed = 0

    # Append turn player
    hashed = hashed | PLAYER_HASH[state["turn"]]

    # Exit count hashing if included. Note that 4 won't work - game over
    if not ignore_exits:
        # Ordered iteration
        for name in PLAYER_NAMES:
            hashed = (hashed << CODE_LEN) | state['exits'][name]

    # Encode coordinates: First, make space
    hashed = hashed << NUM_HEXES * CODE_LEN

    # ith pair of 2-bits = ith location in VALID_COORDINATES
    for name in PLAYER_NAMES:
        for piece in state[name]:
            hashed = hashed | (PLAYER_HASH[name] + 1 << CODE_LEN * VALID_COORDINATES.index(piece))

    return hashed
