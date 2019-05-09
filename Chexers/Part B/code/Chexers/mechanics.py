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
from moves import VALID_COORDINATES, midpoint, move_action, jump_action, exit_action, jump_sort

########################### GLOBALS ##########################

N_PLAYERS = 3
INITIAL_EXITED_PIECES = 0

MAX_TURNS = 256 # PER PLAYER
MAX_EXITS = 4
MAX_COORDINATE_VAL = 3

STARTS = {
    'red': [(-3,3), (-3,2), (-3,1), (-3,0)],
    'green': [(0,-3), (1,-3), (2,-3), (3,-3)],
    'blue': [(3, 0), (2, 1), (1, 2), (0, 3)],
}

##################### CODES FOR PLAYERS ######################

# A default list of all the player names: note the auto-slicing
PLAYER_NAMES = ["red", "green", "blue"]

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

###################### CORE FUNCTIONALITY ####################

def create_initial_state():
    """
    Returns the starting game state
    :returns: copy of new initial game state
    """
    #### TODO: Instead of deepcopy(), we can just hardcode it here since we
    ####       won't be using the global again.
    initial_state = deepcopy(STARTS)
    initial_state['exits'] = {name: INITIAL_EXITED_PIECES for name in PLAYER_NAMES}
    initial_state['turn'] = 'red'
    initial_state['depth'] = 0
    return initial_state

def player(state):
    """
    Retrieves current player
    """
    return state['turn']

def depth(state):
    """
    Returns number of turns (interpret 1 = first move by red)
    """
    return state['depth']

# NOTE: I simplified stuff, should still work
def next_player(state, ignore_dead=False):
    """
    Determines next player. Can reduce to 2-player if ignore_dead is True.
    :returns: player string
    """
    # Exploits ordering of PLAYER_NAMES, gets index of next along
    if ignore_dead and len(players_left(state)) < N_PLAYERS:
        # If no alive opponents, return self
        # If one alive aopponent, return them
        # Else, just return as usual
        curr_player = player(state)
        alive_opponents = [i for i in get_opponents(state) if not is_dead(state, i) and i != curr_player]
        if not alive_opponents:
            return curr_player
        elif len(alive_opponents) == 1:
            return alive_opponents.pop(0)
        else:
            return next_player(state, False)
    else:
        # Normal functionality
        current_index = PLAYER_HASH[state['turn']]
        return PLAYER_NAMES[(current_index + 1) % N_PLAYERS]

def get_score(state, colour):
    """
    Retrieves score (number of exits made) for player in a state.
    """
    return state['exits'][colour]

def game_drawn(state, counts):
    """
    Detects if game drawn
    """
    return (counts[draw_hash(state)] >= MAX_EXITS or state['depth'] == MAX_TURNS*3)

def game_over(state, print_debug=False):
    """
    Determines if a game is over.
    :returns: boolean which is True if game is over.
    Conditions:
    - A player has exited all pieces (winner)
    - 256 move max for each player has been exceeded (TODO)
    - A state has been visited 4 times (draw)

    TODO: ALL_DEAD IS NOT AN ACTUAL GAME OVER SCENARIO, DELETE AFTER DEBUG

    """
    draw = depth(state) == MAX_TURNS * 3
    all_dead = sum([bool(state[colour]) for colour in PLAYER_NAMES]) == 1
    winner = MAX_EXITS in state['exits'].values()

    if print_debug:
        print(f"\n\t\t\t\t\t\t\t\tMax-turns: {draw}, All Dead: {all_dead}, Winner: {winner}")
        return None

    return winner or draw

def apply_action(state, action, ignore_dead=False):
    """
    Applies an action to a State object
    :returns: new fully updated state
    """
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
    """
    Checks if an action to be applied to a state will capture
    :returns: boolean
    """
    flag, pieces = action
    if flag != "JUMP": return False
    old, new = pieces
    # Returns true if what it would jump over is not its own
    return (midpoint(old, new) not in state[colour])

def possible_actions(state, colour, sort=False):
    """
    Returns list of possible actions for a given state
    """
    actions = list()

    # All occupied hexes (doesn't account for who's who)
    occupied_hexes = function_occupied(state, PLAYER_NAMES)

    actions.extend(exit_action(state, colour))
    if sort:
        actions.extend(jump_sort(state, jump_action(state, occupied_hexes, colour), colour))
    else:
        actions.extend(jump_action(state, occupied_hexes, colour))
    actions.extend(move_action(state, occupied_hexes, colour))

    if not actions:
        return [("PASS", None)]
    else:
        return actions

###################### OTHER FUNCTIONS ########################

#### TODO: Rename, check redundancy
def function_occupied(state, colours):
    """
    Fetches set of all pieces for all colours
    :returns: {pieces_for_specified_colours}
    """
    occupied = set()
    for player in colours:
        occupied.update(set(state[player]))
    return occupied

def is_dead(state, colour):
    """
    Returns whether a specified player (colour) has lost all player_pieces
    :returns: boolean
    """
    return not bool(state[colour])

######################### TOO MANY? ###########################

def num_opponents_dead(state):
    """
    Find the number of dead players (player with no pieces left)
    """
    return sum([is_dead(state, player) for player in PLAYER_NAMES])

def two_players_left(state):
    """
    Checks if one player has lost all pieces
    :returns: boolean
    """
    return len(players_left(state)) == 2

def get_opponents(state):
    """
    Fetches a turn player's opponents
    :returns: list(
    opponent_names in order)
    """
    return [player for player in PLAYER_NAMES if player != state['turn']]

def get_remaining_opponent(state):
    """
    Fetches a turn player's only remaining (alive) opponent
    Assumes only one left alive
    :returns: list(alive_opponent_names in order)
    """
    ### TODO NOTE: Seems redundant but I left it here until we discuss it
    return [opponent for opponent in get_opponents(state) if not is_dead(state, opponent)].pop(0)

def players_left(state):
    """
    Finds all players left
    :returns: list(all_alive_players in order)
    """

    return [player for player in PLAYER_NAMES if len(state[player]) > 0]

########################## HASHING ############################

def draw_hash(state):
    """
    Hashing scheme but without the exits - so that draws can be detected
    """
    return Z_hash(state) >> CODE_LEN * N_PLAYERS

def Z_hash(state):
    """
    Implements a minimal collision NON-INVERTIBLE hash for states. Hash of form
        0b(turn)(exits)(37 hex state flags....)
    Where the flags are:
    - For turn player:
        - 00 for red
        - 01 for green
        - 10 for blue
    - For the 37 hexes:
        - 01 for red
        - 10 for green
        - 11 for blue
        - 00 for none
    :returns: integer unique to the state
    """
    hashed = 0

    # Append turn player
    hashed = hashed | PLAYER_HASH[state["turn"]]

    # Encode coordinates: First, make space
    hashed = hashed << NUM_HEXES * CODE_LEN

    # ith pair of 2-bits = ith location in VALID_COORDINATES
    for player in PLAYER_NAMES:
        for piece in state[player]:
            hashed = hashed | (PLAYER_HASH[player] + 1 << CODE_LEN * VALID_COORDINATES.index(piece))

    # Encode exits
    hashed = hashed << CODE_LEN * N_PLAYERS
    for i, player in enumerate(PLAYER_NAMES):
            hashed = hashed | (state['exits'][player] << i)

    return hashed
