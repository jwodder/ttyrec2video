import click
from   .read_ttyrec import read_ttyrec

@click.command()
@click.option('-E', '--encoding', default='utf-8')
@click.argument('ttyrec', type=click.File('rb'), nargs=-1)
def main(ttyrec, encoding):
    for fp in ttyrec:
        frames = read_ttyrec(fp, encoding=encoding)
        first = next(frames)
        for fr in frames:
            last = fr
        print('{}\t{} frames\t{}'.format(
            fp.name, last.index + 1, last.timestamp - first.timestamp,
        ))

if __name__ == '__main__':
    main()
