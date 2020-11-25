.. image:: http://www.repostatus.org/badges/latest/wip.svg
    :target: http://www.repostatus.org/#wip
    :alt: Project Status: WIP — Initial development is in progress, but there
          has not yet been a stable, usable release suitable for the public.

.. image:: https://github.com/jwodder/ttyrec2video/workflows/Test/badge.svg?branch=master
    :target: https://github.com/jwodder/ttyrec2video/actions?workflow=Test
    :alt: CI Status

.. image:: https://codecov.io/gh/jwodder/ttyrec2video/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/ttyrec2video

.. image:: https://img.shields.io/github/license/jwodder/ttyrec2video.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
    :target: https://saythanks.io/to/jwodder

`GitHub <https://github.com/jwodder/ttyrec2video>`_
| `Issues <https://github.com/jwodder/ttyrec2video/issues>`_

``ttyrec2video`` converts `ttyrec <https://en.wikipedia.org/wiki/Ttyrec>`_
files (recordings of terminal sessions, including timing data) to video files
(MP4, WMV, and whatever other formats `imageio's ffmpeg writer
<http://imageio.readthedocs.io/en/latest/format_ffmpeg.html>`_ supports).  You
may be familiar with ttyrecs from their use in recording NetHack games on
`nethack.alt.org <https://alt.org/nethack/>`_.


Installation
============
``ttyrec2video`` requires Python 3.5 or higher to run and `pip
<https://pip.pypa.io>`_ 19.0 or higher to install.  You can install
``ttyrec2video`` and its dependencies by running::

    python3 -m pip install git+https://github.com/jwodder/ttyrec2video.git

Installing inside a `virtual environment
<http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ is recommended.

Note that ``ttyrec2video`` uses `imageio <http://imageio.github.io>`_, which in
turn needs the `ffmpeg <https://ffmpeg.org>`_ program in order to create
videos.  If you don't have a suitable version of ffmpeg already installed, one
will be downloaded for the program to use instead.


Usage
=====

::

    ttyrec2video [<options>] <ttyrec>[.gz|.bz2] [<outfile>]

``<ttyrec>`` may be either a path to a local ttyrec file or an HTTP(S) URL
pointing to a remote ttyrec.  Files compressed with gzip or bzip2 will be
uncompressed automatically.

If no output filename is supplied, the resulting video is written to the input
filepath/URL basename with its extension changed to "``.mp4``."


Options
-------

- ``-E <encoding>``, ``--encoding <encoding>`` — Specify the character encoding
  to use for reading the ttyrec file's text; defaults to UTF-8

- ``--font-file <TTF file>`` — Specify the path to a TrueType font (``.ttf``)
  file containing the font to use for rendering normal (non-bold) text.  The
  font is assumed to be monospaced.  The default is to use the `Ubuntu
  Monospace font <http://font.ubuntu.com>`_.

- ``--bold-font-file <TTF file>`` — Specify the path to a TrueType font
  (``.ttf``) file containing the font to use for rendering bold text.  The font
  is assumed to be monospaced.  The default is to use the bold `Ubuntu
  Monospace font <http://font.ubuntu.com>`_.

- ``--font-size <int>`` — Set the font size (in points) of rendered text;
  defaults to 16

- ``--fps <int>`` — Set the FPS (frames per second) rate of the output video;
  defaults to 12

- ``--ibm`` — Synonym for "``--encoding cp437``" (`CP437
  <https://en.wikipedia.org/wiki/Code_page_437>`_ is the character encoding
  used by NetHack's `IBMgraphics <https://nethackwiki.com/wiki/IBMgraphics>`_
  option)

- ``--info`` — Instead of converting the ttyrec file to a video, output the
  ttyrec's total duration and number of screen updates as a JSON object

- ``--info-all`` — Like ``--info``, but also include a list of the time & byte
  offsets of each screen update

- ``--size <columns> <lines>`` — Set the dimensions of the terminal screen on
  which the ttyrec was recorded; defaults to 80×24


Licenses
========
The source code for ``ttyrec2video`` is licensed under the `MIT license
<https://opensource.org/licenses/MIT>`_.

``ttyrec2video`` contains a bundled copy of the `Ubuntu Monospace font
<http://font.ubuntu.com>`_, regular and bold weight, version 0.83, copyright
2010, 2011 Canonical Ltd, licensed under the `Ubuntu Font Licence, Version 1.0
<https://launchpad.net/ubuntu-font-licence>`_.
