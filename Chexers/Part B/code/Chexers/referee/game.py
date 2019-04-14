"""
Provide a class to maintain the state of an evolving game,
including validation of actions, detection of draws,
and optionally maintaining a game log.

NOTE: This board representation is designed to be used internally by the referee
for the purposes of validating actions and displaying the result of the game.
Each player is expected to store its own internal representation of the board
for use in informing decisions about which action to choose each turn. Please
don't look to this module as an example of a useful board representation for
these purposes; you should think carefully about how to design your own data
structures for representing the state of a game.
"""

import sys
import time
from collections import defaultdict
from mechanics import (
        GAME_NAME, N_PLAYERS, PLAYER_NAMES, PLAYER_CODES, NAMING_DICT,
        MAX_TURNS, create_initial_state, apply_action, possible_actions,
        get_score, encode, game_over, get_template, log_action,
        get_strings_for_template
)

#################### STRICTLY GRAPHICS ONLY ##################

if sys.stdout.isatty():
    # Yay! We can use colour

    # Define a str of 5 characters wide for each colour. Can be shorter dep. implementation
    _DISPLAY = {code: f" \033[1m(\033[91m{code.upper()}\033[0m\033[1m)\033[0m " for code in PLAYER_CODES}
    _DISPLAY[' '] = "     "
else:
    # Define a str of 5 characters wide for each colour. Can be shorter dep. implementation
    _DISPLAY = {code: f"  {code.upper()}  " for code in PLAYER_CODES}
    _DISPLAY[' '] = "     "

#################### GAMEOBJECT FOR REFEREE ##################

class GameObject:
    """
    Represent the evolving state of a game. Main useful methods
    are __init__, update, display, over and end.
    """
    def __init__(self, logfilename):
        self.state = create_initial_state() # need to initialise a state

        # also keep track of some other state variables for win/draw
        # detection (score, number of turns, state history)
        self.score = {code:0 for code in PLAYER_CODES} # {'r': 0, etc.}
        self.drawmsg = ""
        self.nturns  = 0
        self.history = defaultdict(int, {self._snap(): 1})

        # and we might like to log actions!
        if logfilename is not None:
            self._logfile = open(logfilename, 'w')
            self._log("game", f"Start {GAME_NAME} game log at", time.asctime())
        else:
            self._logfile = None

    def update(self, colour, action):
        """
        Submit an action to the game for validation and application.
        If the action is not allowed, raise an InvalidActionException with
        a message describing allowed actions.
        Otherwise, apply the action to the game state.
        """
        available_actions = self._available_actions(colour)
        if action in available_actions:
            # log action
            self._log_action(colour, action)
            # Must update board with the action
            self.state = apply_action(self.state, action)

            # Must update scores as well
            for player_code in self.score:
                self.score[player_code] = get_score(self.state, NAMING_DICT[player_code])

            # detect if a draw
            self._turn_detect_draw()
        else:
            result = f"illegal action detected ({colour}): {action!r}."
            self._log("error", result)
            # NOTE: The game instance _could_ potentially be recovered, but:
            self._end_log()
            available_actions_list = '\n*   '.join(map(str, available_actions))
            raise IllegalActionException(
                f"{colour} player's action, {action!r}, is not well-formed or "
                "not available. See specification and game rules for details, "
                "or consider currently available actions:\n"
                f"*   {available_actions_list}")

    def _available_actions(self, colour):
        """
        A list of currently-available actions for a particular player
        (assists validation).
        """
        # Find all possible actions and append to list a tuple of form ("CODE", data)
        return possible_actions(self.state)

    def _turn_detect_draw(self):
        """
        Register that a turn has passed: Update turn counts and
        detect repeated game states.
        """
        self.nturns += 1
        if self.nturns >= MAX_TURNS * 3:
            self.drawmsg = "maximum number of turns reached."

        state = self._snap()
        self.history[state] += 1
        if self.history[state] >= 4:
            self.drawmsg = "game state occurred 4 times."

    def _snap(self):
        """
        Capture and return the current board state in a hashable way
        (for repeated-state checking and history recording)
        """
        return encode(self.state)

    def over(self):
        """True iff the game over (draw or win detected)."""
        return game_over(self.state) or self.nturns >= MAX_TURNS * 3 or self.history[self._snap()] >= 4

    def end(self):
        """
        Conclude the game, extracting a string describing result (win or draw)
        This method should always be called to conclude a game so that this
        class has a chance to close the logfile, too.
        If the game is not over this is a no-op.
        """
        if self.over():
            if self.drawmsg == "":
                hiscore = 0
                winner  = None
                for colour, score in self.score.items():
                    if score > hiscore:
                        winner = colour
                        hiscore = score
                result = f"winner: {NAMING_DICT[winner]}"
            else:
                result = f"draw detected: {self.drawmsg}"
            self._log("over", result)
            self._end_log()
            return result

    def display(self, debug=False):
        """Create and return a representation of board for printing."""
        template = get_template(debug)

        # Construct a list of strings to insert into template
        args = get_strings_for_template(self.state, debug)

        # Of form similar to "Red: {r} exits, Green: {g} exits, Blue: {b} exits."
        score_str = ", ".join([f"{name}: {self.score[name[0]]}" for name in PLAYER_NAMES])
        return template.format(score_str, *args)

    def _log(self, header, *messages):
        """Helper method to add a message to the logfile"""
        if self._logfile is not None:
            print(f"[{header:5s}] -", *messages, file=self._logfile, flush=True)

    def _log_action(self, colour, action):
        """Helper method to log an action to the logfile"""
        # call self._log(colour, message). Message should vary acc. to atype and aargs
        self._log(colour, log_action(self.state, action))

    def _end_log(self):
        if self._logfile is not None:
            self._logfile.close()
            self._logfile = None

class IllegalActionException(Exception):
    """If this action is illegal based on the current board state."""
