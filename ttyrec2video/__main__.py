from   math         import ceil
from   pathlib      import Path
import click
import imageio
import numpy as np
from   PIL          import ImageFont
from   .            import __version__
from   .info        import ttyrec_info
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
@click.option('--size', type=(int, int), default=(80, 24), show_default=True,
              metavar='COLUMNS LINES',
              help='Size of screen on which ttyrec file was recorded')
@click.version_option(__version__, '-V', '--version',
                      message='ttyrec2video %(version)s')
@click.argument('ttyrec', type=click.File('rb'))
@click.argument('outfile', required=False)
def main(ttyrec, encoding, outfile, size, fps, font_size, font_file,
         bold_font_file):
    imageio.plugins.ffmpeg.download()
    imgr = ScreenRenderer(
        font      = ImageFont.truetype(font_file, size=font_size),
        bold_font = ImageFont.truetype(bold_font_file, size=font_size),
        font_size = font_size,
        columns   = size[0],
        lines     = size[1],
    )
    click.echo('Scanning {} ...'.format(ttyrec.name), err=True)
    info = ttyrec_info(ttyrec.name, read_ttyrec(ttyrec), list_frames=False)
    if info["frame_qty"] == 0:
        raise click.UsageError('{}: ttyrec file is empty'.format(ttyrec.name))
    click.echo('ttyrec length: {duration} ({frame_qty} distinct frames)'
               .format(**info), err=True)
    ttyrec.seek(0)
    if outfile is None:
        outfile = str(Path(ttyrec.name).with_suffix('.mp4'))
    click.echo('Writing {} ...'.format(outfile), err=True)
    with click.progressbar(
        imgr.render_frames(
            read_ttyrec(ttyrec, encoding=encoding, errors='replace'),
            fps,
            block_size=MACRO_BLOCK_SIZE,
        ),
        length=ceil(info["duration_seconds"] * fps),
    ) as mov_frames:
        imageio.mimwrite(outfile, map(np.asarray, mov_frames), fps=fps)

if __name__ == '__main__':
    main()
