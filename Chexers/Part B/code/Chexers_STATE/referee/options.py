"""
Provide a command-line argument parsing function using argparse
(resulting in the following help message):

--------------------------------------------------------------------------------
usage: referee [-h] [-V] [-d [delay]] [-s [space_limit]] [-t [time_limit]]
               [-D] [-v [{0,1,2,3}]] [-l [LOGFILE]]
               red green blue

conducts a game of Chexers between three Player classes.

player package/class specifications (positional arguments):
  
  The first 3 arguments are 'package specifications'. These specify which Python
  package/module to import and search for a class named 'Player' (to instantiate
  for each player in the game). When we test your programs this will just be
  your top-level package (i.e. 'your_team_name').
  
  If you want to play games with another player class from another package (e.g.
  while you develop your player), you can use any absolute module name (as used
  with import statements, e.g. 'your_team_name.player2') or relative path (to a
  file or directory containing the Python module, e.g. 'your_team_name/player3'
  or 'your_team_name/players/player4.py').
  
  Either way, the referee will attempt to import the specified package/module
  and then load a class named 'Player'. If you want the referee to look for a
  class with some other name you can put the alternative class name after a ':'
  (e.g. 'your_team_name:DifferentPlayer').

  red                   location of Red's Player class (e.g. package name)
  green                 location of Green's Player class (e.g. package name)
  blue                  location of Blue's Player class (e.g. package name)

optional arguments:
  -h, --help            show this message
  -V, --version         show program's version number and exit
  -d [delay], --delay [delay]
                        how long (float, seconds) to wait between game turns
  -s [space_limit], --space [space_limit]
                        limit on memory space (float, MB) for each player
  -t [time_limit], --time [time_limit]
                        limit on CPU time (float, seconds) for each player
  -D, --debug           switch to printing the debug board (with coordinates)
                        (overrides -v option; equivalent to -v or -v3)
  -v [{0,1,2,3}], --verbosity [{0,1,2,3}]
                        control the level of output (not including output from
                        players). 0: no output except result; 1: commentary,
                        but no board display; 2: (default) commentary and
                        board display; 3: (equivalent to -D) larger board
                        showing coordinates.
  -l [LOGFILE], --logfile [LOGFILE]
                        if you supply this flag the referee will create a log
                        of all game actions in a text file named LOGFILE
                        (default: game.log)
--------------------------------------------------------------------------------
"""

import argparse

# Program information:
PROGRAM = "referee"
VERSION = "1.1 (released Apr 27 2019)"
DESCRIP = "conducts a game of Chexers between three Player classes."

WELCOME = f"""******************************************************************
welcome to Chexers referee version {VERSION}.
{DESCRIP}
run `python -m referee --help` for additional usage information.
******************************************************************"""

# default values (to use if flag is not provided)
# and missing values (to use if flag is provided, but with no value)

DELAY_DEFAULT = 0   # signifying no delay
DELAY_NOVALUE = 0.5 # seconds (between turns)

SPACE_LIMIT_DEFAULT = 0     # signifying no limit
SPACE_LIMIT_NOVALUE = 100.0 # MB (each)
TIME_LIMIT_DEFAULT  = 0     # signifying no limit
TIME_LIMIT_NOVALUE  = 60.0  # seconds (each)

VERBOSITY_LEVELS  = 4
VERBOSITY_DEFAULT = 2 # normal level, normal board
VERBOSITY_NOVALUE = 3 # highest level, debug board

LOGFILE_DEFAULT = None
LOGFILE_NOVALUE = "game.log"

PKG_SPEC_HELP = """
The first 3 arguments are 'package specifications'. These specify which Python
package/module to import and search for a class named 'Player' (to instantiate
for each player in the game). When we test your programs this will just be
your top-level package (i.e. 'your_team_name').

If you want to play games with another player class from another package (e.g.
while you develop your player), you can use any absolute module name (as used
with import statements, e.g. 'your_team_name.player2') or relative path (to a
file or directory containing the Python module, e.g. 'your_team_name/player3'
or 'your_team_name/players/player4.py').

Either way, the referee will attempt to import the specified package/module
and then load a class named 'Player'. If you want the referee to look for a
class with some other name you can put the alternative class name after a ':'
(e.g. 'your_team_name:DifferentPlayer').
"""

def get_options():
    """Parse and return command-line arguments."""

    parser = argparse.ArgumentParser(
        prog=PROGRAM, description=DESCRIP,
        add_help=False,       # <-- we will add it back to the optional group.
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # positional arguments used for player package specifications:
    positionals = parser.add_argument_group(
        title="player package/class specifications (positional arguments)",
        description=PKG_SPEC_HELP)
    positionals.add_argument('playerR_loc', metavar='red',
        help="location of Red's Player class (e.g. package name)",
        action=PackageSpecAction)
    positionals.add_argument('playerG_loc', metavar='green',
        help="location of Green's Player class (e.g. package name)",
        action=PackageSpecAction)
    positionals.add_argument('playerB_loc', metavar='blue',
        help="location of Blue's Player class (e.g. package name)",
        action=PackageSpecAction)
    
    # optional arguments used for configuration:
    optionals = parser.add_argument_group(title="optional arguments")
    optionals.add_argument('-h','--help',action='help',help="show this message")
    optionals.add_argument('-V','--version',action='version', version=VERSION)

    optionals.add_argument('-d', '--delay', metavar="delay",
        type=float, nargs='?',
        default=DELAY_DEFAULT,  # if the flag is not present
        const=DELAY_NOVALUE,    # if the flag is present with no value
        help="how long (float, seconds) to wait between game turns")

    optionals.add_argument('-s', '--space', metavar="space_limit",
        type=float, nargs='?',
        default=SPACE_LIMIT_DEFAULT, const=SPACE_LIMIT_NOVALUE,
        help="limit on memory space (float, MB) for each player")
    optionals.add_argument('-t', '--time', metavar="time_limit",
        type=float, nargs="?",
        default=TIME_LIMIT_DEFAULT, const=TIME_LIMIT_NOVALUE,
        help="limit on CPU time (float, seconds) for each player")

    optionals.add_argument('-D', '--debug',
        action="store_true",
        help="switch to printing the debug board (with coordinates) "
            "(overrides -v option; equivalent to -v or -v3)")
    optionals.add_argument('-v', '--verbosity',
        type=int, choices=range(0, VERBOSITY_LEVELS), nargs='?', 
        default=VERBOSITY_DEFAULT, const=VERBOSITY_NOVALUE,
        help="control the level of output (not including output from "
            "players). 0: no output except result; 1: commentary, but no"
            " board display; 2: (default) commentary and board display; "
            "3: (equivalent to -D) larger board showing coordinates.")

    optionals.add_argument('-l', '--logfile', 
        type=str, nargs='?',
        default=LOGFILE_DEFAULT, const=LOGFILE_NOVALUE, metavar="LOGFILE",
        help="if you supply this flag the referee will create a log of all "
        "game actions in a text file named %(metavar)s (default: %(const)s)")

    args = parser.parse_args()

    # resolving any conflicts:
    if args.debug:
        args.verbosity = 3
        del args.debug

    # done!
    if args.verbosity > 0:
        print(WELCOME)
    return args

class PackageSpecAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        pkg_spec = values
        
        # detect alternative class:
        if ":" in pkg_spec:
            pkg, cls = pkg_spec.split(':', maxsplit=1)
        else:
            pkg = pkg_spec
            cls = "Player"

        # try to convert path to module name
        mod = pkg.strip("/").replace("/", ".")
        if mod.endswith(".py"): # NOTE: Assumes submodule is not named `py`.
            mod = mod[:-3]

        # save the result in the arguments namespace as a tuple
        setattr(namespace, self.dest, (mod, cls))
    