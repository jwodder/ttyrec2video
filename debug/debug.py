#!/usr/bin/python3
import sys
import click
import pyte
from   read_ttyrec import read_ttyrec

@click.command()
@click.option('-E', '--encoding', default='utf-8')
@click.argument('ttyrec', type=click.File('rb'))
def main(ttyrec, encoding):
    screen = pyte.DebugScreen(sys.stdout)
    stream = pyte.Stream(screen)
    for i, fr in enumerate(read_ttyrec(ttyrec, encoding=encoding)):
        print('# Frame', i)
        stream.feed(fr.data)
        print()

if __name__ == '__main__':
    main()
