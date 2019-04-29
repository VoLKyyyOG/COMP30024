"""
Client program to instantiate a player class and 
conduct a game of Chexers through the online battleground
"""

from referee.log import StarLog
from referee.game import Chexers
from referee.player import PlayerWrapper, set_space_line

from battleground.options import get_options
from battleground.protocol import Connection as Server, ConnectingException 
from battleground.protocol import MessageType as M, ProtocolException
from battleground.protocol import DisconnectException


def main():
    # Parse command-line options into a namespace for use throughout this
    # program
    options = get_options()

    # Create a star-log for controlling the format of output from within this
    # program
    out = StarLog(options.verbosity)
    out.comment("all messages printed by the client after this begin with a *")
    out.comment("(any other lines of output must be from your Player class).")
    out.comment()
    
    try:
        # Import player classes
        player = PlayerWrapper("your player", options.player_loc, options, out)
    
        # We'll start measuring space usage from now, after all
        # library imports should be finished:
        set_space_line()

        # Play the game, catching any errors and displaying them to the 
        # user:
        connect_and_play(player, options, out)

    except KeyboardInterrupt:
        print() # (end the line)
        out.comment("bye!")
    except ConnectingException as e:
        out.print("error connecting to server")
        out.comment(e)
    except DisconnectException:
        out.print("connection lost")
    except ProtocolException as e:
        out.print("protocol error!")
        out.comment(e)
    # If it's another kind of error then it might be coming from the player
    # itself? Then, a traceback will be more helpful.


def connect_and_play(player, options, out):
    # SET UP SERVER CONNECTION
    out.section("connecting to battleground")
    # attempt to connect to the server...
    out.comment("attempting to connect to the server...")
    server = Server.from_address(options.host, options.port)
    out.comment("connection established!")
    
    # FIND A GAME
    # we would like to play a game!
    if options.channel:
        channel_str = f"channel '{options.channel}'"
    else:
        channel_str = "open channel"
    out.comment(f"submitting game request as '{options.name}' in {channel_str}...")
    server.send(M.PLAY, name=options.name, channel=options.channel)
    server.recv(M.OKAY)
    out.comment("game request submitted.")
    # wait for the server to find a game for us...
    out.comment(f"waiting for opponents in {channel_str}...")
    out.comment("(press ^C to stop waiting)")
    # (wait through some OKAY-OKAY msg exchanges until a GAME message comes---
    # the server is asking if we are still here waiting, or have disconnected)
    gamemsg = server.recv(M.OKAY|M.GAME)
    while gamemsg['mtype'] is not M.GAME:
        server.send(M.OKAY)
        gamemsg = server.recv(M.OKAY|M.GAME)
    # when we get a game message, it's time to play!
    out.comment("opponents found!")
    out.comment("red player:  ", gamemsg['red'])
    out.comment("green player:", gamemsg['green'])
    out.comment("blue player: ", gamemsg['blue'])

    # PLAY THE GAME
    # Set up a new Chexers game and initialise our player.
    game = Chexers(logfilename=options.logfile, debugboard=options.verbosity>2)

    out.section("initialising player")
    out.comment("waiting for colour assignment...")
    initmsg = server.recv(M.INIT|M.ERRO)
    if initmsg['mtype'] is M.ERRO:
        erromsg = initmsg
        out.section("connection error")
        out.print(erromsg['reason'])
        return
    out.comment("playing as", initmsg['colour'], pad=1)
    out.comment("initialising your player class...")
    player.init(initmsg['colour'])
    out.comment("ready to play!")
    server.send(M.OKAY)
    
    players = format_players(gamemsg, player.colour)

    # Display the initial state of the game.
    out.section("game start", clear=True)
    out.comment("displaying game info:")
    out.comments(players, pad=1)
    out.comments(game, pad=1)

    # Now wait for messages from the sever and respond accordingly:
    while True:
        msg = server.recv(M.TURN|M.UPD8|M.OVER|M.ERRO)
        if msg['mtype'] is M.TURN:
            # it's our turn!
            out.section("your turn!", clear=True)
            out.comment("displaying game info:")
            out.comments(players, pad=1)
            out.comments(game, pad=1)
            
            # decide on action and submit it to server
            action = player.action()
            server.send(M.ACTN, action=action)

        elif msg['mtype'] is M.UPD8:
            # someone made a move!
            colour = msg['colour']
            action = msg['action']
            # update our local state,
            out.section("receiving update", clear=True)
            game.update(colour, action)
            out.comment("displaying game info:")
            out.comments(players, pad=1)
            out.comments(game, pad=1)
            player.update(colour, action)
            # then notify server we are ready to continue:
            server.send(M.OKAY)
        
        elif msg['mtype'] is M.OVER:
            # the game ended! either legitmately or through some
            # game error (e.g. non-allowed move by us or opponent)
            out.section("game over!")
            out.print(msg['result'])
            break
        
        elif msg['mtype'] is M.ERRO:
            out.section("connection error")
            out.print(msg['reason'])
            break


def format_players(gamemsg, your_colour):
    players = []
    for colour, name in gamemsg.items():
        if colour == 'mtype':
            continue # not a colour!
        if colour == your_colour:
            prefix = "you -> " + colour
        else:
            prefix = colour
        players.append(f"{prefix:>12} player: {name}")
    return '\n'.join(players)


if __name__ == '__main__':
    main()
