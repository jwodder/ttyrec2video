import click
import imageio
import numpy as np
from   PIL            import ImageFont
from   .read_ttyrec   import read_ttyrec
from   .screen_imager import ScreenImager

@click.command()
@click.option('-E', '--encoding', default='utf-8')
@click.option('-o', '--outfile', default='ttyrec.mp4')
@click.option('--fps', type=int, default=12)
@click.option('--size', type=(int, int), default=(80, 24))
@click.argument('ttyrec', type=click.File('rb'))
def main(ttyrec, encoding, outfile, size, fps):
    imgr = ScreenImager(
        font      = ImageFont.truetype('data/fonts/unifont.ttf', size=16),
        bold_font = ImageFont.truetype('data/fonts/unifont.ttf', size=16),
        font_size = 16,
        columns   = size[0],
        lines     = size[1],
    )
    imageio.plugins.ffmpeg.download()
    imageio.mimwrite(
        outfile,
        map(
            np.asarray,  # <https://stackoverflow.com/a/1095878/744178>
            imgr.slideshow(read_ttyrec(ttyrec, encoding=encoding), fps),
        ),
        format='mp4',
        fps=fps,
    )
    ### TODO: Include progress bar

if __name__ == '__main__':
    main()
