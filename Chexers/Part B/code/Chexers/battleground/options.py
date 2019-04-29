"""
Provide a command-line argument parsing function using argparse
(resulting in the following help message):

--------------------------------------------------------------------------------
usage: battleground [-h] [-V] [-H HOST] [-P PORT] [-D] [-v [{0,1,2,3}]]
                    [-l [LOGFILE]]
                    player name [channel]

play Chexers with your Player class on the online battleground

player package/class specifications (positional arguments):
  player                location of your Player class (e.g. package name)
  name                  identify your player on the battleground server (e.g.
                        team name or player name)
  channel               restrict matchmaking to players specifying the same
                        channel (optional; leave blank to play against anyone)

optional arguments:
  -h, --help            show this message
  -V, --version         show program's version number and exit
  -H HOST, --host HOST  address of server (leave blank for default)
  -P PORT, --port PORT  port to contact server on (leave blank for default)
  -D, --debug           switch to printing the debug board (with coordinates)
                        (overrides -v option; equivalent to -v or -v3)
  -v [{0,1,2,3}], --verbosity [{0,1,2,3}]
                        control the level of output (not including output from
                        player). 0: no output except result; 1: commentary,
                        but no board display; 2: (default) commentary and
                        board display; 3: (equivalent to -D) larger board
                        showing coordinates.
  -l [LOGFILE], --logfile [LOGFILE]
                        if you supply this flag the client will create a log
                        of all game actions in a text file named LOGFILE
                        (default: battle.log)
--------------------------------------------------------------------------------
"""

import argparse

# Program information:
PROGRAM = "battleground"
VERSION = "1.0 (released Apr 27 2019)"
DESCRIP = "play Chexers with your Player class on the online battleground"

WELCOME = f"""******************************************************************
welcome to battleground client version {VERSION}.
{DESCRIP}
run `python -m battleground -h` for additional usage information.
******************************************************************"""

# default values (to use if flag is not provided)
# and missing values (to use if flag is provided, but with no value)

PORT_DEFAULT = 6666 # chexit
HOST_DEFAULT = 'ai.far.in.net'

CHANNEL_DEFAULT  = ''

VERBOSITY_LEVELS  = 4
VERBOSITY_DEFAULT = 2 # normal level, normal board
VERBOSITY_NOVALUE = 3 # highest level, debug board

LOGFILE_DEFAULT = None
LOGFILE_NOVALUE = "battle.log"

def get_options():
    """

    positional arguments:
      player_module  full name of module containing Player class
      player_name    team name or name of Player (no spaces)
      game_key       only play games against players with the same key (leave it
                     blank to play against anyone)

    optional arguments:
      -h, --help     show this help message and exit
      --host HOST    name of referee server to connect to
      --port PORT    port to contact the referee server on
    ---------------------
    """
    """Parse and return command-line arguments."""

    parser = argparse.ArgumentParser(
        prog=PROGRAM, description=DESCRIP,
        add_help=False,       # <-- we will add it back to the optional group.
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # positional arguments used for player package specifications:
    positionals = parser.add_argument_group(
        title="player package/class specifications (positional arguments)")
    positionals.add_argument('player_loc', metavar='player',
        help="location of your Player class (e.g. package name)",
        action=PackageSpecAction)
    
    positionals.add_argument('name',
        help="identify your player on the battleground server (e.g. team name "
             "or player name)")
    positionals.add_argument('channel', default=CHANNEL_DEFAULT, nargs="?",
            help="restrict matchmaking to players specifying the same channel "
                "(optional; leave blank to play against anyone)")

    # optional arguments used for configuration:
    optionals = parser.add_argument_group(title="optional arguments")
    optionals.add_argument('-h','--help',action='help',help="show this message")
    optionals.add_argument('-V','--version',action='version', version=VERSION)

    optionals.add_argument('-H', '--host', type=str, default=HOST_DEFAULT,
        help="address of server (leave blank for default)")
    optionals.add_argument('-P', '--port', type=int, default=PORT_DEFAULT,
        help="port to contact server on (leave blank for default)")

    optionals.add_argument('-D', '--debug',
        action="store_true",
        help="switch to printing the debug board (with coordinates) "
            "(overrides -v option; equivalent to -v or -v3)")
    optionals.add_argument('-v', '--verbosity',
        type=int, choices=range(0, VERBOSITY_LEVELS), nargs='?', 
        default=VERBOSITY_DEFAULT, const=VERBOSITY_NOVALUE,
        help="control the level of output (not including output from "
            "player). 0: no output except result; 1: commentary, but no "
            "board display; 2: (default) commentary and board display; "
            "3: (equivalent to -D) larger board showing coordinates.")

    optionals.add_argument('-l', '--logfile', metavar="LOGFILE",
        type=str, nargs='?', default=LOGFILE_DEFAULT, const=LOGFILE_NOVALUE,
        help="if you supply this flag the client will create a log of all "
        "game actions in a text file named %(metavar)s (default: %(const)s)")

    args = parser.parse_args()

    # resolving any conflicts:
    if args.debug:
        args.verbosity = 3
        del args.debug

    # disable delay, space limiting, time limiting for networked games:
    args.delay = 0
    args.time  = 0
    args.space = 0

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
    