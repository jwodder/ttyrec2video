import click
import imageio
import numpy as np
from   PIL          import ImageFont
from   .            import __version__
from   .read_ttyrec import read_ttyrec
from   .renderer    import ScreenRenderer

# Width & height of ffmpeg input needs to be a multiple of this value or else
# imageio gets all complainy:
MACRO_BLOCK_SIZE = 16

def set_ibm_encoding(ctx, param, value):
    if value:
        ctx.params['encoding'] = 'cp437'

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('-E', '--encoding', default='utf-8', show_default=True,
              help='Character encoding of ttyrec file')
@click.option('--font-file', type=click.Path(exists=True, dir_okay=False),
              metavar='TTF_FILE', required=True)
@click.option('--bold-font-file', type=click.Path(exists=True, dir_okay=False),
              metavar='TTF_FILE', required=True)
@click.option('--font-size', type=int, default=16)
@click.option('--fps', type=int, default=12, show_default=True,
              help='Set output frames per second')
@click.option('--ibm', callback=set_ibm_encoding, expose_value=False,
              help='Synonym for "--encoding cp437"')
@click.option('-o', '--outfile', default='ttyrec.mp4', show_default=True)
@click.option('--size', type=(int, int), default=(80, 24), show_default=True,
              metavar='COLUMNS LINES',
              help='Size of screen on which ttyrec file was recorded')
@click.version_option(__version__, '-V', '--version',
                      message='ttyrec2video %(version)s')
@click.argument('ttyrec', type=click.File('rb'))
def main(ttyrec, encoding, outfile, size, fps, font_size, font_file,
         bold_font_file):
    imgr = ScreenRenderer(
        font      = ImageFont.truetype(font_file, size=font_size),
        bold_font = ImageFont.truetype(bold_font_file, size=font_size),
        font_size = font_size,
        columns   = size[0],
        lines     = size[1],
    )
    ### TODO: Read through the input at least once before beginning conversion
    ### so that encoding errors are caught as soon as possible?
    imageio.plugins.ffmpeg.download()
    imageio.mimwrite(
        outfile,
        map(
            np.asarray,  # <https://stackoverflow.com/a/1095878/744178>
            imgr.render_frames(
                read_ttyrec(ttyrec, encoding=encoding, errors='replace'),
                fps,
                block_size=MACRO_BLOCK_SIZE,
            ),
        ),
        format='mp4',
        fps=fps,
    )
    ### TODO: Include progress bar

if __name__ == '__main__':
    main()
