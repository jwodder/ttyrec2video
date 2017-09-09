#!/usr/bin/python3
import click
from   read_ttyrec import read_ttyrec

@click.command()
@click.option('-E', '--encoding', default='utf-8')
@click.argument('ttyrec', type=click.File('rb'))
def main(ttyrec, encoding):
    for fr in read_ttyrec(ttyrec, encoding=encoding):
        print(fr.timestamp, fr.data)

if __name__ == '__main__':
    main()
