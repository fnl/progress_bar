============
progress_bar
============
----------------------------------------------
a module to display progress bars in terminals
----------------------------------------------

A simple way of providing an informative and clean progress bar on the
terminal that *knows a terminal's current width*, has a header, works *out
of the box* when *reading files*, and always shows a relative percentage;
progress_bar works for Python 2.6+ and 3.0+

Synopsis
========

::

    file.txt: [========================79.3%===============>          ]

Installation
============

``pip install progress_bar``

Usage
=====

Generally, to create any kind of progress bar with a default "size"
of 100 arbitrary units::

  from progress_bar import InitBar

  pbar = InitBar()
  pbar(10)  # update % to 10%
  pbar(20)  # update % to 20%
  pbar(15)  # simulate a Microsoft progress bar
  
  del pbar  # move bar to final 100% and write the newline

To easily create a progress bar for reporting (reading) progress in a
filehandle that can ``tell()`` its offset::

  from progress_bar import InitBarForInfile

  pbar = InitBarForInfile("path/to/file.txt")
  instream = open("path/to/file.txt")

  for line in iter(instream.readline, ''):
    pbar(instream.tell())

  del pbar

With those default arguments, the bar will be as wide as the terminal window.
However, it will have two whitespaces on both sides of the bar to achieve a
visually more appealing display. Terminal window width is defined by
``termios`` using ``fcntl``, both from the standard library. The progress bar
will be prefixed with the *basename* of the input file ("file.txt" in the
above example).

Version History
===============

- 6: removed remaining function annotations (Py2.7; thanks to Adam Knight
  @ahknight)
- 5: fixed a few rough edges from the last update
- 4: made the bars with titles one-liners and fixed functions names
  (FunctionNames, ClassNames, methodNames, variable_names) because the PEP8
  convention of using "snake_case" for nearly all names makes no sense to me
  what-so-ever...
  Finally, fixed the documentation to reflect Sphinx standards.
- 3: fixed the version number so PEP426 issues are avoided (pip install now
  works...)
- 2: updated the readme/usage section to reflect tell() issues with Python3
- 1: initial release

Copyright and License
=====================

License: `Apache License v2 <https://www.apache.org/licenses/LICENSE-2.0.html>`_.
Copyright 2007-2014 Florian Leitner. All rights reserved.

