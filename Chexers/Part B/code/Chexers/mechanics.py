""" mechanics.py

Contains core game functionality: defines number of players, name,
maximum turns, player names and codes, what a State object is, and any
game-specific functions and variables.

"""

########################### IMPORTS ##########################

# Standard modules
from math import inf
from copy import deepcopy
from collections import defaultdict

# User-defined files
from moves import midpoint, move_action, jump_action, exit_action

########################### GLOBALS ##########################

N_PLAYERS = 3
INITIAL_EXITED_PIECES = 0

MAX_TURNS = 256 # PER PLAYER
MAX_EXITS = 4
MAX_COORDINATE_VAL = 3

CORNER_HEXES = [
    (-3, 0), (-3, 3), (0, 3), (3, 0), (3, -3), (0, -3)
]

STARTS = {
    'red': [(-3,3), (-3,2), (-3,1), (-3,0)],
    'green': [(0,-3), (1,-3), (2,-3), (3,-3)],
    'blue': [(3, 0), (2, 1), (1, 2), (0, 3)],

}

##################### CODES FOR PLAYERS ######################

# A default list of all the player names: note the auto-slicing
PLAYER_NAMES = [
    "red", "green", "blue",
    "orange", "yellow", "purple"
][:N_PLAYERS]

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

def function_occupied(state, colours):
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

def get_score(state, colour):
    """Retrieves score for player in a state."""
    return state['exits'][colour]

def game_over(state, print_debug=False):
    """
    Determines if a game is over.
    Conditions:
    - A player has exited all pieces
    - 256 move max for each player has been exceeded
    - A state has been visited 4 times

    TODO: ALL_DEAD IS NOT AN ACTUAL GAME OVER SCENARIO
    """
    draw = depth(state) == MAX_TURNS * 3
    all_dead = sum([bool(state[colour]) for colour in PLAYER_NAMES]) == 1
    winner = MAX_EXITS in state['exits'].values()

    if print_debug:
        print(f"\n\t\t\t\t\t\t\t\tDraw: {draw}, All Dead: {all_dead}, Winner: {winner}")
        return None

    return winner or draw

def is_dead(state, colour):
    return not bool(state[colour])

def apply_action(state, action, ignore_dead=False):
    """Applies an action to a State object, returns new state"""
    flag, pieces = action
    new_state = deepcopy(state)

    turn_player = new_state['turn']

    if is_dead(new_state, turn_player):
        # print(f"\n\t\t\t\t\t\t\t\tPlayer {turn_player} is dead and skipping state")
        new_state['turn'] = next_player(state, ignore_dead)
        return new_state

    player_pieces = new_state[turn_player]
    if flag in ("MOVE", "JUMP"):
        old, new = pieces
        player_pieces.remove(old)
        player_pieces.append(new)

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

    return new_state

def is_capture(state, action, colour):
    """Checks if an action to be applied to a state will capture"""
    atype, pieces = action
    if atype != "JUMP": return False
    old, new = pieces
    return midpoint(old, new) not in state[colour]

def paris(state):
    """
    Evaluates captures that each player could perform
    :returns: {player: list_of_capturing_actions for each player}
    """
    captures = defaultdict(list)
    occupied_hexes = occupied(state, PLAYER_NAMES)
    for player in PLAYER_NAMES:
        for action in jump_action(state, occupied_hexes, player):
            if is_capture(state, action, player):
                captures[player].append(action)
    return captures

def possible_actions(state, colour):
    """Returns list of possible actions for a given state"""
    actions = list()

    # All occupied hexes (doesn't account for who's who)
    occupied_hexes = function_occupied(state, PLAYER_NAMES)

    actions.extend(exit_action(state, colour))
    actions.extend(jump_action(state, occupied_hexes, colour))
    actions.extend(move_action(state, occupied_hexes, colour))

    if not actions:
        return [("PASS", None)]
    else:
        return actions

def two_players_left(state):
    """Checks if one player has lost all pieces"""
    if not game_over(state):
        return len(players_left(state)) == 2
    return False

def get_opponents(state):
    """Fetches a turn player's opponents"""
    return [player for player in PLAYER_NAMES if player != state['turn']]

def get_remaining_opponent(state):
    """Fetches a turn player's remaining opponents"""
    return [opponent for opponent in get_opponents(state) if not is_dead(state, opponent)][0]

def players_left(state):
    """Finds all players left"""
    return [player for player in PLAYER_NAMES if len(state[player])]

########################## HASHING ############################

def encode(state):
    """Defines a low-collision invertible hash for a State object"""
    return Z_hash(state, ignore_exits=True)

def decode(state):
    """Decodes a hashed State back into a State object"""
    raise NotImplementedError

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
