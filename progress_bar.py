"""
.. py:module:: progress_bar
   :synopsis: A progress bar for the command line.

.. moduleauthor:: Florian Leitner <florian.leitner@gmail.com>
.. License: Apache License v2
"""
import logging
import os
import stat
import sys

__author__ = "Florian Leitner <florian.leitner@gmail.com>"
### PROGRESS BAR ###


def __termios(fd):
    """Try to discover terminal width with fcntl, struct and termios."""
    #noinspection PyBroadException
    try:
        import fcntl
        import termios
        import struct
        cr = struct.unpack('hh',
                           fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
    except Exception:
        return None
    return cr


def __curses():
    """Try to discover terminal width with curses library."""
    #noinspection PyBroadException
    try:
        import curses
        curses.setupterm()
        cr = (curses.tigetnum('cols'), curses.tigetnum('lines'))
    except Exception:
        return None
    return cr


def TerminalSize():
    """Returns the terminal size as a (columns, rows) tuple."""
    cr = __termios(0) or __termios(1) or __termios(2)
    if cr:
        logging.debug("terminal size from termios")
    else:
        cr = __curses()
        if cr:
            logging.debug("terimanl size from curses.tigetnum")
    if not cr:
        #noinspection PyBroadException
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = __termios(fd)
            os.close(fd)
            logging.debug("terminal size from termios and os.ctermid")
        except Exception:
            pass
    if not cr:
        #noinspection PyBroadException
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
            logging.debug("terminal size from environment")
        except Exception:
            cr = (25, 78)
            logging.debug("terminal size using defaults")
    return int(cr[1]), int(cr[0])


class ProgressBar(object):
    """
    Create a text-based progress bar.

    Call the object to see the progress bar, which looks something like this::

        heading: [=======>        22%                  ]

    You may specify the progress bar's width, min and max values on init.

    Usage Example (filling 21% of all 100)::

    >>> bar = ProgressBar("heading", offset=2, total_width=50)
    >>> for i in range(22):
    ...     bar(i)
    ...
      heading: [=========>           21%                    ]
    """

    def __init__(self, title="", min_value=0, max_value=100, offset=0,
                 total_width=80, stream=sys.stderr):
        """
        Initialize a new progress bar.

        :param title: a title string to be placed before the actual bar
        :param min_value: the absolute starting value of the bar
                          (used to calculate the relative precentage value)
        :param max_value: the absolute end value for the bar
                          (used to calculate the relative precentage value)
        :param offset: how far the bar should be set off from the left and
                       right of the total_width of the terminal
        :param total_width: of the bar, usually set this as wide as the
                            terminal and including the offset
        """
        self.logger = logging.getLogger("ProgressBar")
        self.prog_bar = None   # stores the latest progress bar string
        self.arrow = None      # stores the latest arrow of the bar
        self.percent = ""      # stores the latest percentage value string
        if not title:
            self.title = ""
        else:
            self.title = title + ": "
        if max_value < min_value:
            max_value = min_value
        self.min = min_value
        self.max = max_value
        self.width = total_width - (2 * offset) - 2  # -2 for surr. brackets
        self.width -= len(self.title)  # 2 for the ": "
        assert self.width > 3, "progress bar size too small"
        # if not __DEBUG__, rescue what we can
        if self.width < 3 and offset > 0:
            # 3: length("100"); -1: bracket which won't be used
            offset -= (3 - self.width - 1)
        if offset < 0:
            offset = 0
        self.offset = offset
        self.stream = stream
        self.logger.debug(' '.join([
            "ProgressBar:", "min", str(self.min), "- max", str(self.max),
            "- offset", str(self.offset), "- width", str(self.width)
        ]))
        self.updateAmount(min_value)  # Build the progress bar string

    def _calculateFraction(self, amount):
        """Calculate fraction of how much has been done (done/width)."""
        done = float(amount - self.min)
        width = float(self.max - self.min)
        if width == 0.0:
            return done
        return done / width

    def _arrowCharacters(self, fraction):
        """Return the new arrow of the bar based on the fraction done."""
        size = int(round(fraction * self.width))
        return "=" * size

    def _percentString(self, fraction_done):
        """Return the largest possible string based on bar space."""
        if self.width > 5:  # [100.0%], w.o. braces!
            percent_string = "%.1f%%" % round(fraction_done * 100, 1)
        else:
            percent_string = str(int(round(fraction_done * 100)))
            if self.width > 3:  # [100%]
                percent_string += "%"
        return percent_string

    def updateAmount(self, amount=0):
        """
        Update the progress bar to the new position/amount.

        If new_amount is greater or less than max_value or min_value, set at
        intialization, respectively, it uses these values.
        """
        # ensure not over min or max and not doing the same thing twice
        if amount < self.min:
            amount = self.min
        if amount > self.max:
            amount = self.max

        fraction = self._calculateFraction(amount)
        arrow = self._arrowCharacters(fraction)
        percent = self._percentString(fraction)

        if percent == self.percent:
            # if still at the same percentage, just return the old bar
            return "%s%s%s" % (" " * self.offset, self.title, self.prog_bar)
        else:
            self.percent = percent

        if self.width < 4:
            # if the width is really small, the "bar" is only an integer
            # without most of the fancy stuff
            self.prog_bar = "%3i" % int(percent)
            return "%s%s%s" % (" " * self.offset, self.title, self.prog_bar)

        if arrow != self.arrow:
            # (re-) build the progress bar if the arrow length has changed
            self.arrow = arrow
            size = len(arrow)
            if size == 0 and fraction == 0.0:
                self.prog_bar = "[%s]" % (' ' * self.width)
            elif size == self.width:
                self.prog_bar = "[%s]" % arrow
            else:
                self.prog_bar = "[%s>%s]" % (arrow,
                                             ' ' * (self.width - size - 1))

        # place the percentage (pos) roughly centered
        pos = int(len(self.prog_bar) / 2 - len(percent) / 2)

        # slice the percentage into the bar
        if pos > 0:
            self.prog_bar = "%s%s%s" % (
                self.prog_bar[0:pos], percent, self.prog_bar[pos + len(percent):]
            )
        else:
            self.prog_bar = percent
        return "%s%s%s" % (" " * self.offset, self.title, self.prog_bar)

    def __str__(self):
        """
        Return the latest progress bar string defined by the last
        ``updateAmount()`` call.
        """
        return self.prog_bar

    def __call__(self, value):
        """
        Update the amount to value and write the bar to stream.

        Prints a carriage return first, so it will overwrite the current
        line in the stream.
        """
        self.stream.write('\r')
        self.stream.write(self.updateAmount(value))
        self.stream.flush()

    def __del__(self):
        """Add a newline to stream when deleting the bar."""
        if self.prog_bar is not None:
            self.stream.write('\n')


def InitBar(title=None, size=100, offset=2, stream=sys.stderr):
    """
    Initialize a new progess bar for a terminal with title.

    The width of the bar will be equal to the TerminalSize() - offset.

    :param title: an optional title string prefixing the bar
    :param size: the max. (update) value setting ProgressBar.max_value
    :param offset: of the bar to the left and right of the terminal
    :param stream: to print the progress bar an (default: STDERR)
    """
    width = TerminalSize()[0]
    pbar = ProgressBar(title=title, max_value=size, offset=offset,
                       total_width=width, stream=stream)
    return pbar


def InitBarForInfile(filename, offset=2, stream=sys.stderr):
    """
    Initialize a new progress bar for a terminal for reading a given
    input file (path).

    The basename of the file will be used as title.

    Example::

        ...
        progress_bar = initBarForInfile(filename)
        filehandle = open(filename)
        ...

        for line in filehandle:
            progress_bar(filehandle.tell())
            ...

        del progress_bar
        ...
    """
    size = os.stat(filename)[stat.ST_SIZE]
    title = os.path.basename(filename)
    return InitBar(title, size, offset, stream)
