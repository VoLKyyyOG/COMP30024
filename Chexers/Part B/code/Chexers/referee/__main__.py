"""
Driver program to instantiate three Player classes
and conduct a game of Chexers between them.
"""

import time

from referee.log import StarLog
from referee.game import Chexers, IllegalActionException
from referee.player import PlayerWrapper, ResourceLimitException, set_space_line
from referee.options import get_options

def main():
    # Parse command-line options into a namespace for use throughout this
    # program
    options = get_options()

    # Create a star-log for controlling the format of output from within this
    # program
    out = StarLog(level=options.verbosity, star="*")
    out.comment("all messages printed by the referee after this begin with a *")
    out.comment("(any other lines of output must be from your Player classes).")
    out.comment()

    try:
        # Import player classes
        p_R = PlayerWrapper('red player',   options.playerR_loc, options, out)
        p_G = PlayerWrapper('green player', options.playerG_loc, options, out)
        p_B = PlayerWrapper('blue player',  options.playerB_loc, options, out)

        # We'll start measuring space usage from now, after all
        # library imports should be finished:
        set_space_line()

        # Play the game!
        play([p_R, p_G, p_B], options, out)

    # In case the game ends in an abnormal way, print a clean error
    # message for the user (rather than a trace).
    except KeyboardInterrupt:
        print() # (end the line)
        out.comment("bye!")
    except IllegalActionException as e:
        out.section("game error")
        out.print("error: invalid action!")
        out.comment(e)
    except ResourceLimitException as e:
        out.section("game error")
        out.print("error: resource limit exceeded!")
        out.comment(e)
    chosen = input("\n\n\nGAME OVER - Debug chosen player (r,g,b) >> ")[0]
    if chosen == 'r':
        player = p_R.player
    elif chosen == 'g':
        player = p_G.player
    elif chosen == 'b':
        player = p_B.player
    else:
        return
    player.debug()
    # If it's another kind of error then it might be coming from the player
    # itself? Then, a traceback will be more helpful.

def play(players, options, out):
    # Set up a new Chexers game and initialise a Red, Green and Blue player
    # (constructing three Player classes including running their .__init__()
    # methods).
    game = Chexers(logfilename=options.logfile, debugboard=options.verbosity>2)
    out.section("initialising players")
    for player, colour in zip(players, ['red', 'green', 'blue']):
        # NOTE: `player` here is actually a player wrapper. Your program should
        # still implement a method called `__init__()`, not one called `init()`.
        player.init(colour)

    # Display the initial state of the game.
    out.section("game start")
    out.comment("displaying game info:")
    out.comments(game, pad=1)

    # Repeat the following until the game ends
    # (starting with Red as the current player, then alternating):
    curr_player, next_player, prev_player = players
    while not game.over():
        time.sleep(options.delay)
        out.section(f"{curr_player.name}'s turn")

        # Ask the current player for their next action (calling their .action()
        # method).
        action = curr_player.action()

        # Validate this action (or pass) and apply it to the game if it is
        # allowed. Display the resulting game state.
        game.update(curr_player.colour, action)
        out.comment("displaying game info:")
        out.comments(game, pad=1)

        # Notify all three players (including the current player) of the action
        # (or pass) (using their .update() methods).
        for player in players:
            player.update(curr_player.colour, action)

        # Next player's turn!
        curr_player,next_player,prev_player=next_player,prev_player,curr_player

    # After that loop, the game has ended (one way or another!)
    # Display the final result of the game to the user.
    result = game.end()
    out.section("game over!")
    out.print(result)

if __name__ == '__main__':
    main()
