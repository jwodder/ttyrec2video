#!/usr/bin/python3
import click
from   PIL               import ImageFont
import pyte
from   lib.read_ttyrec   import read_ttyrec
from   lib.screen_imager import ScreenImager

@click.command()
@click.option('-E', '--encoding', default='utf-8')
@click.option('-o', '--outfile', default='ttyrec.png')
@click.argument('ttyrec', type=click.File('rb'))
@click.argument('frame', type=int)
def main(ttyrec, frame, encoding, outfile):
    screen = pyte.Screen(80, 24)
    stream = pyte.Stream(screen)
    frames = read_ttyrec(ttyrec, encoding=encoding)
    for _ in range(frame):
        stream.feed(next(frames).data)
    ScreenImager(
        font      = ImageFont.truetype('data/fonts/unifont.ttf', size=16),
        bold_font = ImageFont.truetype('data/fonts/unifont.ttf', size=16),
        font_size = 16,
        lines     = 24,
        columns   = 80,
    ).render(screen).save(outfile)

if __name__ == '__main__':
    main()
