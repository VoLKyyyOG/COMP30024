"""
Driver program to instantiate Player classes
and conduct a game between them.
"""

import time

from referee.game import GameObject, IllegalActionException, PLAYER_NAMES
from referee.player import PlayerWrapper, ResourceLimitException, set_space_line
from referee.options import get_options
# from referee.game_implementation import PLAYER_NAMES

def main():
    # Parse command-line options into a namespace for use throughout this
    # program
    options = get_options()

    try:
        # Import player classes
        wrappers = [PlayerWrapper(name, getattr(options, f"player{name[0].upper()}_loc"), \
                        options) for name in PLAYER_NAMES]

        # We'll start measuring space usage from now, after all
        # library imports should be finished:
        set_space_line()

        # Play the game!
        play(options, *wrappers)

    # In case the game ends in an abnormal way, print a clean error
    # message for the user (rather than a trace).
    except IllegalActionException as e:
        info("game error", options)
        say("error: invalid action!")
        if options.verbosity > 0:
            say(e)
    except ResourceLimitException as e:
        info("game error", options)
        say("error: resource limit exceeded!")
        if options.verbosity > 0:
            say(e)

def play(options, *wrappers):
    # Set up a new game and initialise players
    # (constructing three Player classes including running their .__init__()
    # methods).
    game = GameObject(options.logfile)
    info("initialising players", options)
    all_players = wrappers
    for player in all_players:
        # NOTE: `player` here is actually a player wrapper. Your program should
        # still implement a method called `__init__()`, not one called `init()`.
        player.init()

    # Display the initial state of the game.
    info("game start", options)
    display(game, options)

    # Repeat the following until the game ends
    # (starting with Red as the current player, then alternating):
    curr_player = wrappers[0]
    # Will shift the player order so that 'next player' is at front
    shift = lambda wrappers: list(wrappers[1:]) + [wrappers[0]]

    while not game.over():
        time.sleep(options.delay)
        info(f"{curr_player.colour} player's turn", options)

        # Ask the current player for their next action (calling their .action()
        # method).
        action = curr_player.action()

        # Validate this action (or pass) and apply it to the game if it is
        # allowed. Display the resulting game state.
        game.update(curr_player.colour, action)
        display(game, options)

        # Notify all three players (including the current player) of the action
        # (or pass) (using their .update() methods).
        for player in all_players:
            player.update(curr_player.colour, action)

        # Next player's turn!
        wrappers = shift(wrappers)
        curr_player = wrappers[0]

    # After that loop, the game has ended (one way or another!)
    # Display the final result of the game to the user.
    result = game.end()
    info("game over!", options)
    say(result)

def display(game, options):
    """Helper function to display the game board (depending on options)"""
    if options.verbosity > 1:
        say("displaying game board:")
        print(game.display(debug=options.verbosity>2))
def info(message, options):
    if options.verbosity > 0 and message:
        say(f"== {message} ==")
def say(message):
    """Helper function to display a message from the referee"""
    print("*", message)


if __name__ == '__main__':
    main()
