#!/usr/bin/python3
import sys; sys.path.insert(1, sys.path[0] + '/..')
import pyte
from   lib.read_ttyrec import read_ttyrec

recfile, frameno = sys.argv[1:]
frameno = int(frameno)

screen = pyte.Screen(80, 24)
stream = pyte.Stream(screen)
with open(sys.argv[1], 'rb') as fp:
    frames = read_ttyrec(fp, encoding='utf-8')
    for _ in range(frameno):
        stream.feed(next(frames).data)
