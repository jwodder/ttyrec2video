from   io            import BytesIO
from   math          import ceil
from   pathlib       import Path
from   urllib.parse  import urlsplit
import click
import imageio
import requests
import numpy as np
from   PIL           import ImageFont
from   pkg_resources import resource_filename
from   .             import __version__
from   .reader       import ShortTTYRecError, read_ttyrec
from   .renderer     import ScreenRenderer

# Width & height of ffmpeg input needs to be a multiple of this value or else
# imageio gets all complainy:
MACRO_BLOCK_SIZE = 16

def font_file(fontname):
    return resource_filename('ttyrec2video', 'data/ubuntu-font/' + fontname)

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('-E', '--encoding', default='utf-8', show_default=True,
              help='Character encoding of ttyrec file')
@click.option('--font-file', type=click.Path(exists=True, dir_okay=False),
              metavar='TTF_FILE', default=font_file('UbuntuMono-R.ttf'),
              help='Font for regular-weight text')
@click.option('--bold-font-file', type=click.Path(exists=True, dir_okay=False),
              metavar='TTF_FILE', default=font_file('UbuntuMono-B.ttf'),
              help='Font for bold text')
@click.option('--font-size', type=int, default=16, show_default=True,
              metavar='POINTS', help='Font size of rendered text')
@click.option('--fps', type=int, default=12, show_default=True,
              help='Frames per second rate for output video')
@click.option('--ibm', is_flag=True, help='Synonym for "--encoding cp437"')
@click.option('--size', type=(int, int), default=(80, 24), show_default=True,
              metavar='COLUMNS LINES',
              help='Size of screen on which ttyrec file was recorded')
@click.version_option(__version__, '-V', '--version',
                      message='ttyrec2video %(version)s')
@click.argument('ttyrec')
@click.argument('outfile', required=False)
@click.pass_context
def main(ctx, ttyrec, encoding, ibm, outfile, size, fps, font_size, font_file,
         bold_font_file):
    """ Convert ttyrec files to videos """
    if ibm:
        encoding = 'cp437'
    fp, def_outfile = open_or_get(ttyrec)
    try:
        with fp:
            updates = list(read_ttyrec(fp, encoding=encoding, errors='replace'))
    except ShortTTYRecError as e:
        ctx.fail(str(e))
    if len(updates) < 2:
        ctx.fail(
            'ttyrec only has {} update{}; need at least two to make a video'
            .format(len(updates), 's' if len(updates) != 1 else '')
        )
    duration = updates[-1].timestamp - updates[0].timestamp
    click.echo(
        'ttyrec length: {} ({} distinct frames)'.format(duration, len(updates)),
        err=True,
    )
    imgr = ScreenRenderer(
        font      = ImageFont.truetype(font_file, size=font_size),
        bold_font = ImageFont.truetype(bold_font_file, size=font_size),
        font_size = font_size,
        columns   = size[0],
        lines     = size[1],
    )
    imageio.plugins.ffmpeg.download()
    if outfile is None:
        outfile = def_outfile
    click.echo('Writing {} ...'.format(outfile), err=True)
    with click.progressbar(
        imgr.render_updates(updates, fps, block_size=MACRO_BLOCK_SIZE),
        length=ceil(duration.total_seconds() * fps),
    ) as mov_frames:
        imageio.mimwrite(outfile, map(np.asarray, mov_frames), fps=fps)

def open_or_get(fname):
    if fname.lower().startswith(('http://', 'https://')):
        click.echo('Downloading {} ...'.format(fname), err=True)
        r = requests.get(fname)
        r.raise_for_status()
        fp = BytesIO(r.content)
        pth = Path(urlsplit(fname).path.rstrip('/').split('/')[-1] or 'ttyrec')
    else:
        click.echo('Reading {} ...'.format(fname), err=True)
        fp = click.open_file(fname, 'rb')
        pth = Path(fname)
    if pth.suffix.lower() == '.gz':
        import gzip
        fp  = gzip.open(fp, 'rb')
        pth = pth.with_suffix('')
    elif pth.suffix.lower() == '.bz2':
        import bz2
        fp  = bz2.open(fp, 'rb')
        pth = pth.with_suffix('')
    return fp, str(pth.with_suffix('.mp4'))

if __name__ == '__main__':
    main()
