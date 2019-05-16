"""
Provide a wrapper for Player classes to handle tedious details like
timing, measuring space usage, reporting which method is currently
being executed, etc.
"""

import gc
import time
import importlib

class PlayerWrapper:
    """
    Wraps a real Player class, providing essentially the same interface:
    * Wrapper constructor attempts to import the Player class by name.
    * `.init()` method constructs the Player instance (calling `.__init__()`)
    * `.action()` and `.update()` methods just delegate to the real Player's
      methods of the same name.
    Each method enforces resource limits on the real Player's computation.
    """
    def __init__(self, name, player_loc, options, out):
        self.out  = out
        self.name = name

        # create some context managers for resource limiting
        self.timer = _CountdownTimer(options.time, self.name)
        self.space = _MemoryWatcher(options.space)

        # import the Player class from given package
        player_pkg, player_cls = player_loc
        self.out.comment(f"importing {self.name}'s player class '{player_cls}' "
            f"from package '{player_pkg}'")
        self.Player = _load_player_class(player_pkg, player_cls)

    def init(self, colour):
        self.colour = colour
        player_cls = str(self.Player).strip('<class >')
        self.out.comment(f"initialising {self.colour} player as a {player_cls}")
        with self.space, self.timer:
            # construct/initialise the player class
            self.player = self.Player(colour)
        self.comment_if(self.timer.status(), pad=1)
        self.comment_if(self.space.status(), pad=1)

    def action(self):
        self.out.comment(f"asking {self.name} for next action...")
        with self.space, self.timer:
            # ask the real player
            action = self.player.action()
        self.out.comment(f"{self.name} returned action: {action!r}", pad=1)
        self.comment_if(self.timer.status(), pad=1)
        self.comment_if(self.space.status(), pad=1)
        # give back the result
        return action

    def update(self, colour, action):
        self.out.comment(f"updating {self.name} with {colour}'s action {action}"
            "...")
        with self.space, self.timer:
            # forward to the real player
            self.player.update(colour, action)
        self.comment_if(self.timer.status(), pad=1)
        self.comment_if(self.space.status(), pad=1)

    def comment_if(self, message, **kwargs):
        if message:
            self.out.comment(message, **kwargs)

def _load_player_class(package_name, class_name):
    """
    Load a Player class given the name of a package.
    """
    module = importlib.import_module(package_name)
    player_class = getattr(module, class_name)
    return player_class


# RESOURCE MANAGEMENT

class ResourceLimitException(Exception):
    """For when players exceed specified time / space limits."""


class _CountdownTimer:
    """
    Reusable context manager for timing specific sections of code

    * measures CPU time, not wall-clock time
    * unless time_limit is 0, throws an exception upon exiting the context after
      the allocated time has passed
    """
    def __init__(self, time_limit, name):
        """
        Create a new countdown timer with time limit `limit`, in seconds
        (0 for unlimited time)
        """
        self.name  = name
        self.limit = time_limit
        self.clock = 0
        self._status = ""
    def _set_status(self, status):
        self._status = status
    def status(self):
        return self._status

    def __enter__(self):
        # clean up memory off the clock
        gc.collect()
        # then start timing
        self.start = time.process_time()
        return self # unused

    def __exit__(self, exc_type, exc_val, exc_tb):
        # accumulate elapsed time since __enter__
        elapsed = time.process_time() - self.start
        self.clock += elapsed
        self._set_status(f"time:  +{elapsed:6.3f}s  (just elapsed)  "
            f"{self.clock:7.3f}s  (game total)")

        # if we are limited, let's hope we aren't out of time!
        if self.limit and self.clock > self.limit:
            raise ResourceLimitException(f"{self.name} exceeded available time")

class _MemoryWatcher:
    """
    Context manager for clearing memory before and measuring memory usage
    after using a specific section of code.

    * works by parsing procfs; only available on linux.
    * unless the limit is set to 0, throws an exception upon exiting the
      context if the memory limit has been breached
    """
    def __init__(self, space_limit):
        self.limit = space_limit
        self._status = ""
    def _set_status(self, status):
        self._status = status
    def status(self):
        return self._status

    def __enter__(self):
        return self # unused
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Check up on the current and peak space usage of the process, printing
        stats and ensuring that peak usage is not exceeding limits
        """
        if _SPACE_ENABLED:
            curr_usage, peak_usage = _get_space_usage()

            # adjust measurements to reflect usage of players and referee, not
            # the Python interpreter itself
            curr_usage -= _DEFAULT_MEM_USAGE
            peak_usage -= _DEFAULT_MEM_USAGE

            self._set_status(f"space: {curr_usage:7.3f}MB (current usage) "
                f"{peak_usage:7.3f}MB (max usage) (shared)")

            # if we are limited, let's hope we are not out of space!
            # triple the limit because space usage is shared
            if self.limit and peak_usage > 3 * self.limit:
                raise ResourceLimitException("players exceeded shared space "
                    "limit")

def _get_space_usage():
    """
    Find the current and peak Virtual Memory usage of the current process, in MB
    """
    # on linux, we can find the memory usage of our program we are looking for
    # inside /proc/self/status (specifically, fields VmSize and VmPeak)
    with open("/proc/self/status") as proc_status:
        for line in proc_status:
            if 'VmSize:' in line:
                curr_usage = int(line.split()[1]) / 1024 # kB -> MB
            elif 'VmPeak:' in line:
                peak_usage = int(line.split()[1]) / 1024 # kB -> MB
    return curr_usage, peak_usage

_DEFAULT_MEM_USAGE = 0
_SPACE_ENABLED = False
def set_space_line():
    """
    by default, the python interpreter uses a significant amount of space
    measure this first to later subtract from all measurements
    """
    global _SPACE_ENABLED, _DEFAULT_MEM_USAGE

    try:
        _DEFAULT_MEM_USAGE, _ = _get_space_usage()
        _SPACE_ENABLED = True
    except:
        # this also gives us a chance to detect if our space-measuring method
        # will work on this platform, and notify the user if not.
        print("* NOTE: unable to measure memory usage on this platform "
            "(try dimefox)")
        _SPACE_ENABLED = False
