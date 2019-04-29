"""
Helper module, simplifying configurable-verbosity logging
with uniform formatting accross multiple parts of a program
"""

import sys

if sys.stdout.isatty():
    _CLEAR = "\033[H\033[J"
else:
    _CLEAR = "\033[H\033[J"

class StarLog:
    def __init__(self, level=1, file=sys.stdout, time=None,
                star='*', pad='  ', title="**"):
        self.kwargs = {"file": file, "flush": True}
        self.level = level
        self.timef = time
        self.star  = star
        self.pad   = pad
        self.title = title

    def clear(self):
        print(_CLEAR, end="", **self.kwargs)
    def print(self, *args, pad=0, **kwargs):
        """print, no matter verbosity level"""
        print(self._start(pad), *args, **kwargs, **self.kwargs)
    def comment(self, *args, pad=0, **kwargs):
        """running commentary and info (if verbosity level 1 or higher)"""
        if self.level >= 1:
            print(self._start(pad), *args, **kwargs, **self.kwargs)
    def section(self, *args, pad=0, clear=False, **kwargs):
        """begin a new section of output (same level as a comment)"""
        if self.level >= 1:
            new_args = [self.title, *args, self.title]
            if clear:
                self.clear()
            print(self._start(pad), *new_args, **kwargs, **self.kwargs)
    def debug(self, *args, pad=0, **kwargs):
        """detailed debugging information (if verbosity level 2 or higher)"""
        if self.level >= 2:
            print(self._start(pad), *args, **kwargs, **self.kwargs)
    # for multi-line:
    def comments(self, comment, pad=0, **kwargs):
        """comment, for multi-line strings"""
        if self.level >= 1:
            for line in str(comment).split('\n'):
                print(self._start(pad), line, **kwargs, **self.kwargs)
    def _start(self, pad):
        start = self.star + self.pad*pad
        if self.timef is not None:
            start += f" [{self.timef()}]"
        return start

