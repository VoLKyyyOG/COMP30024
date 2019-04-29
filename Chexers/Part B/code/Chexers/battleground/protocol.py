"""
Helper module to implement either side of the Centrally Connected Competitive Chexers Client Control protocol (the 'C hex' protocol).

This module provides a convenient Connection class to manage a C hex connection
and MessageType flag enum to easily work with the various C hex message types.

Example usage:

    >>> from protocol import Connection, MessageType as M
    >>> server = Connection.from_address('ai.far.in.net', 6666)
    >>> server.send(M.PLAY, name="chexpiala_docious", channel="C-hive")
    >>> server.recv(M.OKAY)
    { 'mtype': <MessageType.OKAY [000000001]> }
    >>> server.recv(M.OKAY|M.GAME)
    { 'mtype': <MessageType.GAME [000001000]>
    , 'red': 'chexpiala_docious'
    , 'green': 'hexproof'
    , 'blue': 'william_chexpeare'
    }

"""

import json
import socket
from enum import Flag as FlagEnum


# Print messages while sending and receiving messages?
_NET_DEBUG = False


class MessageType(FlagEnum):
    # The different protocol message types:
    OKAY = 0b000000001
    ERRO = 0b000000010
    PLAY = 0b000000100
    GAME = 0b000001000
    INIT = 0b000010000
    TURN = 0b000100000
    ACTN = 0b001000000
    UPD8 = 0b010000000
    OVER = 0b100000000

    @staticmethod
    def any():
        """wildcard---any of the above!"""
        msgtypes = ( MessageType.OKAY | MessageType.ERRO | MessageType.PLAY
                   | MessageType.GAME | MessageType.INIT | MessageType.TURN
                   | MessageType.ACTN | MessageType.UPD8 | MessageType.OVER
                   )
        return msgtypes

    @staticmethod
    def from_name(name):
        names = { "OKAY": MessageType.OKAY, "ERRO": MessageType.ERRO
                , "PLAY": MessageType.PLAY, "GAME": MessageType.GAME
                , "INIT": MessageType.INIT, "TURN": MessageType.TURN
                , "ACTN": MessageType.ACTN, "UPD8": MessageType.UPD8
                , "OVER": MessageType.OVER
                }
        try:
            msgtype = names[name]
            return msgtype
        except KeyError:
            raise ValueError(f"Invalid flag name {name}")
   
    def __repr__(self):
        return f"<{str(self)} [{self.value:09b}]>"


class Connection:
    @staticmethod
    def from_address(host, port):
        """
        Create and return a direct TCP-based connection to another host (at 
        'host':'port') to be used with this protocol.

        Raises a ConnectingException if there is any issue establishing the 
        connection (connection refused by host, connection aborted while
        setting up connection, getaddrinfo had some error, error resolving the 
        hostname, etc.)
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, port))
        except (ConnectionRefusedError, ConnectionAbortedError, socket.gaierror,
                socket.herror) as e:
            raise ConnectingException(str(e))
        return Connection(sock)
    
    @staticmethod
    def iter_listen(host, port):
        """
        Generate connections by binding on and listening to a server socket
        on 'port' (and 'host', which should probably be "" to allow all incoming
        connections).
        """
        ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ssock.bind((host, port))
        ssock.listen()
        while True:
            sock, address = ssock.accept()
            yield Connection(sock), address
    
    def __init__(self, sock):
        """
        Avoid using this constructor directly. Prefer to use from_address or 
        iter_listen instead.
        
        If you do use the constructor, note that the Connection assumes
        ownership of the provided socket. Make sure to close the socket with the 
        disconnect() method when you are finished with this connection, and
        don't use the socket directly anymore.
        """
        self.socket  = sock
        self.socketf = sock.makefile('rb') # for line-based reading
    
    def disconnect(self):
        """
        Close this protocol and its underlying socket

        Do NOT call any other methods after this one, on this connection
        or the socket!
        """
        self.socketf.close()
        self.socket.close()

    def send(self, mtype, **margs):
        """
        Send a message of type 'mtype' with payload given by keyword arguments.
        """
        if mtype.name is None:
            raise ValueError("Unnamed MessageType {mtype} not valid for send()")
        # convert mtype to a string, e.g. 'ACTN', for sending:
        margs['mtype'] = mtype.name
        self._send(**margs)

    def recv(self, mtype=MessageType.any(), timeout=None):
        """
        Recv a message of a type in 'mtype' (default: any message type).
        Parse the message and return it as a dictionary. The type of message
        recv'd is returned through the dictionary, under the 'mtype' key.
        
        This method blocks until a message is recv'd, unless 'timeout' is 
        specified, in which case it will wait up to 'timeout' (float) seconds.

        Use '|' to combine message types to allow multiple types of messages
        to be accepted, for example, c.recv(MessageType.ACTN|MessageType.UPD8).
        """
        msg = self._recv(timeout=timeout)
        # convert mtype back to a MessageType, e.g. MessageType.ACTN:
        try:
            msg['mtype'] = MessageType.from_name(msg['mtype'])
        except ValueError:
            raise ProtocolException(f"Unknown message type {msg['mtype']}!")
        if not (mtype & msg['mtype']):
            # recvd message type was not expected!
            raise ProtocolException(f"Unexpected {msg['mtype']} message!")
        return msg

    def _send(self, **msg):
        string = json.dumps(msg, indent=None, separators=(',', ':'))
        line = f"{string}\n".encode()
        if _NET_DEBUG: print("SENDING:", repr(line))
        self.socket.sendall(line)
        if _NET_DEBUG: print("SENT!")

    def _recv(self, timeout=None):
        if _NET_DEBUG: print("RECVING...")
        self.socket.settimeout(timeout)
        try:
            line = self.socketf.readline()
        except socket.timeout:
            raise DisconnectException("Timeout exceeded! Assuming lost.")
        except ConnectionResetError as e:
            raise DisconnectException(f"Connection error! {e}")
        finally:
            self.socket.settimeout(None)
        if _NET_DEBUG: print("RECV'D:", repr(line))
        if not line:
            raise DisconnectException("Connection lost!")
        string = line.decode().strip()
        msg = json.loads(string, object_hook=_tuplify_values_hook)
        return msg


# Helper methods to get JSON arrays to decode as tuples.
# If only JSONDecoder had an 'array_hook'; we could just use 'array_hook=tuple'!
# I like this idea so much I submitted a partial patch to CPython:
# * https://bugs.python.org/issue36738
# * https://github.com/python/cpython/pull/12980
# Who knows, maybe it will be accepted and become part of Python 3.8? Well,
# probably not, but oh well, I tried!
def _tuplify_values_hook(obj):
    """A Json object's values may contain arrays: convert them!"""
    return {key: _deep_tuple(val) for key, val in obj.items()}
def _deep_tuple(item):
    """
    Convert a nested list with arbitrary structure to a nested _tuple_ instead.
    """
    if isinstance(item, list):
        # In the recursive case (item is a list), recursively deep_tuple-ify all 
        # list items, and store all items in a tuple intead.
        return tuple(_deep_tuple(i) for i in item)
    else:
        # In the base case (any items that are not lists, including some 
        # possibly deep objects like dicts, and tuples themselves), change 
        # nothing.
        return item


class ProtocolException(Exception):
    """
    For when an unexpected message is recvd, indicating that we (and the
    other party) disagree about what is meant to happen next in the protocol
    TODO: add message contents validation to protocol, using this exception,
    while sending and recving messages. That way, errors caused by e.g. missing
    message data won't pop up elsewhere on the wrong side of the network.
    """


class ConnectingException(Exception):
    """For when we have trouble establishing a connection in the first place"""


class DisconnectException(Exception):
    """For when the connection closes while we are trying to recv a message"""
