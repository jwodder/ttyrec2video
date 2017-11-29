.. image:: http://www.repostatus.org/badges/latest/wip.svg
    :target: http://www.repostatus.org/#wip
    :alt: Project Status: WIP — Initial development is in progress, but there
          has not yet been a stable, usable release suitable for the public.

.. image:: https://img.shields.io/github/license/jwodder/ttyrec2video.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/ttyrec2video>`_
| `Issues <https://github.com/jwodder/ttyrec2video/issues>`_

``ttyrec2video`` converts `ttyrec <https://en.wikipedia.org/wiki/Ttyrec>`_
files (recordings of terminal sessions, including timing data) to MP4 videos
(and, later, possibly other formats???).  You may be familiar with ttyrecs from
their use in recording NetHack games on `nethack.alt.org
<https://alt.org/nethack/>`_.


Installation
============
``ttyrec2video`` requires Python 3.4 or higher to run and `pip
<https://pip.pypa.io>`_ 6.0+, `Setuptools <https://setuptools.readthedocs.io>`_
30.3.0+, & `wheel <https://pypi.python.org/pypi/wheel>`_ to install.  `Once you
have those
<https://packaging.python.org/tutorials/installing-packages/#install-pip-setuptools-and-wheel>`_,
you can install ``ttyrec2video`` and its dependencies by running::

    python3 -m pip install git+https://github.com/jwodder/ttyrec2video.git

Installing inside a `virtual environment
<http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ is recommended.


Usage
=====

::

    ttyrec2video --font-file <TTF file>
                 --bold-font-file <TTF file>
                 [--font-size <int>]
                 [-E|--encoding <encoding>]
                 [--ibm]
                 [--fps <int>]
                 [-o|--outfile <filepath>]
                 [--size <columns> <lines>]
                 <ttyrec>


Options
-------

- ``--font-file <TTF file>`` — Specify the path to a TrueType font (``.ttf``)
  file containing the font to use for rendering normal text.  This option is
  required.

- ``--bold-font-file <TTF file>`` — Specify the path to a TrueType font
  (``.ttf``) file containing the font to use for rendering bold text.  This
  option is required.

- ``--font-size <int>`` — Set the size of rendered text; defaults to 16

- ``-E <encoding>``, ``--encoding <encoding>`` — Specify the character encoding
  to use for reading the ttyrec file; defaults to UTF-8

- ``--ibm`` — Synonym for "``--encoding cp437``", `cp437
  <https://en.wikipedia.org/wiki/Code_page_437>`_ being the character encoding
  used by NetHack's `IBMgraphics <https://nethackwiki.com/wiki/IBMgraphics>`_
  option

- ``--fps <int>`` — Set the FPS (frames per second) rate of the output video;
  defaults to 12

- ``-o <filepath>``, ``--outfile <filepath>`` — Save the output video to the
  given path; defaults to ``ttyrec.mp4``

- ``--size <columns> <lines>`` — Set the dimensions of the terminal screen on
  which the ttyrec was recorded; defaults to 80×24
