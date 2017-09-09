#!/usr/bin/python3
__requires__ = ['pyte ~= 0.6.0']
import sys
import pyte
from   read_ttyrec import read_ttyrec

recfile, frameno = sys.argv[1:]
frameno = int(frameno)

screen = pyte.Screen(80, 24)
stream = pyte.Stream(screen)
with open(sys.argv[1], 'rb') as fp:
    frames = read_ttyrec(fp, encoding='utf-8')
    for _ in range(frameno):
        stream.feed(next(frames).data)
