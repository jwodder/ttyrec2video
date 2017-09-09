#!/usr/bin/python3
import click
import pyte
from   read_ttyrec import read_ttyrec

@click.command()
@click.option('-E', '--encoding', default='utf-8')
@click.argument('ttyrec', type=click.File('rb'))
def main(ttyrec, encoding):
    screen = pyte.Screen(80, 24)
    stream = pyte.Stream(screen)
    fgs = set()
    bgs = set()
    for fr in read_ttyrec(ttyrec, encoding=encoding):
        stream.feed(fr.data)
        for y in range(24):
            for x in range(80):
                c = screen.buffer[y][x]
                if c.fg not in fgs:
                    click.echo('FG: ' + str(c.fg))
                    fgs.add(c.fg)
                if c.bg not in bgs:
                    click.echo('BG: ' + str(c.bg))
                    bgs.add(c.bg)
    click.echo(fgs)
    click.echo(bgs)

if __name__ == '__main__':
    main()
