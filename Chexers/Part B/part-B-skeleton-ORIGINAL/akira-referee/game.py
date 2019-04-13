"""
Provide a class to maintain the state of an evolving game
of Chexers, including validation of actions, detection of draws,
and optionally maintaining a game log.

NOTE: This board representation is designed to be used intenrally by the referee
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

# Game-specific constants:

_STARTING_HEXES = {
    'r': {(-3,3), (-3,2), (-3,1), (-3,0)},
    'g': {(0,-3), (1,-3), (2,-3), (3,-3)},
    'b': {(3, 0), (2, 1), (1, 2), (0, 3)},
}
_FINISHING_HEXES = {
    'r': {(3,-3), (3,-2), (3,-1), (3,0)},
    'g': {(-3,3), (-2,3), (-1,3), (0,3)},
    'b': {(-3,0),(-2,-1),(-1,-2),(0,-3)},
}
_ADJACENT_STEPS = [(-1,+0),(+0,-1),(+1,-1),(+1,+0),(+0,+1),(-1,+1)]
_MAX_TURNS = 256 # per player


# Display-specific constants:

_COL_NAME  = {
    'r': 'Red',
    'g': 'Green',
    'b': 'Blue',
}
if sys.stdout.isatty():
    # Yay! We can use colour
    _DISPLAY = { # something 5 characters wide for each colour:
        'r': " \033[1m(\033[91mR\033[0m\033[1m)\033[0m ",
        'g': " \033[1m(\033[92mG\033[0m\033[1m)\033[0m ",
        'b': " \033[1m(\033[94mB\033[0m\033[1m)\033[0m ",
        ' ': "     "
    }
else:
    _DISPLAY = { # something 5 characters wide for each colour:
        'r': "  R  ", 
        'g': "  G  ",
        'b': "  B  ",
        ' ': "     "
    }

_TEMPLATE_NORMAL = """*   scores: {0}
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
_TEMPLATE_DEBUG = """*   scores: {0}
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


class Chexers:
    """
    Represent the evolving state of a game of Chexers. Main useful methods
    are __init__, update, display, over and end.
    """
    def __init__(self, logfilename):
        # initialise game board state:
        ran = range(-3, +3+1)
        self.hexes = {(q,r) for q in ran for r in ran if -q-r in ran}
        self.board = {qr: ' ' for qr in self.hexes}
        for colour in "rgb":
            for qr in _STARTING_HEXES[colour]:
                self.board[qr] = colour
        
        # also keep track of some other state variables for win/draw
        # detection (score, number of turns, state history)
        self.score = {'r': 0, 'g': 0, 'b': 0}
        self.drawmsg = ""
        self.nturns  = 0
        self.history = defaultdict(int, {self._snap(): 1})

        # and we might like to log actions!
        if logfilename is not None:
            self._logfile = open(logfilename, 'w')
            self._log("game", "Start Chexers game log at", time.asctime())
        else:
            self._logfile = None
        
    def update(self, colour, action):
        """
        Submit an action to the game for validation and application.
        If the action is not allowed, raise an InvalidActionException with
        a message describing allowed actions.
        Otherwise, apply the action to the game state.
        """
        col = colour[0]
        available_actions = self._available_actions(col)
        if action in available_actions:
            atype, aargs = action
            if atype == "MOVE":
                qr_a, qr_b = aargs
                self.board[qr_a] = ' '
                self.board[qr_b] = col
            elif atype == "JUMP":
                qr_a, qr_b = (q_a, r_a), (q_b, r_b) = aargs
                qr_c = (q_a+q_b)//2, (r_a+r_b)//2
                self.board[qr_a] = ' '
                self.board[qr_b] = col
                self.board[qr_c] = col
            elif atype == "EXIT":
                qr = aargs
                self.board[qr] = ' '
                self.score[col] += 1
            else: # atype == "PASS":
                pass
            self._log_action(colour, action)
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
        available_actions = []
        for qr in self.hexes:
            if self.board[qr] == colour:
                if qr in _FINISHING_HEXES[colour]:
                    available_actions.append(("EXIT", qr))
                q, r = qr
                for dq, dr in _ADJACENT_STEPS:
                    for i, atype in [(1, "MOVE"), (2, "JUMP")]:
                        tqr = q+dq*i, r+dr*i
                        if tqr in self.hexes:
                            if self.board[tqr] == ' ':
                                available_actions.append((atype, (qr, tqr)))
                                break
        if not available_actions:
            available_actions.append(("PASS", None))
        return available_actions
    def _turn_detect_draw(self):
        """
        Register that a turn has passed: Update turn counts and 
        detect repeated game states.
        """
        self.nturns += 1
        if self.nturns >= _MAX_TURNS * 3:
            self.drawmsg = "maximum number of turns reached."
        
        state = self._snap()
        self.history[state] += 1
        if self.history[state] >= 4:
            self.drawmsg = "game state occurred 4 times."
    def _snap(self):
        """
        Capture the current board state in a hashable way
        (for repeated-state checking)
        """
        return (
            # same colour pieces in the same positions
            tuple((qr,p) for qr,p in self.board.items() if p in "rgb"),
            # on the same player's turn
            self.nturns % 3,
        )

    def over(self):
        """True iff the game over (draw or win detected)."""
        return (max(self.score.values()) >= 4) or (self.drawmsg != "")
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
                result = f"winner: {_COL_NAME[winner]}"
            else:
                result = f"draw detected: {self.drawmsg}"
            self._log("over", result)
            self._end_log()
            return result

    def display(self, debug=False):
        """Create and return a representation of board for printing."""
        if debug:
            template = _TEMPLATE_DEBUG
        else:
            template = _TEMPLATE_NORMAL
        cells = []
        ran = range(-3, +3+1)
        for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
            cells.append(_DISPLAY[self.board[qr]])
        score_template = "Red: {r} exits, Green: {g} exits, Blue: {b} exits."
        score_str = score_template.format(**self.score)
        return template.format(score_str, *cells)

    def _log(self, header, *messages):
        """Helper method to add a message to the logfile"""
        if self._logfile is not None:
            print(f"[{header:5s}] -", *messages, file=self._logfile, flush=True)
    def _log_action(self, colour, action):
        """Helper method to log an action to the logfile"""
        atype, aargs = action
        if atype in {"JUMP", "MOVE"}:
            self._log(colour, f"{atype} from {aargs[0]} to {aargs[1]}.")
        elif atype == "EXIT":
            self._log(colour, f"{atype} from {aargs}.")
        else: #atype == "PASS":
            self._log(colour, f"{atype}.")
    def _end_log(self):
        if self._logfile is not None:
            self._logfile.close()
            self._logfile = None

class IllegalActionException(Exception):
    """If this action is illegal based on the current board state."""
