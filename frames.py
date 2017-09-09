#!/usr/bin/python3
import sys
from   blessed     import Terminal
import click
from   colored     import attr, fg, bg
import pyte
from   read_ttyrec import read_ttyrec

FG = {}
FG.update({v: fg(k-30) for k,v in pyte.graphics.FG.items()})
FG.update({v: fg(i) for i,v in enumerate(pyte.graphics.FG_BG_256)})
FG["default"] = ''

BG = {}
BG.update({v: bg(k-40) for k,v in pyte.graphics.BG.items()})
BG.update({v: bg(i) for i,v in enumerate(pyte.graphics.FG_BG_256)})
BG["default"] = ''

@click.command()
@click.option('-E', '--encoding', default='utf-8')
@click.argument('ttyrec', type=click.File('rb'))
def main(ttyrec, encoding):
    screen = pyte.Screen(80, 24)
    stream = pyte.Stream(screen)
    with Terminal().cbreak():
        for fr in read_ttyrec(ttyrec, encoding=encoding):
            stream.feed(fr.data)
            for y in range(24):
                for x in range(80):
                    c = screen.buffer[y][x]
                    print(
                        FG[c.fg],
                        BG[c.bg],
                        attr('bold') if c.bold else '',
                        #attr('underline') if c.underline else '', # pyte 0.7.0?
                        attr('reverse') if c.reverse else '',
                        c.data,
                        attr('reset'),
                        end='',
                        sep='',
                    )
                if y+1 < 24:
                    print()
            sys.stdout.flush()
            ch = sys.stdin.read(1)
            if ch == 'q':
                break

if __name__ == '__main__':
    main()
