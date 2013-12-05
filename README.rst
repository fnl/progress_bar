============
progress_bar
============
----------------------------------------------
a module to display progress bars in terminals
----------------------------------------------

A simple way of providing an informative and clean progress bar on the
terminal that respects the terminal's width, has a header, and the
current %age for Python 2.6+ and 3.0+

Synopsis
========

::

                       reading names.dmp                     
    [========================79.3%===============>          ]

Installation
============

::

  pip install progress_bar

Usage
=====

Generally, to create any kind of progress bar with a default "size"
of 100 arbitrary units::

  from progress_bar import initBar

  pbar = initBar("title")
  pbar(10)  # update % to 10%
  pbar(20)  # update % to 20%
  pbar(15)  # simulate Microsoft progress effects
  
  del pbar  # move bar to final 100% and write the newline

To easily create a progress bar for reporting (reading) progress in a
filehandle that can ``tell()`` its offset::

  from progress_bar import initBarForInfile

  pbar = initBarForInfile("path")
  instream = open("path")

  for line in instream:
    pbar(instream.tell())

  del pbar

With those default arguments, the bar will be as wide as the terminal window.
Terminal window width is defined by ``termios`` using ``fcntl``,
both from the standard library.

Copyright and License
=====================

License: `Apache License v2 <https://www.apache.org/licenses/LICENSE-2.0.html>`_.
Copyright 2007-2013 Florian Leitner. All rights reserved.

